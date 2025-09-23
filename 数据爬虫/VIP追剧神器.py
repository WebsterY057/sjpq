# 导入必要的库
import tkinter  # GUI库
import webbrowser  # 网页浏览器控制库

class VIPVideoApp:
    def __init__(self, root):
        """初始化应用程序界面"""
        self.root = root
        self.root.title('VIP追剧神器')  # 设置窗口标题
        self.root.geometry('580x200')  # 设置窗口尺寸
        self.create_widgets()  # 调用控件创建方法

    def create_widgets(self):
        """创建界面控件"""
        # 视频链接提示标签
        label_movie_link = tkinter.Label(self.root, text='输入视频网址：')
        label_movie_link.place(x=20, y=30, width=100, height=30)  # 绝对位置布局

        # 视频链接输入框
        self.entry_movie_link = tkinter.Entry(self.root)
        self.entry_movie_link.place(x=125, y=30, width=260, height=30)

        # 清空按钮（绑定empty方法）
        button_movie_link = tkinter.Button(self.root, text='清空', command=self.empty)
        button_movie_link.place(x=400, y=30, width=50, height=30)

        # 视频平台快捷按钮
        button_movie1 = tkinter.Button(self.root, text='爱奇艺', command=self.open_iqy)
        button_movie1.place(x=25, y=80, width=80, height=40)

        button_movie2 = tkinter.Button(self.root, text='腾讯视频', command=self.open_tx)
        button_movie2.place(x=125, y=80, width=80, height=40)

        button_movie3 = tkinter.Button(self.root, text='优酷视频', command=self.open_yq)
        button_movie3.place(x=225, y=80, width=80, height=40)

        button_movie4 = tkinter.Button(self.root, text='芒果tv', command=self.open_mg)
        button_movie4.place(x=325, y=80, width=80, height=40)

        # VIP视频播放按钮（绑定play_video方法）
        button_movie = tkinter.Button(self.root, text='播放VIP视频', command=self.play_video)
        button_movie.place(x=425, y=80, width=125, height=40)

        # 红色警示标签
        text = '提示：本案例仅供学习使用，不可作为他用。'
        lab_remind = tkinter.Label(self.root, text=text, fg='red', font=('Arial', 15, 'bold'))
        lab_remind.place(x=125, y=150, width=400, height=30)

        # 允许窗口调整大小
        self.root.resizable()

    def open_iqy(self):
        """打开爱奇艺网站"""
        webbrowser.open('https://www.iqiyi.com')

    def open_tx(self):
        """打开腾讯视频网站"""
        webbrowser.open('https://v.qq.com')

    def open_yq(self):
        """打开优酷视频网站"""
        webbrowser.open('https://www.youku.com/')

    def open_mg(self):
        """打开优酷视频网站"""
        webbrowser.open('https://www.mgtv.com/')

    def play_video(self):
        """播放VIP视频（使用第三方解析服务）"""
        video = self.entry_movie_link.get()  # 获取输入框内容
        webbrowser.open('https://jx.xmflv.cc/?url=' + video)  # 拼接解析地址

    def empty(self):
        """清空输入框内容"""
        self.entry_movie_link.delete(0, 'end')  # 从第0个字符删除到末尾

if __name__ == '__main__':
    # 创建主窗口并启动程序
    root = tkinter.Tk()
    app = VIPVideoApp(root)
    root.mainloop()