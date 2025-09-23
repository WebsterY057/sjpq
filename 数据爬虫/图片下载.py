import requests

url = 'https://img-s.msn.cn/tenant/amp/entityid/AA13c1OB.img'
header={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
}
#发送请求获取响应信息
response = requests.get(url=url,headers = header)

#将返回的相应信息的内容写入到一个图片文件
with open ("baidu.jpg", 'wb') as f:
    f.write(response.content)