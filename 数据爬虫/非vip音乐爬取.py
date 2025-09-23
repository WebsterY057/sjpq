#爬虫：爬取网络中的数据——网页、视频、音频、图片、文档

'''爬取步骤：
1、获取数据源链接——URL  链接  网址，访问网络中的数据
2、对于这个数据源地址发送一次网络请求，第三方模块，requests 打开终端 pip install ...——拿到数据
3、处理这个数据，保存，本地文件/数据库'''

#更改链接和名称可用

url = ('https://m10.music.126.net/20250515210247/78ff23cb060cf39e6c7b402956196de6/yyaac/obj/wonDkMOGw6XDiTHCmMOi/3022726896/5326/eb4e/a069/3e01f1db46c1491a9146df34b979e74a.m4a?vuutv=v+/D4aUcMuRVFjT/2CtQBoJMKiQpO1BExSpzX0mTTD/hCt+rvScTUslSf6v0Wx/oRR6IpQvgzUiwAK5XtF4E/UGQWqDnZ9djYtYV6nhvA9o=')

import  requests
#get 专门对于一个链接发送网络请求参数
data = requests.get(url).content
print(data)
#w:写入文件 b：二进制数据
file = open('跨不过的距离.mp3', 'wb')
# .write :往文件中写入数据的方法
file.write(data)