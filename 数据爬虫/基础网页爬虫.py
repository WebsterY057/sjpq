import requests
from bs4 import BeautifulSoup
import time
import csv


def basic_web_crawler(url, output_file='data.csv'):
    """
    基础网页爬虫示例 - 爬取网页标题和内容

    参数:
        url: 要爬取的网页URL
        output_file: 输出CSV文件名
    """

    # 设置请求头，模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        # 发送HTTP GET请求
        print(f"正在爬取: {url}")
        response = requests.get(url, headers=headers, timeout=10)

        # 检查请求是否成功
        response.raise_for_status()  # 如果状态码不是200，抛出异常

        # 设置编码（根据网页实际情况调整）
        response.encoding = 'utf-8'

        # 使用BeautifulSoup解析HTML内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 提取网页标题
        title = soup.title.string if soup.title else "无标题"
        print(f"网页标题: {title}")

        # 提取所有段落文本（根据实际网页结构调整选择器）
        paragraphs = soup.find_all('p')
        content = ' '.join([p.get_text().strip() for p in paragraphs])

        # 保存数据到CSV文件
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['标题', '内容摘要'])
            writer.writerow([title, content[:500]])  # 只保存前500个字符

        print(f"数据已保存到: {output_file}")

        # 礼貌性延迟，避免请求过于频繁
        time.sleep(2)

    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")


# 使用示例
if __name__ == "__main__":
    basic_web_crawler('https://httpbin.org/html')