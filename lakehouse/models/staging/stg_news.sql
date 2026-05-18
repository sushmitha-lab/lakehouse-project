SELECT
    topic,
    title,
    source,
    published_at::TIMESTAMP AS published_at,
    extracted_at::TIMESTAMP AS extracted_at
FROM raw.news
