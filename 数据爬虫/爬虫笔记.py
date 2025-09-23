#Xpath即为XML路径语言，是用来确定XML文档中某部分位置的语言
#lxml专门用来解析xml文档的库
"""
1.导入lxml
2.将获取的网页内容转化为xml
3.通过xpath去定位和解析页面中的内容

xpth数据提取的技巧：
    1，定位到包含所有数据的元素//ol
    2，再从中找到包含单条数据所有内容的元素 //ol/li
    3，对定位到包含所有元素的列表进行遍历，得到包含单条数据的元素
    4，在提取单条数据中的详细内容
"""
from lxml import etree

page = open ('douban.html','r',encoding='utf-8').read()

html = etree.HTML(page)

data_list = html.xpath("//ol/li")

for li in data_list:
    title = li.xpath()
    score = li.xpath()

    print("电影的名称:")
