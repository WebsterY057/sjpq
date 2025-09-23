import requests
#UA伪装，将对应的user-agent封装到一个字典中
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
}
#指定url
url="https://www.sogou.com/web"
#处理url携带的参数：封装到字典中
kw=input("word:")
param={
     'query':kw
}
#发起请求，get方法会返回一个相应对象
response=requests.get(url=url,params=param,headers=headers)
#获取相应数据。text，返回的是字符串形式的响应数据
page_text=response.text
filename=kw +'.html'

print(page_text)
#持久化存储
with open(filename,'w',encoding='utf-8') as fp:
     fp.write(page_text)
print('filename,保存成功')