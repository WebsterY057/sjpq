import requests
import json
import time
import pandas as pd
from datetime import datetime, timedelta


class APICrawlerWithAuth:
    """
    带认证的API数据爬虫 - 适用于需要登录或API密钥的网站
    """

    def __init__(self, base_url, auth_type='token', credentials=None):
        """
        初始化

        参数:
            base_url: API基础URL
            auth_type: 认证类型 ('token', 'basic', 'oauth2')
            credentials: 认证凭据
        """
        self.base_url = base_url
        self.auth_type = auth_type
        self.credentials = credentials or {}
        self.session = requests.Session()

        # 设置通用请求头
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        })

        # 根据认证类型设置认证
        self._setup_auth()

    def _setup_auth(self):
        """设置认证"""
        if self.auth_type == 'token':
            token = self.credentials.get('token')
            if token:
                self.session.headers['Authorization'] = f'Bearer {token}'

        elif self.auth_type == 'basic':
            username = self.credentials.get('username')
            password = self.credentials.get('password')
            if username and password:
                self.session.auth = (username, password)

    def make_request(self, endpoint, method='GET', params=None, data=None):
        """
        发送API请求

        参数:
            endpoint: API端点
            method: HTTP方法
            params: 查询参数
            data: 请求体数据
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            if method.upper() == 'GET':
                response = self.session.get(url, params=params, timeout=10)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, timeout=10)
            else:
                raise ValueError(f"不支持的HTTP方法: {method}")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"API请求失败: {e}")
            return None

    def paginated_crawl(self, endpoint, page_size=100, max_pages=None):
        """
        分页爬取数据

        参数:
            endpoint: API端点
            page_size: 每页大小
            max_pages: 最大页数
        """
        all_data = []
        page = 1

        while True:
            if max_pages and page > max_pages:
                break

            print(f"正在获取第 {page} 页数据...")

            params = {
                'page': page,
                'limit': page_size
            }

            data = self.make_request(endpoint, params=params)

            if not data or not isinstance(data, list) or len(data) == 0:
                print("没有更多数据")
                break

            all_data.extend(data)
            print(f"第 {page} 页获取完成，本页 {len(data)} 条，累计 {len(all_data)} 条")

            # 如果返回的数据少于请求的页大小，说明是最后一页
            if len(data) < page_size:
                break

            page += 1
            time.sleep(1)  # 礼貌延迟

        return all_data

    def incremental_crawl(self, endpoint, date_field='created_at', days=7):
        """
        增量爬取数据（按时间范围）

        参数:
            endpoint: API端点
            date_field: 日期字段名
            days: 爬取最近几天的数据
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        all_data = []
        current_date = start_date

        while current_date <= end_date:
            next_date = current_date + timedelta(days=1)

            params = {
                'start_date': current_date.strftime('%Y-%m-%d'),
                'end_date': next_date.strftime('%Y-%m-%d')
            }

            print(f"正在获取 {current_date.strftime('%Y-%m-%d')} 的数据...")

            data = self.make_request(endpoint, params=params)

            if data and isinstance(data, list):
                all_data.extend(data)
                print(f"获取到 {len(data)} 条数据")
            else:
                print("没有数据")

            current_date = next_date
            time.sleep(1)

        return all_data


# 使用示例
if __name__ == "__main__":
    # 示例：使用Token认证的API爬虫
    credentials = {
        'token': 'your_api_token_here'
    }

    crawler = APICrawlerWithAuth(
        base_url='https://api.example.com',
        auth_type='token',
        credentials=credentials
    )

    # 分页爬取数据
    # data = crawler.paginated_crawl('/v1/data', page_size=50, max_pages=10)

    # 增量爬取数据
    # data = crawler.incremental_crawl('/v1/records', days=30)