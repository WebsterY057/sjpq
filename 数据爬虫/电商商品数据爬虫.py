import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import random


class EcommerceCrawler:
    """
    电商商品数据爬虫 - 爬取商品信息、价格、评论等
    """

    def __init__(self, base_delay=1, max_delay=3):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        })
        self.base_delay = base_delay
        self.max_delay = max_delay

    def random_delay(self):
        """随机延迟，避免被封IP"""
        delay = random.uniform(self.base_delay, self.max_delay)
        time.sleep(delay)

    def extract_product_info(self, product_url):
        """
        提取单个商品信息

        参数:
            product_url: 商品页面URL
        """
        try:
            print(f"正在爬取商品: {product_url}")

            response = self.session.get(product_url, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'

            soup = BeautifulSoup(response.text, 'html.parser')

            product_info = {
                'url': product_url,
                'title': self._extract_title(soup),
                'price': self._extract_price(soup),
                'original_price': self._extract_original_price(soup),
                'rating': self._extract_rating(soup),
                'review_count': self._extract_review_count(soup),
                'description': self._extract_description(soup),
                'specifications': self._extract_specifications(soup),
                'images': self._extract_images(soup),
                'stock_status': self._extract_stock_status(soup),
                'timestamp': pd.Timestamp.now()
            }

            self.random_delay()
            return product_info

        except Exception as e:
            print(f"爬取商品失败: {e}")
            return None

    def extract_products_from_listing(self, listing_url, max_products=20):
        """
        从商品列表页提取多个商品信息

        参数:
            listing_url: 商品列表页URL
            max_products: 最大商品数量
        """
        try:
            print(f"正在爬取商品列表: {listing_url}")

            response = self.session.get(listing_url, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'

            soup = BeautifulSoup(response.text, 'html.parser')

            # 提取商品链接（根据实际网站结构调整选择器）
            product_links = []

            # 方法1: 查找商品卡片中的链接
            product_cards = soup.find_all('div', class_=lambda x: x and 'product' in x.lower())
            for card in product_cards[:max_products]:
                link = card.find('a', href=True)
                if link:
                    href = link['href']
                    if not href.startswith('http'):
                        href = 'https://example.com' + href  # 根据实际情况调整
                    product_links.append(href)

            # 方法2: 直接查找所有商品链接
            if not product_links:
                all_links = soup.find_all('a', href=True)
                for link in all_links[:max_products * 2]:  # 多找一些链接
                    href = link['href']
                    if '/product/' in href or '/item/' in href:
                        if not href.startswith('http'):
                            href = 'https://example.com' + href
                        product_links.append(href)

            # 去重
            product_links = list(set(product_links))[:max_products]

            print(f"找到 {len(product_links)} 个商品链接")

            # 爬取每个商品详情
            products_data = []
            for link in product_links:
                product_info = self.extract_product_info(link)
                if product_info:
                    products_data.append(product_info)

                if len(products_data) >= max_products:
                    break

            return products_data

        except Exception as e:
            print(f"爬取商品列表失败: {e}")
            return []

    def extract_reviews(self, product_url, max_reviews=50):
        """
        提取商品评论

        参数:
            product_url: 商品页面URL
            max_reviews: 最大评论数量
        """
        # 这里需要根据具体网站结构实现
        # 有些网站评论在商品页面内，有些需要通过API获取

        reviews = []

        try:
            # 示例：从商品页面提取评论
            response = self.session.get(product_url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # 查找评论元素（根据实际网站结构调整）
            review_elements = soup.find_all('div', class_=lambda x: x and 'review' in x.lower())

            for review_element in review_elements[:max_reviews]:
                review = {
                    'author': self._extract_review_author(review_element),
                    'rating': self._extract_review_rating(review_element),
                    'date': self._extract_review_date(review_element),
                    'content': self._extract_review_content(review_element),
                    'verified': self._extract_review_verified(review_element)
                }
                reviews.append(review)

        except Exception as e:
            print(f"提取评论失败: {e}")

        return reviews

    # 以下是根据具体网站结构实现的辅助方法
    def _extract_title(self, soup):
        # 实现提取商品标题的逻辑
        title_element = soup.find('h1') or soup.find('title')
        return title_element.get_text().strip() if title_element else "未知标题"

    def _extract_price(self, soup):
        # 实现提取当前价格的逻辑
        # 查找价格相关的元素
        return "未知价格"

    def _extract_original_price(self, soup):
        # 实现提取原价的逻辑
        return ""

    def _extract_rating(self, soup):
        # 实现提取评分的逻辑
        return 0.0

    def _extract_review_count(self, soup):
        # 实现提取评论数量的逻辑
        return 0

    def _extract_description(self, soup):
        # 实现提取商品描述的逻辑
        return ""

    def _extract_specifications(self, soup):
        # 实现提取商品规格的逻辑
        return {}

    def _extract_images(self, soup):
        # 实现提取商品图片的逻辑
        return []

    def _extract_stock_status(self, soup):
        # 实现提取库存状态的逻辑
        return "未知"

    def _extract_review_author(self, review_element):
        return "匿名用户"

    def _extract_review_rating(self, review_element):
        return 5.0

    def _extract_review_date(self, review_element):
        return ""

    def _extract_review_content(self, review_element):
        return ""

    def _extract_review_verified(self, review_element):
        return False


# 使用示例
if __name__ == "__main__":
    crawler = EcommerceCrawler(base_delay=1, max_delay=3)

    # 爬取商品列表
    # products = crawler.extract_products_from_listing(
    #     'https://example.com/products/category',
    #     max_products=10
    # )

    # 保存到Excel
    # if products:
    #     df = pd.DataFrame(products)
    #     df.to_excel('products_data.xlsx', index=False)
    #     print(f"商品数据已保存到 products_data.xlsx")