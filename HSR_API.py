import os
import shutil
import random
import requests

def bytes_to_gb(size):
    return round(size / (1024 ** 3), 2)

api_list = [
    ("https://api-launcher-static.mihoyo.com/hkrpg_cn/mdk/launcher/api/resource?key=6KcVuOkbcqjJomjZ&launcher_id=33", "CN.md"),
    ("https://hkrpg-launcher-static.hoyoverse.com/hkrpg_global/mdk/launcher/api/resource?key=vplOVX8Vn7cwG8yb&launcher_id=35", "README.md")
]

def get_and_write_data(api_url, md_file):
    response = requests.get(api_url)
    data = response.json()

    md_title = "# HSR Download Info\n\n"

    md_content = ""

    if data["retcode"] == 0 and data["message"] == "OK":
        md_content += "This document is based on the api url provided by miHoYo to get the lastest download informations of HSR, such as version number, update time, download link, etc. This document is for reference only and does not represent the official views or positions of miHoYo or hoyoverse.\n\n"
        game_latest = data["data"]["game"]["latest"]
        md_content += "## Latest version\n\n"
        md_content += "- **Version number**：" + game_latest["version"] + "\n"
        md_content += "- **Size**：" + str(bytes_to_gb(int(game_latest["size"]))) + " GB\n"
        md_content += "- **MD5 checksum**：" + game_latest["md5"] + "\n"
        md_content += "- **Entry file**：" + game_latest["entry"] + "\n\n"
        md_content += "## Client\n\n"
        md_content += "| Download link | Package size | MD5 checksum |\n"
        md_content += "| :---: | :---: | :---: |\n"
        md_content += "| [" + game_latest["path"].split("/")[-1] + "](" + game_latest["path"] + ") | " + str(bytes_to_gb(int(game_latest["package_size"]))) + " GB | " + game_latest["md5"] + " |\n"
        md_content += "\n"
        voice_packs = game_latest["voice_packs"]
        md_content += "## Voice Pack\n\n"
        md_content += "| Language | Download link | Size | Package size | MD5 checksum |\n"
        md_content += "| :---: | :---: | :---: | :---: | :---: |\n"
        for voice_pack in voice_packs:
            md_content += "| " + voice_pack["language"] + " | [" + voice_pack["language"] + "_" + version + ".zip](" + voice_pack["path"] + ") | " + str(bytes_to_gb(int(voice_pack["size"]))) + " GB | " + str(bytes_to_gb(int(voice_pack["package_size"]))) + " GB | " + voice_pack["md5"] + " |\n" 
        md_content += "\n"
        diffs = data["data"]["game"]["diffs"]
        md_content += "## Client Diff files\n\n"
        md_content += "| Diff version | Download link | Size | Package size | MD5 checksum |\n"
        md_content += "| :---: | :---: | :---: | :---: | :---: |\n"
        for diff in diffs:
            md_content += "| " + diff["version"] + "-" + game_latest["version"] +" | [" + diff["name"] + "](" + diff["path"] + ") | " + str(bytes_to_gb(int(diff["size"]))) + " GB | " + str(bytes_to_gb(int(diff["package_size"]))) + " GB | " + diff["md5"] + " |\n" 
        md_content += "\n"
        for diff in diffs:
            voice_packs = diff["voice_packs"]
            md_content += "### Voice Pack  " + diff["version"] + "-" + game_latest["version"] + " Diff\n\n"
            md_content += "| Language | Download link | Size | Package size | MD5 checksum |\n"
            md_content += "| :---: | :---: | :---: | :---: | :---: |\n"
            for voice_pack in voice_packs:
                md_content += "| " + voice_pack["language"] + " | [" + voice_pack["name"] + "](" + voice_pack["path"] + ") | " + str(bytes_to_gb(int(voice_pack["size"]))) + " GB | " + str(bytes_to_gb(int(voice_pack["package_size"]))) + " GB | " + voice_pack["md5"] + " |\n" 
            md_content += "\n"
        if "pre_download_game" in data["data"] and data["data"]["pre_download_game"] is not None:
            pre_download_game = data["data"]["pre_download_game"]["latest"]
            md_content += "# Pre-Downloads\n\n"
            md_content += "- **Version number**：" + pre_download_game["version"] + "\n"
            md_content += "- **Full Size**：" + str(bytes_to_gb(int(pre_download_game["size"]))) + " GB (Client + All Languages Voice Packs Unpacked Size)\n" 
            md_content += "- **MD5 checksum**：" + pre_download_game["md5"] + "\n"
            md_content += "- **Entry file**：" + pre_download_game["entry"] + "\n\n"
            segments = pre_download_game["segments"]
            md_content += "## Pre-Download Client\n\n"
            md_content += "| Download link | Package size | MD5 checksum |\n"
            md_content += "| :---: | :---: | :---: |\n"
            md_content += "| [" + pre_download_game["path"].split("/")[-1] + "](" + pre_download_game["path"] + ") | " + str(bytes_to_gb(int(pre_download_game["package_size"]))) + " GB | " + pre_download_game["md5"] + " |\n" 
            md_content += "\n"
            voice_packs = pre_download_game["voice_packs"]
            md_content += "## Pre-Download Voice Pack\n\n"
            md_content += "| Language | Download link | Size | Package size | MD5 checksum |\n"
            md_content += "| :---: | :---: | :---: | :---: | :---: |\n"
            for voice_pack in voice_packs:
                md_content += "| " + voice_pack["language"] + " | [" + voice_pack["language"] + "_" + pre_download_game["version"] + ".zip](" + voice_pack["path"] + ") | " + str(bytes_to_gb(int(voice_pack["size"]))) + " GB | " + str(bytes_to_gb(int(voice_pack["package_size"]))) + " GB | " + voice_pack["md5"] + " |\n" 
            md_content += "\n"

            diffs = data["data"]["pre_download_game"]["diffs"]
            md_content += "## Pre-Download Client Diff files\n\n"
            md_content += "| Diff version | Download link | Size | Package size | MD5 checksum |\n"
            md_content += "| :---: | :---: | :---: | :---: | :---: |\n"
            for diff in diffs:
                md_content += "| " + diff["version"] + "-" + pre_download_game["version"] +" | [" + diff["name"] + "](" + diff["path"] + ") | " + str(bytes_to_gb(int(diff["size"]))) + " GB | " + str(bytes_to_gb(int(diff["package_size"]))) + " GB | " + diff["md5"] + " |\n" 
            md_content += "\n"
            for diff in diffs:
                voice_packs = diff["voice_packs"]
                md_content += "### Pre-Download Voice Pack  " + diff["version"] + "-" + pre_download_game["version"] + " Diff\n\n"
                md_content += "| Language | Download link | Size | Package size | MD5 checksum |\n"
                md_content += "| :---: | :---: | :---: | :---: | :---: |\n"
                for voice_pack in voice_packs:
                    md_content += "| " + voice_pack["language"] + " | [" + voice_pack["name"] + "](" + voice_pack["path"] + ") | " + str(bytes_to_gb(int(voice_pack["size"]))) + " GB | " + str(bytes_to_gb(int(voice_pack["package_size"]))) + " GB | " + voice_pack["md5"] + " |\n" 
                md_content += "\n"
        else:
            print("Pre-Download is not available now")
    else:
        md_content += "Request failed, reason as follows:\n\n"
        md_content += data["message"] + "\n"

    md = open(md_file, "a", encoding="utf-8")

    md.write(md_title)
    md.write(md_content)
    md.close()
    print("The information obtained has been written to the markdown file：" + md_file)

for api_url, md_file in api_list:
    response = requests.get(api_url)
    data = response.json()
    version = data["data"]["game"]["latest"]["version"]

    get_and_write_data(api_url, md_file)