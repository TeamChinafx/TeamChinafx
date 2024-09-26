import os
import requests

def bytes_to_gb(size):
    return round(size / (1024 ** 3), 2)

game_names = {
    "1Z8W5NHUQb": "原神",
    "64kMb5iAWu": "崩坏：星穹铁道",
    "x6znKlJ0xK": "绝区零",
    "osvnlOc0S8": "崩坏3",
    "gopR6Cufr3": "Genshin Impact",
    "4ziysqXOQ8": "Honkai: Star Rail",
    "U5hbdsT9W7": "Zenless Zone Zero"
}

cn_order = ["1Z8W5NHUQb", "64kMb5iAWu", "x6znKlJ0xK", "osvnlOc0S8"]
global_order = ["gopR6Cufr3", "4ziysqXOQ8", "U5hbdsT9W7"]

api_urls = [
    ("https://hyp-api.mihoyo.com/hyp/hyp-connect/api/getGamePackages?game_ids[]=1Z8W5NHUQb&game_ids[]=64kMb5iAWu&game_ids[]=x6znKlJ0xK&game_ids[]=osvnlOc0S8&launcher_id=jGHBHlcOq1", "Games_CN.md", cn_order, "米哈游游戏下载信息", "此文档基于米哈游提供的API URL获取最新的游戏下载信息，如版本号、更新时间、下载链接等。此文档仅供参考，不代表米哈游或Hoyoverse的官方观点或立场。"),
    ("https://sg-hyp-api.hoyoverse.com/hyp/hyp-connect/api/getGamePackages?game_ids[]=gopR6Cufr3&game_ids[]=4ziysqXOQ8&game_ids[]=U5hbdsT9W7&launcher_id=VYTpXlbWo8", "README.md", global_order, "Hoyoverse Games Download Info", "This document is based on the API URL provided by Hoyoverse to get the latest download information of various games, such as version number, update time, download link, etc. This document is for reference only and does not represent the official views or positions of Hoyoverse.")
]

def get_and_write_data(api_urls):
    for api_url, md_file, order, title, description in api_urls:
        response = requests.get(api_url)
        data = response.json()

        md_title = f"# {title}\n\n"
        md_content = f"{description}\n\n"

        if data["retcode"] == 0 and data["message"] == "OK":
            game_packages = {pkg["game"]["id"]: pkg for pkg in data["data"]["game_packages"]}
            for game_id in order:
                if game_id in game_packages:
                    game_package = game_packages[game_id]
                    game = game_package["game"]
                    main = game_package["main"]
                    latest_version = main["major"]["version"]
                    game_name = game_names.get(game["id"], game["id"].upper())
                    
                    if "CN" in md_file:
                        md_content += f"## {game_name}\n\n"
                        md_content += f"- **版本号**: {latest_version}\n"
                    else:
                        md_content += f"## {game_name}\n\n"
                        md_content += f"- **Version number**: {latest_version}\n"
                    
                    game_pkgs = main["major"]["game_pkgs"]
                    if game_pkgs:
                        if "CN" in md_file:
                            md_content += "### 客户端\n\n"
                            md_content += "| 下载链接 | 包大小 | MD5 校验码 |\n"
                        else:
                            md_content += "### Client\n\n"
                            md_content += "| Download link | Package size | MD5 checksum |\n"
                        md_content += "| :---: | :---: | :---: |\n"
                        for pkg in game_pkgs:
                            md_content += f"| [{pkg['url'].split('/')[-1]}]({pkg['url']}) | {bytes_to_gb(int(pkg['size']))} GB | {pkg['md5']} |\n"
                        md_content += "\n"
                    
                    audio_pkgs = main["major"]["audio_pkgs"]
                    if audio_pkgs:
                        if "CN" in md_file:
                            md_content += "### 语音包\n\n"
                            md_content += "| 语言 | 下载链接 | 大小 | MD5 校验码 |\n"
                        else:
                            md_content += "### Voice Pack\n\n"
                            md_content += "| Language | Download link | Size | MD5 checksum |\n"
                        md_content += "| :---: | :---: | :---: | :---: |\n"
                        for audio in audio_pkgs:
                            md_content += f"| {audio['language']} | [{audio['url'].split('/')[-1]}]({audio['url']}) | {bytes_to_gb(int(audio['size']))} GB | {audio['md5']} |\n"
                        md_content += "\n"
                    
                    patches = main["patches"]
                    if patches:
                        client_diffs = [patch for patch in patches if patch["game_pkgs"]]
                        audio_diffs = [patch for patch in patches if patch["audio_pkgs"]]
                        
                        if client_diffs:
                            if "CN" in md_file:
                                md_content += "### 客户端差分文件\n\n"
                                md_content += "| 差分版本 | 下载链接 | 大小 | MD5 校验码 |\n"
                            else:
                                md_content += "### Client Diff files\n\n"
                                md_content += "| Diff version | Download link | Size | MD5 checksum |\n"
                            md_content += "| :---: | :---: | :---: | :---: |\n"
                            for patch in client_diffs:
                                for pkg in patch["game_pkgs"]:
                                    md_content += f"| {patch['version']}-{latest_version} | [{pkg['url'].split('/')[-1]}]({pkg['url']}) | {bytes_to_gb(int(pkg['size']))} GB | {pkg['md5']} |\n"
                            md_content += "\n"
                        
                        if audio_diffs:
                            if "CN" in md_file:
                                md_content += "### 语音差分文件\n\n"
                                md_content += "| 差分版本 | 下载链接 | 大小 | MD5 校验码 |\n"
                            else:
                                md_content += "### Audio Diff files\n\n"
                                md_content += "| Diff version | Download link | Size | MD5 checksum |\n"
                            md_content += "| :---: | :---: | :---: | :---: |\n"
                            for patch in audio_diffs:
                                for audio in patch["audio_pkgs"]:
                                    md_content += f"| {patch['version']}-{latest_version} | [{audio['url'].split('/')[-1]}]({audio['url']}) | {bytes_to_gb(int(audio['size']))} GB | {audio['md5']} |\n"
                            md_content += "\n"
        else:
            md_content += "请求失败，原因如下：\n\n" if "CN" in md_file else "Request failed, reason as follows:\n\n"
            md_content += data["message"] + "\n"

        with open(md_file, "w", encoding="utf-8") as md:
            md.write(md_title)
            md.write(md_content)
        print(f"The information obtained has been written to the markdown file: {md_file}")

get_and_write_data(api_urls)
