import requests
import json
import csv
import time


def api_crawler(api_url, params=None, headers=None, output_file='api_data.csv'):
    """
    API数据爬虫示例 - 直接调用API接口获取数据

    参数:
        api_url: API接口URL
        params: 请求参数
        headers: 请求头
        output_file: 输出文件名
    """

    # 默认请求头
    default_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json'
    }

    # 合并请求头
    if headers:
        default_headers.update(headers)

    try:
        print(f"正在调用API: {api_url}")

        # 发送API请求
        response = requests.get(
            api_url,
            params=params or {},
            headers=default_headers,
            timeout=10
        )

        # 检查请求状态
        response.raise_for_status()

        # 解析JSON响应
        data = response.json()

        print(f"API响应成功，数据类型: {type(data)}")

        # 处理数据（根据实际API响应结构调整）
        if isinstance(data, list):
            # 如果响应是列表
            processed_data = data
        elif isinstance(data, dict):
            # 如果响应是字典，提取其中的数据
            # 这里假设数据在'data'或'results'字段中，根据实际情况调整
            processed_data = data.get('data', []) or data.get('results', [])
            if not processed_data:
                processed_data = [data]  # 如果没有找到数据字段，将整个响应作为一条记录
        else:
            processed_data = [{'raw_data': str(data)}]

        # 保存数据到CSV
        if processed_data:
            # 提取所有可能的字段名
            fieldnames = set()
            for item in processed_data:
                if isinstance(item, dict):
                    fieldnames.update(item.keys())

            fieldnames = list(fieldnames)

            with open(output_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()

                for item in processed_data:
                    if isinstance(item, dict):
                        writer.writerow(item)
                    else:
                        # 如果数据不是字典，将其转换为字典
                        writer.writerow({'value': item})

            print(f"数据已保存到: {output_file}")
            print(f"共保存 {len(processed_data)} 条记录，包含 {len(fieldnames)} 个字段")
        else:
            print("没有找到可保存的数据")

    except requests.exceptions.RequestException as e:
        print(f"API请求错误: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")


# 使用示例
if __name__ == "__main__":
    # 示例：调用一个公共API
    api_url = "https://api.github.com/users/octocat/repos"
    api_crawler(api_url)