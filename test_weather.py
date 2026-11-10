"""运行：python -m unittest -v（不访问网络）。"""

import io
import json
import unittest
from unittest.mock import patch
from urllib.error import URLError
from urllib.parse import parse_qs, urlparse

from main import run_agent
from weather import get_weather


class WeatherTests(unittest.TestCase):
    def test_success_and_request_parameters(self):
        places = {"results": [{"name": "北京", "admin1": "北京", "country": "中国",
                               "latitude": 39.9, "longitude": 116.4}]}
        forecast = {"timezone": "Asia/Shanghai", "current": {
            "time": "2026-11-10T15:00", "temperature_2m": 12.5,
            "apparent_temperature": 10.2, "relative_humidity_2m": 45,
            "weather_code": 0, "wind_speed_10m": 8.0,
        }}
        responses = [io.BytesIO(json.dumps(data).encode()) for data in (places, forecast)]
        with patch("weather.urlopen", side_effect=responses) as request:
            result = get_weather(" 北京 ")
        self.assertIn("城市：北京，中国", result)
        self.assertIn("温度：12.5 °C", result)
        self.assertIn("天气：晴", result)
        self.assertIn("Asia/Shanghai", result)
        geo_query = parse_qs(urlparse(request.call_args_list[0].args[0]).query)
        weather_query = parse_qs(urlparse(request.call_args_list[1].args[0]).query)
        self.assertEqual(geo_query["name"], ["北京"])
        self.assertEqual(weather_query["latitude"], ["39.9"])
        self.assertEqual(weather_query["timezone"], ["auto"])

    def test_empty_city_does_not_access_network(self):
        with patch("weather.urlopen") as request:
            self.assertIn("请输入城市", get_weather(" "))
        request.assert_not_called()

    def test_city_not_found(self):
        with patch("weather._get_json", return_value={}):
            self.assertIn("没有找到城市", get_weather("不存在的城市"))

    def test_network_failure_and_timeout(self):
        for error in (URLError("offline"), TimeoutError()):
            with self.subTest(error=error), patch("weather.urlopen", side_effect=error):
                self.assertIn("检查网络", get_weather("上海"))

    def test_invalid_json_and_service_error(self):
        for payload in (b"not json", b"[]", b'{"error": true}'):
            with self.subTest(payload=payload), patch("weather.urlopen", return_value=io.BytesIO(payload)):
                self.assertIn("天气服务", get_weather("上海"))

    def test_incomplete_forecast(self):
        places = {"results": [{"latitude": 31.2, "longitude": 121.5}]}
        with patch("weather._get_json", side_effect=[places, {"current": {}}]):
            self.assertIn("数据暂不完整", get_weather("上海"))

    def test_agent_routes_city_formats(self):
        for task in ("北京", "天气：北京", "天气: 北京", "查询天气 北京", "北京天气", "北京的天气", "weather Beijing"):
            with self.subTest(task=task), patch("main.get_weather", return_value="晴") as weather:
                self.assertIn("城市天气工具", run_agent(task))
                weather.assert_called_once_with("Beijing" if task == "weather Beijing" else "北京")

    def test_existing_tools(self):
        with patch("main.get_weather") as weather:
            self.assertIn("北京时间工具", run_agent("现在几点？"))
            self.assertIn("共有 2 个字符", run_agent("统计字数：你好"))
            self.assertIn("请使用格式", run_agent("统计字数"))
        weather.assert_not_called()


if __name__ == "__main__":
    unittest.main()
