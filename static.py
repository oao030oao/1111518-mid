import requests
from bs4 import BeautifulSoup
import json
import re

url = "https://zh.wikipedia.org/zh-tw/%E5%85%A8%E7%90%83%E6%9C%80%E9%AB%98%E9%9B%BB%E5%BD%B1%E7%A5%A8%E6%88%BF%E6%94%B6%E5%85%A5%E5%88%97%E8%A1%A8"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

table = soup.find("table", class_="wikitable")
rows = table.find_all("tr")[1:11]  # 前十名（跳過表頭）

movies = []

def clean_title(text):
    # 移除中括號註解與前後空白和換行符號
    text = re.sub(r"\[.*?\]", "", text)
    return text.strip()

def clean_revenue(text):
    # 移除註解、非數字/逗號/貨幣符號以外的內容
    text = re.sub(r"\[.*?\]", "", text)
    return re.sub(r"[^\d,\$]", "", text)

for row in rows:
    cols = row.find_all("td")
    if len(cols) >= 3:
        title = clean_title(cols[2].text)
        revenue = clean_revenue(cols[3].text)
        movies.append({
            "電影": title,
            "票房": revenue
        })

with open("static.json", "w", encoding="utf-8") as f:
    json.dump(movies, f, ensure_ascii=False, indent=4)
