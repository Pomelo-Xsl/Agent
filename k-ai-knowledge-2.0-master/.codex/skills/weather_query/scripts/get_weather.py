import json
import sys
import urllib.error
import urllib.parse
import urllib.request


WTTR_URL = "https://wttr.in/{city}?format=j1"
TIMEOUT_SECONDS = 10


def _value(items, key):
    if not items:
        return ""
    value = items[0].get(key, "")
    return str(value).strip()


def _description(current):
    descriptions = current.get("weatherDesc") or []
    if descriptions and isinstance(descriptions, list):
        return _value(descriptions, "value")
    return ""


def _with_unit(value, unit):
    value = str(value).strip()
    if not value:
        return ""
    if unit == "%":
        return f"{value}%"
    return f"{value} {unit}"


def get_weather(city: str):
    city = city.strip()
    if not city:
        return {"error": "please input the city name"}

    encoded_city = urllib.parse.quote(city)
    url = WTTR_URL.format(city=encoded_city)

    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "codex-weather-query-skill/1.0",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return {"error": f"weather query failed: HTTP {exc.code}", "city": city}
    except urllib.error.URLError as exc:
        return {"error": f"weather query failed: {exc.reason}", "city": city}
    except TimeoutError:
        return {"error": "weather query failed: request timed out", "city": city}
    except json.JSONDecodeError:
        return {"error": "weather query failed: invalid provider response", "city": city}

    current = (payload.get("current_condition") or [{}])[0]
    nearest_area = (payload.get("nearest_area") or [{}])[0]
    provider_city = _value(nearest_area.get("areaName") or [], "value") or city

    result = {
        "city": provider_city,
        "requested_city": city,
        "weather": _description(current),
        "temperature": _with_unit(current.get("temp_C", ""), "C"),
        "feels_like": _with_unit(current.get("FeelsLikeC", ""), "C"),
        "humidity": _with_unit(current.get("humidity", ""), "%"),
        "wind": " ".join(
            part
            for part in [
                current.get("winddir16Point", ""),
                _with_unit(current.get("windspeedKmph", ""), "km/h"),
            ]
            if part
        ),
        "precipitation": _with_unit(current.get("precipMM", ""), "mm"),
        "visibility": _with_unit(current.get("visibility", ""), "km"),
        "uv_index": str(current.get("uvIndex", "")).strip(),
        "observation_time": current.get("observation_time", ""),
        "source": "wttr.in",
    }

    return {key: value for key, value in result.items() if value}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "please input the city name"}, ensure_ascii=False))
        return 1

    city = " ".join(sys.argv[1:])
    result = get_weather(city)
    exit_code = 1 if "error" in result else 0
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
