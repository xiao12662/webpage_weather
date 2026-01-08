import requests
import os
from datetime import datetime

def get_weather_info(code):
    try:
        c = int(code)
    except:
        return f"解析中({code})", "⏳"
        
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
    return weather_dict.get(c, (f"代码:{c}", "🌈"))

def main():
    # 1. 抓取 (长沙)
    url = "https://api.open-meteo.com/v1/forecast?latitude=28.23&longitude=112.94&current_weather=true"
    res = requests.get(url).json()
    curr = res['current_weather']
    
    # 2. 翻译天气
    status_text, emoji = get_weather_info(curr['weathercode'])
    # 拼接成类似 "☀️ 晴朗"
    weather_display = f"{emoji} {status_text}"

    # 3. 读模板 (必须确保仓库里有 template.html)
    if os.path.exists('template.html'):
        with open('template.html', 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        # 兜底：如果没有模板，就打印错误
        print("错误：找不到 template.html 文件！")
        return

    # 4. 替换 (精准匹配 {temp}, {code}, {update_time})
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    content = content.replace('{temp}', str(curr['temperature']))
    content = content.replace('{code}', weather_display)
    content = content.replace('{update_time}', now)

    # 5. 写入展示用的 index.html
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"更新成功！当前天气：{weather_display}")

if __name__ == "__main__":
    main()
