import pandas as pd
from pyecharts import  options as opts
from pyecharts.charts import Bar,Timeline
import numpy
print(numpy.__file__)  # 例如：D:\anaconda\envs\DL\lib\site-packages\numpy\__init__.py
#用pandas.read_csv()读取指定的excel文件，选择编码格式gb18030

df=pd.read_csv('weather.csv', encoding='gb18030')
#print(df['日期'])

df['日期']=df['日期'].apply(lambda x:pd.to_datetime(x))

df['month']=df['日期'].dt.month

df_agg=df.groupby(['month','天气']).size().reset_index()
print(df_agg)

df_agg.columns=['month','tianqi','count']
print(df_agg)

print(df_agg[df_agg['month']==1][['tianqi','count']].sort_values(by='count',ascending=False).values.tolist())

#实例化一个时间序列的对象
timeline=Timeline()
#播放参数：设置时间间隔2秒 单位是：ms
timeline.add_schema(play_interval=2000)

for month in df_agg['month'].unique():
    data=(
        df_agg[df_agg['month']==month][['tianqi','count']]
    .sort_values(by='count',ascending=True).values.tolist()
    )
    print(data)

    #绘制柱状图
    bar=Bar()
    #x轴是天气名称
    bar.add_xaxis([x[0] for x in data])

    #y轴是出现次数
    bar.add_yaxis('',[x[1] for x in data])

    #让柱状图横着放
    bar.reversal_axis()
    #将计数标签放置在图形右边
    bar.set_series_opts(label_opts=opts.LabelOpts(position='right'))

    # 设置下图标名称
    bar.set_global_opts(title_opts=opts.TitleOpts(title='北京2024年每月天气变化'))

    timeline.add(bar,f'{month}月')

#将设置好的图表保存为"weather.html"文件
timeline.render('weather.html')




