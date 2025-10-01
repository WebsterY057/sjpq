import requests
import os
import json
from bs4 import BeautifulSoup
import re


def extract_audio_urls(webpage_url, audio_extensions=None):
    """
    从网页中提取音频链接

    参数:
        webpage_url: 网页URL
        audio_extensions: 音频文件扩展名列表
    """

    if audio_extensions is None:
        audio_extensions = ['mp3', 'wav', 'm4a', 'aac', 'ogg', 'flac']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        response = requests.get(webpage_url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        audio_urls = []

        # 方法1: 查找audio标签
        audio_tags = soup.find_all('audio')
        for audio in audio_tags:
            src = audio.get('src')
            if src:
                audio_urls.append(src)

        # 方法2: 查找所有可能的音频文件链接
        all_links = soup.find_all('a', href=True)
        for link in all_links:
            href = link['href']
            if any(href.lower().endswith(ext) for ext in audio_extensions):
                audio_urls.append(href)

        # 方法3: 在脚本中查找音频URL（常见于动态加载的音频）
        script_tags = soup.find_all('script')
        for script in script_tags:
            if script.string:
                # 使用正则表达式查找音频URL
                urls = re.findall(r'https?://[^\s"\']*\.(?:mp3|wav|m4a)[^\s"\']*', script.string)
                audio_urls.extend(urls)

        # 转换为完整URL
        base_url = webpage_url.rsplit('/', 1)[0] + '/'
        full_audio_urls = []
        for url in audio_urls:
            if not url.startswith('http'):
                url = urljoin(base_url, url)
            full_audio_urls.append(url)

        return list(set(full_audio_urls))  # 去重

    except Exception as e:
        print(f"提取音频链接失败: {e}")
        return []


def download_audio(audio_url, output_dir='audio_downloads'):
    """
    下载单个音频文件

    参数:
        audio_url: 音频文件URL
        output_dir: 输出目录
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://www.example.com/'
    }

    try:
        # 获取文件名
        filename = audio_url.split('/')[-1]
        filepath = os.path.join(output_dir, filename)

        print(f"正在下载音频: {filename}")

        response = requests.get(audio_url, headers=headers, stream=True, timeout=30)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0

        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)

                    if total_size > 0:
                        progress = (downloaded_size / total_size) * 100
                        print(f"\r下载进度: {progress:.1f}%", end='', flush=True)

        print(f"\n音频下载完成: {filepath}")
        return filepath

    except Exception as e:
        print(f"音频下载失败: {e}")
        return None


def batch_download_audio(webpage_url, output_dir='audio_downloads'):
    """
    批量下载网页中的所有音频文件

    参数:
        webpage_url: 网页URL
        output_dir: 输出目录
    """

    print(f"开始从网页提取音频链接: {webpage_url}")
    audio_urls = extract_audio_urls(webpage_url)

    if not audio_urls:
        print("未找到音频链接")
        return

    print(f"找到 {len(audio_urls)} 个音频文件")

    success_count = 0
    for i, audio_url in enumerate(audio_urls):
        print(f"\n正在下载第 {i + 1}/{len(audio_urls)} 个音频")
        result = download_audio(audio_url, output_dir)
        if result:
            success_count += 1

    print(f"\n音频下载完成！成功下载 {success_count}/{len(audio_urls)} 个文件")


# 使用示例
if __name__ == "__main__":
    # 示例：批量下载网页中的音频
    # batch_download_audio('https://example.com/audio-page', 'my_audio_files')
    pass