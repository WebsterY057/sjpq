#B站  视频请求的隐藏处理，CTRL+F 搜索video 找到跟视频相关的链接
#将视频和音频合并

url= 'https://xy113x57x1x201xy.mcdn.bilivideo.cn:8082/v1/resource/94198756_da2-1-100024.m4s?agrr=0&build=0&buvid=5BA59746-D481-A1CA-946C-7361DC576BC863607infoc&bvc=vod&bw=617850&deadline=1747406735&dl=0&e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M%3D&f=u_0_0&gen=playurlv3&mcdnid=50026418&mid=3461576369637751&nbs=1&nettype=0&og=cos&oi=1874139289&orderid=0%2C3&os=mcdn&platform=pc&sign=923c31&tag=&traceid=trLkiWpxrjbZIP_0_e_N&uipk=5&uparams=e%2Cmid%2Coi%2Cuipk%2Cgen%2Cog%2Cdeadline%2Ctag%2Cnbs%2Cplatform%2Ctrid%2Cos&upsig=62fa266b246499029ea4c42ad5314a2e'


import requests

#获取请求链接所得到的数据

data =requests.get(url).content


file = open('B站视频.mp4', 'wb')

file.write(data)

