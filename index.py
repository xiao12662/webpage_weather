import requests
import os
from datetime import datetime

def get_weather_info(code):
    try:
        c = int(code)
    except:
        return f"解析失败({code})", "⚠️"
        
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
    return weather_dict.get(c, (f"未知代码:{c}", "🌈"))

def main():
    # 1. 抓取
    url = "https://api.open-meteo.com/v1/forecast?latitude=28.23&longitude=112.94&current_weather=true"
    res = requests.get(url).json()
    curr = res['current_weather']
    temp = curr['temperature']
    code = curr['weathercode']

    # 2. 翻译
    status_text, emoji = get_weather_info(code)
    weather_display = f"{emoji} {status_text}"
    print(f"调试信息：当前天气是 {weather_display}")

    # 3. 读模板 (优先读 template.html)
    target_file = 'template.html' if os.path.exists('template.html') else 'index.html'
    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 4. 替换 (注意：这里要确保模板里真的有这三个词)
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    content = content.replace('{temp}', str(temp))
    content = content.replace('{code}', weather_display)
    content = content.replace('{update_time}', now)

    # 5. 强制写回 index.html
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)

    # 6. 推送调试消息到手机
    bark_key = os.getenv('BARK_KEY')
    if bark_key:
        requests.get(f"https://api.day.app/{bark_key}/机器人报告/网页已更新为：{weather_display}?level=active")

if __name__ == "__main__":
    main()
