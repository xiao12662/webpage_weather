import requests
import os
from datetime import datetime

def get_weather_info(code):
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
    # 1. 抓取数据
    url = "https://api.open-meteo.com/v1/forecast?latitude=28.23&longitude=112.94&current_weather=true"
    res = requests.get(url).json()
    curr = res['current_weather']
    
    # 2. 翻译
    status_text, emoji = get_weather_info(curr['weathercode'])
    weather_display = f"{emoji} {status_text}"

    # 3. 读取模板 (template.html)，而不是直接读 index.html
    # 这样可以保证每次运行都有 {code} 可以被替换
    if os.path.exists('template.html'):
        with open('template.html', 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        # 如果你还没建 template.html，先用 index.html 顶替一次
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()

    # 4. 替换
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    content = content.replace('{temp}', str(curr['temperature']))
    content = content.replace('{code}', weather_display)
    content = content.replace('{update_time}', now)

    # 5. 统一写回 index.html（这是展示给浏览器看的）
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    main()
