"""通过 Open-Meteo 查询城市天气，只使用 Python 标准库。"""

import json
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen


WEATHER_CODES = {
    0: "晴", 1: "大部晴朗", 2: "局部多云", 3: "阴天",
    45: "雾", 48: "雾凇", 51: "小毛毛雨", 53: "毛毛雨", 55: "大毛毛雨",
    56: "轻度冻毛毛雨", 57: "强冻毛毛雨",
    61: "小雨", 63: "中雨", 65: "大雨", 66: "轻度冻雨", 67: "强冻雨",
    71: "小雪", 73: "中雪", 75: "大雪", 77: "雪粒",
    80: "小阵雨", 81: "中阵雨", 82: "强阵雨",
    85: "小阵雪", 86: "强阵雪", 95: "雷暴",
    96: "雷暴伴小冰雹", 99: "雷暴伴大冰雹",
}


class WeatherError(Exception):
    """可直接展示给用户的天气查询错误。"""


def _get_json(endpoint: str, params: dict) -> dict:
    url = f"{endpoint}?{urlencode(params)}"
    try:
        with urlopen(url, timeout=10) as response:
            data = json.load(response)
    except (URLError, TimeoutError, OSError) as exc:
        raise WeatherError("天气服务暂时无法连接，请检查网络后重试。") from exc
    except (ValueError, UnicodeError) as exc:
        raise WeatherError("天气服务返回了无法解析的数据，请稍后重试。") from exc
    if not isinstance(data, dict) or data.get("error"):
        raise WeatherError("天气服务返回异常，请稍后重试。")
    return data


def get_weather(city: str) -> str:
    """先将城市转为经纬度，再查询该位置的当前天气。"""
    city = city.strip()
    if not city:
        return "请输入城市，例如：天气：北京 / 北京 / --city 上海。"

    try:
        places = _get_json("https://geocoding-api.open-meteo.com/v1/search", {
            "name": city, "count": 1, "language": "zh", "format": "json",
        })
        results = places.get("results", [])
        if not results:
            return f"没有找到城市“{city}”，请检查名称，或尝试拼音、英文名称。"
        place = results[0]
        data = _get_json("https://api.open-meteo.com/v1/forecast", {
            "latitude": place["latitude"], "longitude": place["longitude"],
            "current": "temperature_2m,apparent_temperature,relative_humidity_2m,weather_code,wind_speed_10m",
            "temperature_unit": "celsius", "wind_speed_unit": "kmh", "timezone": "auto",
        })
        current = data["current"]
        required = ("time", "temperature_2m", "apparent_temperature",
                    "relative_humidity_2m", "weather_code", "wind_speed_10m")
        if any(current.get(key) is None for key in required):
            raise WeatherError("该城市的天气数据暂不完整，请稍后重试。")
        # 显示实际匹配的地区，方便发现同名城市的误匹配。
        location = "，".join(dict.fromkeys(
            str(place[key]) for key in ("name", "admin1", "country") if place.get(key)
        ))
        description = WEATHER_CODES.get(current["weather_code"], "未知天气")
        return (
            f"城市：{location}\n"
            f"数据时间：{current['time'].replace('T', ' ')}（{data['timezone']}）\n"
            f"天气：{description}\n"
            f"温度：{current['temperature_2m']} °C\n"
            f"体感温度：{current['apparent_temperature']} °C\n"
            f"相对湿度：{current['relative_humidity_2m']}%\n"
            f"风速：{current['wind_speed_10m']} km/h\n"
            "来源：Open-Meteo（当前天气为模型估算）"
        )
    except WeatherError as exc:
        return str(exc)
    except (KeyError, IndexError, TypeError, AttributeError):
        return "天气服务返回的数据不完整，请稍后重试。"
