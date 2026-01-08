import requests
import os
from datetime import datetime

def get_weather_info(code):
    # 核心修复：确保 code 是整数
    code = int(code) 
    
    weather_dict = {
        0: ("晴朗", "☀️"),
        1: ("晴间多云", "🌤️"),
        2: ("多云", "⛅"),
        3: ("阴天", "☁️"),
        45: ("雾", "🌫️"),
        48: ("霾", "🌫️"),
        51: ("毛毛雨", "🌦️"),
        61: ("小雨", "🌧️"),
        71: ("小雪", "🌨️"),
        95: ("雷阵雨", "⛈️")
    }
    return weather_dict.get(code, (f"代码:{code}", "🌈"))

def main():
    url = "https://api.open-meteo.com/v1/forecast?latitude=28.23&longitude=112.94&current_weather=true"
    res = requests.get(url).json()
    temp = res['current_weather']['temperature']
    code = res['current_weather']['weathercode']

    status_text, emoji = get_weather_info(code)
    weather_display = f"{emoji} {status_text}"

    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    html = html.replace('{temp}', str(temp))
    html = html.replace('{code}', weather_display)
    html = html.replace('{update_time}', now)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
