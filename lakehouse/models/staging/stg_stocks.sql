SELECT
    ticker,
    CAST(price AS FLOAT) AS price,
    CAST(change AS FLOAT) AS price_change,
    REPLACE(change_percent, '%', '')::FLOAT AS change_percent,
    CAST(volume AS BIGINT) AS volume,
    extracted_at::TIMESTAMP AS extracted_at
FROM raw.stocks
