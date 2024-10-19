# coding: utf-8

# import
from sys import exit as sys_exit
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
            u.info('Selected config:')
            u.info(f'Name: {conf["name"]}')
            u.info(f'BaseFolder: {conf["baseFolder"]}')
            u.info(f'TargetFolder: {conf["targetFolder"]}')
        except KeyboardInterrupt:
            raise
        except:
            u.warning('Invaild config number!')
            continue
        break

    # main while
    while True:
        # get av id
        avbv = u.input('AV/BV id: ')
        avid = u.videoid.convert(avbv)
        if not avid:
            continue

        #


# Main Error Handle
try:
    sys_exit(Main())
except KeyboardInterrupt:
    print('[Detected ^C/^Z or other stop signal]')
    u.info('Quitting.')

except Exception as e:
    print(f'[Main ERROR] Exception: {e}')
    raise
