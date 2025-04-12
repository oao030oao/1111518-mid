import requests
import csv
url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWA-37B285F2-E031-4B45-BA7B-7D94297D80BF&locationName=%E6%96%B0%E5%8C%97%E5%B8%82&elementName='

# 發送 GET 請求
response = requests.get(url)
data = response.json()

location_data = data['records']['location'][0]
location_name = location_data['locationName']
weather_elements = location_data['weatherElement']

# 建立時間區間列表
time_intervals = weather_elements[0]['time']
num_intervals = len(time_intervals)

# 初始化資料列表
weather_data = []

# 逐個時間區間提取資料
for i in range(num_intervals):
    interval = {}
    interval['地點'] = location_name
    interval['開始時間'] = weather_elements[0]['time'][i]['startTime']
    interval['結束時間'] = weather_elements[0]['time'][i]['endTime']
    # 提取各項天氣元素
    for element in weather_elements:
        element_name = element['elementName']
        parameter = element['time'][i]['parameter']
        value = parameter.get('parameterName', '')
        interval[element_name] = value
    weather_data.append(interval)

# 定義 CSV 欄位
fieldnames = ['地點', '開始時間', '結束時間'] + [element['elementName'] for element in weather_elements]

# 寫入 CSV 檔案
with open('api.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in weather_data:
        writer.writerow(row)
