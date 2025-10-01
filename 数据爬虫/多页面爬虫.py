import requests
from bs4 import BeautifulSoup
import time
import csv
import os


def multi_page_crawler(base_url, pages=5, output_dir='output'):
    """
    多页面爬虫示例 - 爬取分页内容

    参数:
        base_url: 基础URL，包含页码占位符
        pages: 要爬取的页数
        output_dir: 输出目录
    """

    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    all_data = []

    for page in range(1, pages + 1):
        try:
            # 构建每一页的URL（根据实际网站结构调整）
            url = base_url.format(page=page)
            print(f"正在爬取第 {page} 页: {url}")

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'

            soup = BeautifulSoup(response.text, 'html.parser')

            # 提取页面中的数据（这里以提取所有链接为例）
            links = soup.find_all('a', href=True)
            page_data = []

            for link in links:
                text = link.get_text().strip()
                href = link['href']
                if text and href.startswith('http'):  # 只保存有文本且是完整URL的链接
                    page_data.append({'text': text, 'url': href})

            all_data.extend(page_data)
            print(f"第 {page} 页爬取完成，找到 {len(page_data)} 个链接")

            # 延迟，避免请求过快
            time.sleep(1)

        except Exception as e:
            print(f"爬取第 {page} 页时出错: {e}")
            continue

    # 保存所有数据
    output_file = os.path.join(output_dir, 'all_pages_data.csv')
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['text', 'url'])
        writer.writeheader()
        writer.writerows(all_data)

    print(f"所有数据已保存到: {output_file}")
    print(f"总共爬取 {len(all_data)} 条数据")


# 使用示例
if __name__ == "__main__":
    # 示例URL，实际使用时需要替换为真实的分页URL格式
    base_url = "https://httpbin.org/links/{page}/10"  # 假设的分页URL格式
    multi_page_crawler(base_url, pages=3)