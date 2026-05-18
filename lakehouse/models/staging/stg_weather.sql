SELECT
    city,
    CAST(temperature_f AS FLOAT) AS temperature_f,
    CAST(humidity AS INTEGER) AS humidity,
    weather AS weather_description,
    CAST(wind_speed AS FLOAT) AS wind_speed,
    extracted_at::TIMESTAMP AS extracted_at
FROM raw.weather
