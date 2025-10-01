import requests
import json
import pandas as pd
import time
from datetime import datetime
import re


class SocialMediaCrawler:
    """
    社交媒体数据爬虫 - 爬取帖子、评论、用户信息等
    """

    def __init__(self, platform):
        self.platform = platform
        self.session = requests.Session()
        self.set_platform_headers(platform)

    def set_platform_headers(self, platform):
        """设置平台特定的请求头"""
        common_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        }

        if platform == 'weibo':
            common_headers.update({
                'Referer': 'https://weibo.com/',
                'X-Requested-With': 'XMLHttpRequest'
            })
        elif platform == 'twitter':
            common_headers.update({
                'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'x-twitter-client-language': 'zh-cn'
            })

        self.session.headers.update(common_headers)

    def crawl_user_posts(self, user_id, count=20):
        """
        爬取用户发布的帖子

        参数:
            user_id: 用户ID
            count: 帖子数量
        """
        posts = []

        if self.platform == 'weibo':
            # 微博API示例（需要根据实际情况调整）
            api_url = f"https://weibo.com/ajax/statuses/mymblog"
            params = {
                'uid': user_id,
                'page': 1,
                'feature': 0
            }

            try:
                response = self.session.get(api_url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    # 解析微博数据
                    for post_data in data.get('data', {}).get('list', [])[:count]:
                        post = self.parse_weibo_post(post_data)
                        if post:
                            posts.append(post)

                time.sleep(2)  # 礼貌延迟

            except Exception as e:
                print(f"爬取微博失败: {e}")

        elif self.platform == 'twitter':
            # Twitter API示例（需要API密钥）
            # 这里只是示例，实际使用时需要申请Twitter开发者账号
            pass

        return posts

    def crawl_hashtag_posts(self, hashtag, count=20):
        """
        爬取话题/标签下的帖子

        参数:
            hashtag: 话题标签
            count: 帖子数量
        """
        posts = []

        if self.platform == 'weibo':
            # 微博话题搜索
            search_url = "https://s.weibo.com/weibo"
            params = {
                'q': f'#{hashtag}#',
                'Refer': 'g'
            }

            try:
                response = self.session.get(search_url, params=params, timeout=10)
                response.encoding = 'utf-8'

                # 解析搜索结果页面
                # 这里需要根据实际页面结构解析
                # 可以使用BeautifulSoup或正则表达式

                time.sleep(2)

            except Exception as e:
                print(f"爬取微博话题失败: {e}")

        return posts

    def crawl_post_comments(self, post_id, max_comments=100):
        """
        爬取帖子评论

        参数:
            post_id: 帖子ID
            max_comments: 最大评论数量
        """
        comments = []

        if self.platform == 'weibo':
            # 微博评论API
            comments_url = f"https://weibo.com/ajax/statuses/buildComments"
            params = {
                'id': post_id,
                'is_show_bulletin': 2,
                'is_mix': 0,
                'count': 20,
                'uid': ''
            }

            page = 1
            while len(comments) < max_comments:
                try:
                    params['page'] = page
                    response = self.session.get(comments_url, params=params, timeout=10)

                    if response.status_code == 200:
                        data = response.json()
                        comment_list = data.get('data', [])

                        if not comment_list:
                            break

                        for comment_data in comment_list:
                            comment = self.parse_weibo_comment(comment_data)
                            if comment:
                                comments.append(comment)

                        print(f"第 {page} 页评论爬取完成，累计 {len(comments)} 条")

                        # 检查是否还有更多评论
                        if not data.get('maxPage', 0) or page >= data.get('maxPage', 0):
                            break

                        page += 1
                        time.sleep(1)

                    else:
                        break

                except Exception as e:
                    print(f"爬取评论失败: {e}")
                    break

        return comments[:max_comments]

    def parse_weibo_post(self, post_data):
        """解析微博帖子数据"""
        try:
            post = {
                'id': post_data.get('id'),
                'user': post_data.get('user', {}).get('screen_name'),
                'content': post_data.get('text_raw', ''),
                'publish_time': post_data.get('created_at'),
                'reposts_count': post_data.get('reposts_count', 0),
                'comments_count': post_data.get('comments_count', 0),
                'attitudes_count': post_data.get('attitudes_count', 0),
                'pics': [pic.get('url') for pic in post_data.get('pic_ids', [])],
                'video': post_data.get('page_info', {}).get('media_info', {}).get('stream_url_hd'),
                'topic': post_data.get('topic_struct', [])
            }
            return post
        except Exception as e:
            print(f"解析微博帖子失败: {e}")
            return None

    def parse_weibo_comment(self, comment_data):
        """解析微博评论数据"""
        try:
            comment = {
                'id': comment_data.get('id'),
                'user': comment_data.get('user', {}).get('screen_name'),
                'content': comment_data.get('text', ''),
                'publish_time': comment_data.get('created_at'),
                'like_count': comment_data.get('like_count', 0),
                'reply_count': comment_data.get('total_number', 0)
            }
            return comment
        except Exception as e:
            print(f"解析微博评论失败: {e}")
            return None


# 使用示例
if __name__ == "__main__":
    # 微博爬虫示例
    weibo_crawler = SocialMediaCrawler('weibo')

    # 爬取用户帖子
    # user_posts = weibo_crawler.crawl_user_posts('123456789', count=10)

    # 爬取帖子评论
    # post_comments = weibo_crawler.crawl_post_comments('123456789012345', max_comments=50)