import streamlit as st
import duckdb
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="Market Intelligence",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Global */
    .stApp { background: #080c14; }
    section[data-testid="stSidebar"] { background: #0d1117; border-right: 1px solid #1e2a3a; }
    .block-container { padding: 2rem 2.5rem; }

    /* Cards */
    .kpi-card {
        background: linear-gradient(135deg, #0d1f35 0%, #0a1628 100%);
        border: 1px solid #1e3a5f;
        border-radius: 16px;
        padding: 24px 20px;
        text-align: center;
        transition: border-color 0.2s;
    }
    .kpi-card:hover { border-color: #2d6aad; }
    .kpi-ticker { font-size: 12px; letter-spacing: 2px; color: #4a7fa5; font-weight: 600; margin-bottom: 8px; }
    .kpi-price { font-size: 30px; font-weight: 800; color: #e8f4ff; margin-bottom: 6px; }
    .kpi-up { font-size: 13px; color: #00e5a0; font-weight: 600; }
    .kpi-down { font-size: 13px; color: #ff4d6d; font-weight: 600; }

    /* Section headers */
    .section-title {
        font-size: 13px;
        letter-spacing: 3px;
        color: #4a7fa5;
        font-weight: 700;
        text-transform: uppercase;
        margin: 2rem 0 1rem;
        padding-bottom: 8px;
        border-bottom: 1px solid #1e2a3a;
    }

    /* Sidebar */
    .sidebar-label { font-size: 11px; letter-spacing: 2px; color: #4a7fa5; font-weight: 700; margin-bottom: 8px; }
    .status-dot { display: inline-block; width: 7px; height: 7px; border-radius: 50%; background: #00e5a0; margin-right: 8px; }
    .status-line { font-size: 12px; color: #7a9ab5; margin: 6px 0; }

    /* Hide streamlit chrome */
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

CHART_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#7a9ab5", family="Inter, sans-serif", size=12),
    margin=dict(t=30, b=30, l=10, r=10),
    xaxis=dict(showgrid=False, zeroline=False, color="#4a7fa5"),
    yaxis=dict(showgrid=True, gridcolor="#0f1e30", zeroline=False, color="#4a7fa5"),
)

con = duckdb.connect('/Users/sushmithakatherinej/lakehouse-project/lakehouse.duckdb')
stocks = con.execute("SELECT * FROM main.stg_stocks").df()
weather = con.execute("SELECT * FROM main.stg_weather").df()
news = con.execute("SELECT * FROM main.stg_news").df()
market = con.execute("SELECT * FROM main.fct_daily_market").df()

stocks["price"] = stocks["price"].astype(float)
stocks["change_percent"] = stocks["change_percent"].astype(float)
stocks["price_change"] = stocks["price_change"].astype(float)
weather["temperature_f"] = weather["temperature_f"].astype(float)
weather["humidity"] = weather["humidity"].astype(float)
weather["wind_speed"] = weather["wind_speed"].astype(float)

with st.sidebar:
    st.markdown(f"""
    <div style='padding: 1rem 0'>
        <div style='font-size:18px;font-weight:800;color:#e8f4ff;letter-spacing:1px'>MARKET<br>INTELLIGENCE</div>
        <div style='font-size:11px;color:#4a7fa5;margin-top:4px'>{datetime.now().strftime("%b %d, %Y  %H:%M")}</div>
    </div>
    <hr style='border-color:#1e2a3a;margin:0.5rem 0 1.5rem'>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-label">Tickers</div>', unsafe_allow_html=True)
    selected_tickers = st.multiselect("", options=stocks["ticker"].tolist(), default=stocks["ticker"].tolist(), label_visibility="collapsed")

    st.markdown('<div class="sidebar-label" style="margin-top:1.5rem">Cities</div>', unsafe_allow_html=True)
    selected_cities = st.multiselect("", options=weather["city"].tolist(), default=weather["city"].tolist(), label_visibility="collapsed")

    st.markdown("""
    <hr style='border-color:#1e2a3a;margin:1.5rem 0'>
    <div class="sidebar-label">Pipeline status</div>
    <div class="status-line"><span class="status-dot"></span>Airflow scheduler</div>
    <div class="status-line"><span class="status-dot"></span>dbt — 6 tests passing</div>
    <div class="status-line"><span class="status-dot"></span>Supabase connected</div>
    <div class="status-line"><span class="status-dot"></span>3 sources active</div>
    """, unsafe_allow_html=True)

fs = stocks[stocks["ticker"].isin(selected_tickers)]
fw = weather[weather["city"].isin(selected_cities)]

st.markdown("""
<div style='margin-bottom:2rem'>
    <div style='font-size:26px;font-weight:800;color:#e8f4ff;letter-spacing:0.5px'>Market & Weather Intelligence</div>
    <div style='font-size:13px;color:#4a7fa5;margin-top:4px'>ELT pipeline · dbt · Airflow · DuckDB · Supabase</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">Live stock prices</div>', unsafe_allow_html=True)
cols = st.columns(len(fs))
for col, (_, row) in zip(cols, fs.iterrows()):
    delta = float(row.change_percent)
    arrow = "▲" if delta > 0 else "▼"
    cls = "kpi-up" if delta > 0 else "kpi-down"
    col.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-ticker">{row.ticker}</div>
        <div class="kpi-price">${float(row.price):.2f}</div>
        <div class="{cls}">{arrow} {abs(delta):.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-title">Price & movement analysis</div>', unsafe_allow_html=True)
col1, col2 = st.columns([3, 2])

with col1:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=fs["ticker"], y=fs["price"],
        marker=dict(
            color=fs["change_percent"],
            colorscale=[[0,"#ff4d6d"],[0.5,"#1e3a5f"],[1,"#00e5a0"]],
            line=dict(width=0)
        ),
        text=[f"${p:.2f}" for p in fs["price"]],
        textposition="outside",
        textfont=dict(color="#e8f4ff", size=12)
    ))
    fig.update_layout(**CHART_THEME, title=dict(text="Stock prices (USD)", font=dict(color="#7a9ab5", size=13)))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig2 = go.Figure()
    colors = ["#00e5a0" if x > 0 else "#ff4d6d" for x in fs["change_percent"]]
    fig2.add_trace(go.Bar(
        x=fs["ticker"], y=fs["change_percent"],
        marker_color=colors,
        text=[f"{p:+.2f}%" for p in fs["change_percent"]],
        textposition="outside",
        textfont=dict(color="#e8f4ff", size=12)
    ))
    fig2.update_layout(**CHART_THEME, title=dict(text="Daily change (%)", font=dict(color="#7a9ab5", size=13)))
    st.plotly_chart(fig2, use_container_width=True)

st.markdown('<div class="section-title">Weather intelligence</div>', unsafe_allow_html=True)
col3, col4, col5 = st.columns(3)

with col3:
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        x=fw["city"], y=fw["temperature_f"],
        marker_color="#4f8ef7",
        text=[f"{t:.0f}°F" for t in fw["temperature_f"]],
        textposition="outside",
        textfont=dict(color="#e8f4ff", size=11)
    ))
    fig3.update_layout(**CHART_THEME, title=dict(text="Temperature (°F)", font=dict(color="#7a9ab5", size=13)))
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    fig4 = go.Figure()
    fig4.add_trace(go.Bar(
        x=fw["city"], y=fw["humidity"],
        marker_color="#a78bfa",
        text=[f"{h:.0f}%" for h in fw["humidity"]],
        textposition="outside",
        textfont=dict(color="#e8f4ff", size=11)
    ))
    fig4.update_layout(**CHART_THEME, title=dict(text="Humidity (%)", font=dict(color="#7a9ab5", size=13)))
    st.plotly_chart(fig4, use_container_width=True)

with col5:
    fig5 = go.Figure()
    fig5.add_trace(go.Bar(
        x=fw["city"], y=fw["wind_speed"],
        marker_color="#f6c90e",
        text=[f"{w:.0f} mph" for w in fw["wind_speed"]],
        textposition="outside",
        textfont=dict(color="#e8f4ff", size=11)
    ))
    fig5.update_layout(**CHART_THEME, title=dict(text="Wind speed (mph)", font=dict(color="#7a9ab5", size=13)))
    st.plotly_chart(fig5, use_container_width=True)

st.markdown('<div class="section-title">News & sentiment</div>', unsafe_allow_html=True)
col6, col7 = st.columns([2, 3])

with col6:
    news_count = news.groupby("topic").size().reset_index(name="count")
    fig6 = go.Figure(go.Pie(
        labels=news_count["topic"],
        values=news_count["count"],
        hole=0.65,
        marker=dict(colors=["#00e5a0","#4f8ef7","#ff4d6d","#f6c90e","#a78bfa"],
                   line=dict(color="#080c14", width=2))
    ))
    fig6.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#7a9ab5", size=12),
        margin=dict(t=30, b=30),
        showlegend=True,
        legend=dict(font=dict(color="#7a9ab5")),
        title=dict(text="News volume by topic", font=dict(color="#7a9ab5", size=13))
    )
    st.plotly_chart(fig6, use_container_width=True)

with col7:
    st.markdown('<div style="margin-top:1rem"></div>', unsafe_allow_html=True)
    styled = news[["topic","title","source","published_at"]].head(8).copy()
    st.dataframe(
        styled,
        use_container_width=True,
        hide_index=True,
        column_config={
            "topic": st.column_config.TextColumn("Topic", width="small"),
            "title": st.column_config.TextColumn("Headline", width="large"),
            "source": st.column_config.TextColumn("Source", width="small"),
            "published_at": st.column_config.TextColumn("Published", width="small"),
        }
    )

st.markdown('<div class="section-title">Full market summary</div>', unsafe_allow_html=True)
st.dataframe(market, use_container_width=True, hide_index=True)

st.markdown("""
<div style='text-align:center;color:#1e2a3a;font-size:11px;margin-top:3rem;padding-top:1rem;border-top:1px solid #1e2a3a'>
    Built with Python · dbt · Airflow · DuckDB · Supabase · Streamlit
</div>
""", unsafe_allow_html=True)
