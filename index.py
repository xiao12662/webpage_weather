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
    
    from datetime import datetime, timedelta, timezone

    # 1. 获取北京时间
    beijing_time = timezone(timedelta(hours=8))
    now_bj = datetime.now(beijing_time)

    # 2. 强行将分钟、秒、毫秒设为 0 (抹零)
    # 这样无论它是 10:05 还是 10:15 跑的，都会显示 10:00:00
    fixed_now = now_bj.replace(minute=0, second=0, microsecond=0)

    # 3. 格式化输出
    update_time_str = fixed_now.strftime('%Y-%m-%d %H:%M:%S')

    now = datetime.now(beijing_time).strftime('%Y-%m-%d %H:%M:%S')
    # 确保是从 api 返回的 json 里实时获取的
    temp = curr['temperature'] 

    # 确保这一行没有被删掉或注释掉
    content = content.replace('{temp}', str(temp))
    content = content.replace('{code}', weather_display)
    content = content.replace('{update-time}', update_time_str)

    # 5. 写入展示用的 index.html
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"更新成功！当前天气：{weather_display}")

if __name__ == "__main__":
    main()
