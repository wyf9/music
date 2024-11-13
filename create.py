# coding: utf-8

# import
from sys import exit as sys_exit
from os import path
# from shutil import copy2 # unused
from config import config, configs
from utils import utils as utils_init
u = utils_init()
u.videoid = u.videoid_init(u)


def cp(num: int, avid: int, audio_path: str, targetFolder: str, audioNameStr: str, needProceed: bool, audio_name: str):
    '''
    Copy and convert audio

    :param num: number, will replace `{v_num}` in `audioNameStr`
    :param avid: Video's AVID, will replace `{v_avid}` in `audioNameStr`
    :param audio_path: Source audio path (`audio.m4s`)
    :param targetFolder: target folder to place output (`config.py` / `configs[x]['targetFolder']`)
    :param audioNameStr: `config.py` / `config['audioNameStr']`
    :param needProceed: Control `Proceed? (Y/n)` prompt (`config.py` / `config['needProceed']`)
    :param audio_name: audio's name, will replace `{v_name}` in `audioNameStr`
    '''
    # build src, tgt and copy
    audio_filename = audioNameStr.format(v_num=num, v_avid=avid, v_name=audio_name)
    audio_file_path = path.join(targetFolder, audio_filename)
    u.debug('audio_filename: ' + audio_filename)
    u.debug('audio_file_path: ' + audio_file_path)
    copy_src = path.abspath(audio_path)
    copy_tgt = path.abspath(audio_file_path)
    u.info(f'Copy: {copy_src} -> {copy_tgt}')
    if needProceed:
        proc = u.input('Proceed? (Y/n)')
        if proc.lower() == 'n':
            u.info('Canceled.')
            return 1
    if path.exists(copy_tgt):
        proc2 = u.input(f'File {copy_tgt} already exists! Replace it? (Y/n)')
        if proc2.lower() == 'n':
            u.info('Canceled.')
            return 1
    # copy2(copy_src, copy_tgt) # old
    try:
        u.convert_m4a_to_mp3(copy_src, copy_tgt)
    except:
        u.error('Convert Error!')
        return 114514
    return 0


def info(entry_path: str, num: int, avid: int, audio_name: str = None):
    '''
    Show video information, and get `audio_name` from user input

    :param entry_path: `entry.json`'s path
    :param num: number, will replace `{v_num}` in `audioNameStr`
    :param avid: Video's AVID, will replace `{v_avid}` in `audioNameStr`
    :param audio_name: audio's name, will replace `{v_name}` in `audioNameStr` *(optional, if not `None`, will skip user input)*
    '''
    # try get owner_name and title from json
    try:
        entry_json = u.load_json(entry_path)
        json_title = entry_json['title']
        json_part = entry_json['page_data']['part']
        json_cid = entry_json['page_data']['cid']
        json_owner = entry_json['owner_name']
        json_owner_id = entry_json['owner_id']

    except Exception as e:
        u.warning(f'Load data from json failed: {e}')
        return None

    # video info and audio name
    u.info('[Video Info]')
    print(f'Title:  {json_title} [AVID {avid}]')
    print(f'Part:  {json_part} [CID {json_cid}]')
    print(f'Owner:  {json_owner} [UID {json_owner_id}]')
    print(f'Number: {num}')
    if audio_name == None:
        audio_name = u.input('Audio name (0 -> cancel): ')
    else:
        print(f'Name: {audio_name}')
    if audio_name == '0':
        return None
    return audio_name


def Main():
    '''
    Main program
    '''
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
            needProceed = bool(config['needProceed'])
            audioNameStr = str(config['audioNameStr'])
            conf = configs[inp - 1]
            baseFolder = str(conf['baseFolder'])
            targetFolder = str(conf['targetFolder'])
            u.info('[Config info]')
            print(f'needProceed: {needProceed}')
            print(f'audioNameStr: {audioNameStr}')
            print(f'Name: {conf["name"]}')
            print(f'BaseFolder: {baseFolder}')
            print(f'TargetFolder: {targetFolder}')
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
        mode = u.input('Select mode (w-while, l-list, ll-list[av/bv id first, names after]): ')
        if mode.lower() == 'w' or mode.lower() == 'l' or mode.lower() == 'll':
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
                audio_name = info(
                    entry_path=entry_path,
                    avid=avid,
                    num=num
                )
                if not audio_name:
                    continue
                ret = cp(
                    num=num,
                    avid=avid,
                    # entry_path=entry_path,
                    audio_path=audio_path,
                    targetFolder=targetFolder,
                    audioNameStr=audioNameStr,
                    needProceed=needProceed,
                    audio_name=audio_name
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

                # audio_name = u.input('Input video name: ')
                audio_name = info(
                    entry_path=entry_path,
                    avid=avid,
                    num=num
                )
                if not audio_name:
                    continue
                avlist += [(avid, entry_path, audio_path, audio_name)]
                u.info(f'Added avid: {avid}')
                continue

            # for in ids
            for i in range(len(avlist)):
                u.info(f'- #{num} {i+1}/{len(avlist)}: AVID {avlist[i][0]} - Name {avlist[i][3]}')
                ret = cp(
                    num=num,
                    avid=avlist[i][0],
                    # entry_path=avlist[i][1],
                    audio_path=avlist[i][2],
                    targetFolder=targetFolder,
                    audioNameStr=audioNameStr,
                    needProceed=needProceed,
                    audio_name=avlist[i][3]
                )
                if ret == 0:
                    num += 1
            u.info('Finished!')

        case 'll' | 'LL':
            # list mode (av/bv id first, name after)
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

                avlist += [(num, avid, entry_path, audio_path)]  # , audio_name]]
                u.info(f'Added avid: {avid}')
                num += 1
                continue

            # get names list
            u.info('List mode - Input audio name(s):')
            for i in range(len(avlist)):
                localnum, avid, entry_path, audio_path = avlist[i]
                while True:
                    audio_name = info(
                        entry_path=entry_path,
                        avid=avid,
                        num=localnum
                    )
                    if not audio_name:
                        continue
                    else:
                        break
                avlist[i] = localnum, avid, entry_path, audio_path, audio_name
                u.info(f'Added name for avid: {avid} - {audio_name}')

            # for in ids
            for i in range(len(avlist)):
                u.info(f'- #{avlist[i][0]} {i+1}/{len(avlist)}: AVID {avlist[i][1]} - Name {avlist[i][4]}')
                ret = cp(
                    num=avlist[i][0],
                    avid=avlist[i][1],
                    # entry_path=avlist[i][1],
                    audio_path=avlist[i][3],
                    targetFolder=targetFolder,
                    audioNameStr=audioNameStr,
                    needProceed=needProceed,
                    audio_name=avlist[i][4]
                )
            u.info('Finished!')


# Main Error Handle
try:
    Main()

except KeyboardInterrupt:
    # User force stop (^C/^Z)
    print('[Detected ^C/^Z or other stop signal]')
    u.info('Quitting.')
    sys_exit(1)

except Exception as e:
    # Other exceptions
    print(f'[Main ERROR] Exception: {e}')
    raise
