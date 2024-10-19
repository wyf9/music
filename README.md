# Music

My Music library on GitHub

这也是一个测试github上能不能放音乐的库

## 本库唯一的代码

- `/create.py`

这是一个从手机 bilibili 缓存目录到此, 实现:
- 通过 AV/BV 号确定音频 (audio.m4s)
- 编号, 改名
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
```

### 使用

如需使用有颜色的输出, 请安装 `colorama`: `pip install colorama` 再运行