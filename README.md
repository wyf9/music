# Music

My music library on GitHub

这也是一个测试github上能不能放音乐的库

> [!TIP]
> 如下所说, 本库 `/bili` 目录下的音频名称格式为 *编号_**AV号**_名称.mp3*, 如果看到自己喜欢的歌曲可以跳转 `https://bilibili.com/video/av[AV号]` 查看原视频~

## 本库唯一的代码

- `/create.py`

这是一个从手机 bilibili 缓存目录到此, 实现:
- 通过 AV/BV 号确定音频 (audio.m4s)
- 编号, ~~改名~~ 转换格式
- And more?

的脚本.

> [!TIP]
> 在使用前, 需要将手机存储通过 FTP + Rclone (或其他方式) 挂载到电脑本地盘符, 或直接在手机上运行 (前提有权限)

### Rclone

Rclone 启动命令参考 (**请保持命令行开启**)
```shell
rclone mount redmi:/  R: --cache-dir E:\rclone_tmp\redmi --vfs-cache-mode writes
```

替换以下字段:
- `redmi` : 使用 `rclone config` 创建远程时定义的名称
- `R:` 为挂载盘符
- `E:\rclone_tmp\redmi` 为缓存目录

### 寻找缓存目录

默认在 `/storage/emulated/0/Android/data/tv.danmaku.bili/download/`

> 在 Android 高版本中系统禁止第三方应用访问 `Android/data`, 可使用 MT 管理器 + Shizuku 来访问 (使用 MT 管理器的 `远程管理` 功能服务 FTP)

### 配置文件

`/config.py`

其中只有一个列表 `configs`, 每一项为字典 (如下):

```py
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
    # {
        # ...
    # }
    # 还可添加更多
]
```

### 使用

> 如需使用有颜色的输出, 请安装 `colorama`: `pip install colorama` 再运行.

> [!WARNING]
> 需安装 ffmpeg, 并添加到 PATH *(或直接移动到系统目录 **{Windows: `C:\Windows\[System32\]`, Linux: `[/usr]/bin/`}中)*** 中以直接调用: [ffmpeg-python GitHub](https://github.com/kkroening/ffmpeg-python#installing-ffmpeg)

按程序中的指引操作即可

> 在 Windows 中按时间顺序(先后)列出文件夹: `dir /A:D /O:D` (加 `/B` 只留文件名)

## 小脚本

`/.scripts/`

包含: 野生的自动点击脚本，用于完成在 [音乐播放软件](https://github.com/zhongyang219/MusicPlayer2) 中 *嵌入歌词/封面* 等操作

## Contact

如果对此库有 想法/建议, 可 [Issue](https://github.com/wyf9/music/issues/new) or [More contact](https://wyf9.top/#/contact)
