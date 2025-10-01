from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import csv


def dynamic_content_crawler(url, output_file='dynamic_data.csv'):
    """
    动态内容爬虫示例 - 处理JavaScript渲染的页面

    参数:
        url: 要爬取的网页URL
        output_file: 输出文件名
    """

    # 配置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 无头模式，不显示浏览器窗口
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # 初始化浏览器驱动（需要下载对应浏览器的driver）
    driver = webdriver.Chrome(options=chrome_options)

    try:
        print(f"正在访问: {url}")
        driver.get(url)

        # 等待页面加载完成
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # 模拟滚动加载（针对需要滚动加载内容的页面）
        print("模拟滚动加载...")
        last_height = driver.execute_script("return document.body.scrollHeight")

        for i in range(3):  # 滚动3次
            # 滚动到页面底部
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # 等待内容加载

            # 计算新的滚动高度，如果没有变化则停止
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # 提取动态加载的内容
        print("提取页面内容...")

        # 获取页面标题
        title = driver.title

        # 提取所有文本内容（根据实际需求调整选择器）
        elements = driver.find_elements(By.TAG_NAME, "p")
        content = [elem.text for elem in elements if elem.text.strip()]

        # 提取所有图片
        images = driver.find_elements(By.TAG_NAME, "img")
        image_urls = [img.get_attribute('src') for img in images if img.get_attribute('src')]

        # 保存数据
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['标题', '内容段落数', '图片数', '内容示例'])
            writer.writerow([title, len(content), len(image_urls), content[0] if content else ''])

        print(f"数据已保存到: {output_file}")
        print(f"提取到 {len(content)} 个段落，{len(image_urls)} 张图片")

    except Exception as e:
        print(f"爬取过程中出错: {e}")
    finally:
        # 关闭浏览器
        driver.quit()
        print("浏览器已关闭")


# 使用示例
if __name__ == "__main__":
    dynamic_content_crawler('https://httpbin.org/html')