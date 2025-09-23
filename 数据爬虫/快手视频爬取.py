#更改链接和名称可用

url = ('https://k0u6fyaayey90z.djvod.ndcimgs.com/bs2/photo-video-mz/5244441931765823360_d28325ebc9db8c92_7316_hd15.mp4?tag=1-1747316747-unknown-0-4erjo8yrbt-d841fd291526bddd&provider=self&clientCacheKey=3xf2pqquju9m3z4_72b251bd&di=JA4EXXYgNWp4AxlDoTDn7w==&bp=10004&ocid=100000348&tt=hd15&ss=vp')

import  requests
#get 专门对于一个链接发送网络请求参数
data = requests.get(url).content
print(data)
#w:写入文件 b：二进制数据
file = open('时代少年团.mp4', 'wb')
# .write :往文件中写入数据的方法
file.write(data)

#思路：首先找到短视频的url，向链接发送请求，收到回应之后，将回应写入文件





