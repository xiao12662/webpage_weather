import requests
import os
from datetime import datetime

def main():
    # 1. 获取天气 (长沙)
    weather_url = "https://api.open-meteo.com/v1/forecast?latitude=28.23&longitude=112.94&current_weather=true"
    res = requests.get(weather_url).json()
    temp = res['current_weather']['temperature']
    code = res['current_weather']['weathercode']

    # 2. 读取 HTML 模板
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 3. 填充最新数据
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    html = html.replace('{temp}', str(temp))
    html = html.replace('{code}', str(code))
    html = html.replace('{update_time}', now)

    # 4. 保存
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    # 5. 可选：发送推送
    bark_key = os.getenv('BARK_KEY')
    if bark_key:
        requests.get(f"https://api.day.app/{bark_key}/网页已更新/当前气温 {temp}度?level=active")

if __name__ == "__main__":
    main()
