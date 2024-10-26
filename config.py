# coding: utf-8
if __name__ == '__main__':
    print('Please start main program craate.py!')

# Configure
configs = [
    {
        'name': 'DESKTOP-3EE05KD-redmi-rclone',  # 名称
        'baseFolder': r'R:\Android\data\tv.danmaku.bili\download',  # 缓存目录
        'targetFolder': r'E:\wyf9\music\bili',  # 目标目录
        'audioNameStr': '{v_num}_{v_avid}_{v_name}.mp3'  # 构建音频名称使用 ({v_num}: 编号; {v_avid}: av 号; {v_name}: 名称)
    },
    {}
    # 还可添加更多
]
