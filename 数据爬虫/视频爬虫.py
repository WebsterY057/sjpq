import requests
import os
import re
import subprocess
from urllib.parse import urljoin, urlparse
import concurrent.futures
import m3u8


def download_video_m3u8(m3u8_url, output_file='video.mp4', temp_dir='temp_ts'):
    """
    m3u8视频流下载器 - 下载并合并ts片段

    参数:
        m3u8_url: m3u8文件的URL
        output_file: 输出视频文件名
        temp_dir: 临时ts文件存储目录
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://www.example.com/'  # 根据实际情况设置Referer
    }

    # 创建临时目录
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    try:
        print(f"正在解析m3u8文件: {m3u8_url}")

        # 解析m3u8文件
        response = requests.get(m3u8_url, headers=headers, timeout=10)
        response.raise_for_status()

        # 解析m3u8内容
        m3u8_content = response.text
        playlist = m3u8.loads(m3u8_content)

        # 获取基础URL（用于构建完整的ts文件URL）
        base_url = m3u8_url.rsplit('/', 1)[0] + '/'

        ts_urls = []
        for segment in playlist.segments:
            ts_url = segment.uri
            # 如果ts_url不是完整URL，则拼接基础URL
            if not ts_url.startswith('http'):
                ts_url = urljoin(base_url, ts_url)
            ts_urls.append(ts_url)

        print(f"找到 {len(ts_urls)} 个ts片段")

        # 下载所有ts片段
        def download_ts(ts_url, index):
            try:
                ts_response = requests.get(ts_url, headers=headers, timeout=30)
                ts_response.raise_for_status()

                ts_filename = os.path.join(temp_dir, f'segment_{index:05d}.ts')
                with open(ts_filename, 'wb') as f:
                    f.write(ts_response.content)

                print(f"下载完成: {index + 1}/{len(ts_urls)}")
                return ts_filename
            except Exception as e:
                print(f"下载片段 {index} 失败: {e}")
                return None

        # 使用线程池并发下载（控制并发数避免被封IP）
        ts_files = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(download_ts, ts_url, i): i for i, ts_url in enumerate(ts_urls)}

            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    ts_files.append(result)

        # 按顺序合并ts文件
        print("正在合并ts文件...")
        with open(output_file, 'wb') as merged:
            for ts_file in sorted(ts_files):
                with open(ts_file, 'rb') as f:
                    merged.write(f.read())

        # 清理临时文件
        for ts_file in ts_files:
            os.remove(ts_file)
        os.rmdir(temp_dir)

        print(f"视频下载完成: {output_file}")

    except Exception as e:
        print(f"视频下载失败: {e}")


def download_direct_video(video_url, output_file='video.mp4'):
    """
    直接下载视频文件（适用于mp4等直接链接）

    参数:
        video_url: 视频直链URL
        output_file: 输出文件名
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://www.example.com/'
    }

    try:
        print(f"正在下载视频: {video_url}")

        # 流式下载大文件
        response = requests.get(video_url, headers=headers, stream=True, timeout=30)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0

        with open(output_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)

                    # 显示下载进度
                    if total_size > 0:
                        progress = (downloaded_size / total_size) * 100
                        print(f"\r下载进度: {progress:.1f}%", end='', flush=True)

        print(f"\n视频下载完成: {output_file}")

    except Exception as e:
        print(f"视频下载失败: {e}")


# 使用示例
if __name__ == "__main__":
    # 示例：下载直接链接视频
    # download_direct_video('https://example.com/video.mp4', 'my_video.mp4')

    # 示例：下载m3u8视频
    # download_video_m3u8('https://example.com/playlist.m3u8', 'my_video.mp4')
    pass