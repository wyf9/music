# coding: utf-8
if __name__ == '__main__':
    print('Please start main program craate.py!')

# Global config
config = {
    'needProceed': False,  # bool: 复制文件时确认
    'audioNameStr': '{v_num}_{v_avid}_{v_name}.mp3'  # str: 构建音频文件名使用 ({v_num}: 编号; {v_avid}: av 号; {v_name}: 名称)
}

# Config list
configs = [
    {
        'name': 'DESKTOP-3EE05KD-redmi-rclone',  # str: 名称
        'baseFolder': r'R:\Android\data\tv.danmaku.bili\download',  # str: 缓存目录
        'targetFolder': r'E:\wyf9\music\bili',  # str: 目标目录
    },
    {
        'name': 'wyf9Desktop-redmi-rclone',  # str: 名称
        'baseFolder': r'/media/redmi/Android/data/tv.danmaku.bili/download',  # str: 缓存目录
        'targetFolder': r'/sync/music/bili',  # str: 目标目录
    },
    # {
    # ...
    # }
    # 还可添加更多
]
