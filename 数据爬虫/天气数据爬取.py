import requests
from lxml import etree
import csv


def getweather(url):
    weather_info = [] #新建一个列表，将爬取的每月数据放进去
    #请求头信息：浏览器版本型号，接收数据的编码格式
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'}
    #请求
    resp = requests.get(url, headers=headers)
    #数据预处理
    resp_html=etree.HTML(resp.text)
    #xpath提取所有数据
    resp_list=resp_html.xpath("//ul[@class='thrui']/li")
    #print(resp_list)

    #for循环迭代遍历
    for li in resp_list :
        day_weather_info={}
        day_weather_info['date_time']=li.xpath("./div[1]/text()")[0].split(' ')[0]
        high=li.xpath("./div[2]/text()")[0]
        day_weather_info['high']=high[:high.find('C')]

        low=li.xpath("./div[3]/text()")[0]
        day_weather_info['low'] = low[:low.find('C')]

        day_weather_info['weather']=li.xpath("./div[4]/text()")[0]

        weather_info.append(day_weather_info)

    return weather_info

weathers=[]
for month in range(1,13):
    weather_time ='2023'+('0'+str(month) if month <10 else str(month))

    url=f'https://lishi.tianqi.com/beijing/{weather_time}.html'
    weather=getweather(url)

    weathers.append(weather)

print(weathers)

with open("weather.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)

    writer.writerow(["日期","最高气温","最低气温","天气"])

    writer.writerows([list(day_weather_dict.values()) for month_weather in weathers for day_weather_dict in month_weather])

