---
name: weather_query
description: >
  Query current weather for a specific city and answer in Chinese with temperature,
  weather condition, humidity, wind, precipitation, visibility, UV index, and
  observation time when available. Use this skill whenever the user asks about
  today's weather, current temperature, rain, wind, humidity, visibility, UV
  exposure, or outdoor conditions for a city or location. If the user asks for a
  forecast, explain that this skill is optimized for current weather and provide
  only the current conditions returned by the script.
---

# Weather Query Skill

## Purpose

Use this skill to answer weather-related questions with data from the bundled
script instead of guessing. Weather changes constantly, so stale memory or
invented values are not acceptable.

## Workflow

1. Extract the city or location from the user's request.
2. If the user did not provide a city, ask a short clarification question.
3. Run the bundled script from this skill directory:

```bash
python ./scripts/get_weather.py "<city>"
```

4. Read the JSON output.
5. If the output contains `error`, tell the user the query failed and include the
   short reason from the script. Do not fabricate weather values.
6. Otherwise, answer naturally in Chinese and include the key fields that are
   present.

## Output Guidance

For a normal successful query, prefer this concise Chinese format:

```text
<城市>当前天气：
- 天气：<天气状况>
- 温度：<温度>
- 体感温度：<体感温度，如有>
- 湿度：<湿度，如有>
- 风况：<风向/风速，如有>
- 降水：<降水量，如有>
- 能见度：<能见度，如有>
- UV指数：<UV指数，如有>
- 观测时间：<时间，如有>
```

If the user asks a casual question such as "上海今天冷吗？", answer the implied
question directly first, then include the weather details.

## Script Contract

`scripts/get_weather.py` accepts one city/location argument. Multi-word locations
are supported when quoted.

Successful output:

```json
{
  "city": "Shanghai",
  "requested_city": "上海",
  "weather": "Partly cloudy",
  "temperature": "30 C",
  "feels_like": "33 C",
  "humidity": "70%",
  "wind": "NE 11 km/h",
  "precipitation": "0.0 mm",
  "visibility": "10 km",
  "uv_index": "7",
  "observation_time": "06:30 AM",
  "source": "wttr.in"
}
```

Failure output:

```json
{
  "error": "weather query failed: ...",
  "city": "Shanghai"
}
```

## Notes

- Do not answer with made-up weather data.
- Do not use random fallback values.
- Do not claim the result is a multi-day forecast unless the script is extended
  to support forecasts.
- Preserve the user's city name in the response when the provider returns a
  normalized or English location name.
- If the user asks specifically for AQI or pollution, explain that the script
  does not provide AQI; report available weather/outdoor fields only.
