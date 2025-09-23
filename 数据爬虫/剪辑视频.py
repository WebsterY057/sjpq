#剪辑B站视频代码
#第三方模块专门做视频剪辑  moviepy

import moviepy
"""
步骤：
1、先加载素材文件，加载视频素材文件，VideoFileClip()
2、加载音频素材文件，AudioFileClip()
3、将音频素材合并到视频素材里面去
4、最终将素材视频导出
"""

vedio = moviepy.VideoFileClip('B站视频.mp4')
audio = moviepy.AudioFileClip('B站音频.mp3')

#with_audio
#形成新的素材文件
file = vedio.with_audio(audio)

#write_videofile 导出最终素材
file.write_videofile('新宝岛.mp4')