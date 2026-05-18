WITH weather AS (
    SELECT * FROM {{ ref('stg_weather') }}
),
stocks AS (
    SELECT * FROM {{ ref('stg_stocks') }}
),
news AS (
    SELECT
        topic,
        COUNT(*) AS news_count,
        MAX(published_at) AS latest_news_at
    FROM {{ ref('stg_news') }}
    GROUP BY topic
)

SELECT
    s.ticker,
    s.price,
    s.price_change,
    s.change_percent,
    s.volume,
    n.news_count,
    n.latest_news_at,
    s.extracted_at
FROM stocks s
LEFT JOIN news n ON (
    CASE
        WHEN s.ticker = 'AAPL' THEN 'Apple stock'
        WHEN s.ticker = 'GOOGL' THEN 'Google'
        WHEN s.ticker = 'MSFT' THEN 'Microsoft'
        WHEN s.ticker = 'AMZN' THEN 'Amazon'
        WHEN s.ticker = 'TSLA' THEN 'Tesla'
    END = n.topic
)
