Python
import requests
import json
import os
from datetime import datetime

API_KEY = os.getenv('NEWS_API_KEY', '')

def fetch_data(query, page_size=20):
    if not API_KEY: return []
    url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&pageSize={page_size}&apiKey={API_KEY}&language=zh"
    try:
        res = requests.get(url)
        return res.json().get('articles', []) if res.status_code == 200 else []
    except: return []

def main():
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M')
    if API_KEY:
        macro = fetch_data("(台灣 經濟) OR (美股 聯準會) OR (歐洲 降息)", 30)[:15]
        corn = fetch_data("(玉米 期貨) OR (CBOT 玉米)", 10)[:5]
        data = {"updated_at": now_str, "macro_news": macro, "corn_news": corn}
    else:
        # 沒填金鑰時的防呆模擬數據
        data = {
            "updated_at": now_str,
            "macro_news": [{"source": {"name": "財經脈動"}, "title": "測試數據：請至 Settings 設定您的 NEWS_API_KEY", "description": "看見此訊息代表網站架設成功，請補上 API 金鑰以抓取即時新聞。", "url": "https://newsapi.org", "publishedAt": datetime.now().isoformat()}] * 15,
            "corn_news": [{"source": {"name": "期貨行情"}, "title": "測試數據：玉米期貨觀測中", "description": "看見此訊息代表期貨區塊運作正常。", "url": "https://newsapi.org", "publishedAt": datetime.now().isoformat()}] * 3
        }
    with open('news_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()
