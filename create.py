# coding: utf-8

# import
from sys import exit as sys_exit
from os.path import join
from config import configs
from utils import utils as utils_init
u = utils_init()
u.videoid = u.videoid_init(u)


def Main():
    # select config
    u.info('Configs list:')
    print('[0] - quit')
    for n in range(len(configs)):
        print(f'[{n + 1}] - {configs[n]}')
    while True:
        try:
            inp = int(u.input('Select by number: '))
            if inp == 0:
                u.info('Quitting.')
                return 0
            conf = configs[inp - 1]
            baseFolder = conf['baseFolder']
            TargetFolder = conf['targetFolder']
            audioNameStr = conf['audioNameStr']
            u.info('Selected config:')
            u.info(f'Name: {conf["name"]}')
            u.info(f'BaseFolder: {baseFolder}')
            u.info(f'TargetFolder: {TargetFolder}')
            u.info(f'audioNameStr: {audioNameStr}')
        except KeyboardInterrupt:
            raise
        except:
            u.warning('Invaild config number, or config format wrong!')
            continue
        break

    # main while
    num = u.input('Start number: ')
    lastNum = -1
    while True:
        if num != lastNum:
            u.info(f'----- #{num}')
            lastNum = num

        # get av id
        avbv = u.input('AV/BV id: ')
        avid = u.videoid.convert(avbv)
        if not avid:
            continue
        
        # get paths
        video_base_path = join(baseFolder, str(avid))
        u.debug(video_base_path)
        entry_path, audio_path = u.find_json_m4s(video_base_path)  # 确保 avid 是字符串

        if not (entry_path and audio_path):
            u.warning('Find entry.json and/or audio.m4s failed! Did you download this video?')
            continue

        u.debug(f'Found entry.json at: {entry_path}')
        u.debug(f'Found audio.m4s at: {audio_path}')

        # try get owner_name and title from json\
        entry_json = u.load_json(entry_path)
        u.debug(entry_json)


# Main Error Handle
try:
    sys_exit(Main())
except KeyboardInterrupt:
    print('[Detected ^C/^Z or other stop signal]')
    u.info('Quitting.')

except Exception as e:
    print(f'[Main ERROR] Exception: {e}')
    raise
