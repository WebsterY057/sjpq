#B站  视频请求的隐藏处理，CTRL+F 搜索video 找到跟视频相关的链接
#将视频和音频合并

url= 'https://xy125x74x62x236xy.mcdn.bilivideo.cn:8082/v1/resource/94198756_da2-1-30232.m4s?agrr=0&build=0&buvid=5BA59746-D481-A1CA-946C-7361DC576BC863607infoc&bvc=vod&bw=130154&deadline=1747407291&dl=0&e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M%3D&f=u_0_0&gen=playurlv3&mcdnid=50026418&mid=3461576369637751&nbs=1&nettype=0&og=cos&oi=1874139289&orderid=0%2C3&os=mcdn&platform=pc&sign=0fe5fb&tag=&traceid=treZxZeTvquDzt_0_e_N&uipk=5&uparams=e%2Ctag%2Cnbs%2Cdeadline%2Cuipk%2Cplatform%2Ctrid%2Coi%2Cmid%2Cgen%2Cos%2Cog&upsig=4a98f053a113625bede88bd82cfa8ac7'


import requests

#获取请求链接所得到的数据

data =requests.get(url).content


file = open('B站音频.mp3', 'wb')

file.write(data)

