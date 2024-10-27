# coding: utf-8

# import
from sys import exit as sys_exit
from os import path
from shutil import copy2
from config import configs
from utils import utils as utils_init
u = utils_init()
u.videoid = u.videoid_init(u)


def dl(num: int, avid: int, entry_path: str, audio_path: str, targetFolder: str, audioNameStr: str):

    # try get owner_name and title from json
    try:
        entry_json = u.load_json(entry_path)
        json_title = entry_json['title']
        json_owner = entry_json['owner_name']
        json_owner_id = entry_json['owner_id']

    except Exception as e:
        u.warning(f'Load data from json failed: {e}')
        return 1

    # video info and audio name
    u.info('[Video Info]')
    print(f'Title:  {json_title} [AVID {avid}]')
    print(f'Owner:  {json_owner} [UID {json_owner_id}]')
    print(f'Number: {num}')
    audio_name = u.input('Audio name (0 -> cancel): ')
    if audio_name == '0':
        return 1

    # build src, tgt and copy
    audio_filename = audioNameStr.format(v_num=num, v_avid=avid, v_name=audio_name)
    audio_file_path = path.join(targetFolder, audio_filename)
    u.debug('audio_filename: ' + audio_filename)
    u.debug('audio_file_path: ' + audio_file_path)
    copy_src = path.abspath(audio_path)
    copy_tgt = path.abspath(audio_file_path)
    u.info(f'Copy: {copy_src} -> {copy_tgt}')
    proc = u.input('Proceed? (*Y*/n)')
    if proc.lower() == 'n':
        u.info('Canceled.')
        return 1
    else:
        if path.exists(copy_tgt):
            proc2 = u.input(f'File {copy_tgt} already exists! Replace it? (y/*N*)')
            if proc2.lower() != 'y':
                u.info('Canceled.')
                return 1
        copy2(copy_src, copy_tgt)
        return 0


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
            baseFolder = str(conf['baseFolder'])
            targetFolder = str(conf['targetFolder'])
            audioNameStr = str(conf['audioNameStr'])
            u.info('[Config info]')
            print(f'Name: {conf["name"]}')
            print(f'BaseFolder: {baseFolder}')
            print(f'TargetFolder: {targetFolder}')
            print(f'audioNameStr: {audioNameStr}')
        except KeyboardInterrupt:
            raise
        except:
            u.warning('Invaild config number, or config format wrong!')
            continue
        break

    # input start number
    while True:
        num = u.input('Start number: ')
        try:
            num = int(num)
            break
        except:
            u.warning('Invaild number!')
            continue
    lastNum = -1

    # select mode
    while True:
        mode = u.input('Select mode (w-while, l-list): ')
        if mode.lower() == 'w' or mode.lower() == 'l':
            break
        else:
            u.warning('Invaild mode!')
            continue

    match mode:
        case 'w' | 'W':
            # main while
            u.info('While mode - input AV/BV id(s):')
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
                video_base_path = path.join(baseFolder, str(avid))
                u.debug('video_base_path: ' + video_base_path)
                entry_path, audio_path = u.find_json_m4s(video_base_path)  # 确保 avid 是字符串

                if not (entry_path and audio_path):
                    u.warning('Find entry.json and/or audio.m4s failed! Did you download this video?')
                    continue

                u.debug(f'Found entry.json at: {entry_path}')
                u.debug(f'Found audio.m4s at: {audio_path}')
                ret = dl(
                    avid=avid,
                    entry_path=entry_path,
                    audio_path=audio_path,
                    targetFolder=targetFolder,
                    audioNameStr=audioNameStr
                )
                if ret == 0:
                    num += 1

        case 'l' | 'L':
            # list mode
            u.tip('Input \'/s\' to save')
            u.info('List mode - Input AV/BV id(s):')

            # get avid list
            avlist = []
            while True:
                avbv = u.input(f'id #{len(avlist)+1}: ')
                if avbv.lower() == '/s':
                    break
                avid = u.videoid.convert(avbv)
                if not avid:
                    continue
                # get paths
                video_base_path = path.join(baseFolder, str(avid))
                u.debug('video_base_path: ' + video_base_path)
                entry_path, audio_path = u.find_json_m4s(video_base_path)  # 确保 avid 是字符串

                if not (entry_path and audio_path):
                    u.warning('Find entry.json and/or audio.m4s failed! Did you download this video?')
                    continue

                avlist += [[avid, entry_path, audio_path]]
                u.info(f'Added avid: {avid}')
                continue

            # for in ids
            for i in range(len(avlist)):
                u.info(f'- #{num} {i+1}/{len(avlist)}: AVID {avlist[i][0]}')
                ret = dl(
                    num=num,
                    avid=avlist[i][0],
                    entry_path=avlist[i][1],
                    audio_path=avlist[i][2],
                    targetFolder=targetFolder,
                    audioNameStr=audioNameStr
                )
                if ret == 0:
                    num += 1


# Main Error Handle
try:
    Main()
except KeyboardInterrupt:
    print('[Detected ^C/^Z or other stop signal]')
    u.info('Quitting.')
    sys_exit(1)

except Exception as e:
    print(f'[Main ERROR] Exception: {e}')
    raise
