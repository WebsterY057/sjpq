# 导入requests库，用于发送HTTP请求
import requests
# 导入json库，用于处理JSON数据
import json

# UA伪装：设置User-Agent头部信息，模拟浏览器访问以防止被反爬
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
}

# 指定百度翻译的API接口地址
url = "https://fanyi.baidu.com/sug"

# 处理请求参数：通过用户输入获取要翻译的单词
word = input("word:")
# 将参数封装为字典，键名'kw'是百度翻译接口要求的参数名
data = {
    'kw': word
}

# 发送POST请求，携带URL、参数和请求头，获取服务器响应
response = requests.post(url=url, data=data, headers=headers)

# 解析响应内容为JSON格式（自动转换为Python字典对象）
dic_obj = response.json()
# 打印原始响应数据（调试用）
print(dic_obj)

# 持久化存储：构造文件名（翻译词+.json）
filename = word + '.json'
# 以写入模式打开文件，指定utf-8编码解决中文乱码问题
fp = open(filename, 'w', encoding='utf-8')
# 将字典数据写入JSON文件，ensure_ascii=False确保中文正常显示
json.dump(dic_obj, fp=fp, ensure_ascii=False)

# 提示操作完成
print('翻译成功')