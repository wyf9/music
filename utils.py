# coding: utf-8
if __name__ == '__main__':
    print('Please start main program craate.py!')

class utils:
    '''
    在创建实例时请额外使用
    ```
    u.videoid = u.videoid_init(u)
    ```
    '''
    def __init__(self):
        try:
            from colorama import Fore, Style
            self.colorama = True
            self.color_fore = Fore
            self.color_style = Style
        except:
            print(f'[utils] [WARNING] colorama import failed, will disable colorful output.')
            self.colorama = False
    def info(self, msg):
        if self.colorama:
            print(f'{self.color_fore.GREEN}[INFO]{self.color_style.RESET_ALL} {msg}')
        else:
            print(f'[INFO] {msg}')
    def tip(self, msg):
        if self.colorama:
            print(f'{self.color_fore.MAGENTA}[TIP]{self.color_style.RESET_ALL} {msg}')
        else:
            print(f'[TIP] {msg}')
    def debug(self, msg):
        if self.colorama:
            print(f'{self.color_fore.CYAN}[DEBUG]{self.color_style.RESET_ALL} {msg}')
        else:
            print(f'[DEBUG] {msg}')
    def warning(self, msg):
        if self.colorama:
            print(f'{self.color_fore.YELLOW}[WARNING]{self.color_style.RESET_ALL} {msg}')
        else:
            print(f'[WARNING] {msg}')
    def error(self, msg):
        if self.colorama:
            print(f'{self.color_fore.RED}[ERROR]{self.color_style.RESET_ALL} {msg}')
        else:
            print(f'[ERROR] {msg}')
    def input(self, msg):
        if self.colorama:
            ret = input(f'{self.color_fore.BLUE}[INPUT]{self.color_style.RESET_ALL} {msg}')
        else:
            ret = input(f'[INPUT] {msg}')
        return ret
    class videoid_init:
        '''
        本 class 中的 av/bv 互转代码来自 https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/misc/bvid_desc.md#python
        并作出了一点修改
        '''
        def __init__(self, utils_instance):
            self.utils_instance = utils_instance
        XOR_CODE = 23442827791579
        MASK_CODE = 2251799813685247
        MAX_AID = 1 << 51
        ALPHABET = "FcwAPNKTMug3GV5Lj7EJnHpWsx4tb8haYeviqBz6rkCy12mUSDQX9RdoZf"
        ENCODE_MAP = 8, 7, 0, 5, 1, 3, 2, 4, 6
        DECODE_MAP = tuple(reversed(ENCODE_MAP))

        BASE = len(ALPHABET)
        PREFIX = "BV1"
        PREFIX_LEN = len(PREFIX)
        CODE_LEN = len(ENCODE_MAP)

        def av2bv(self, avid: int) -> str:
            bvid = [""] * 9
            tmp = (self.MAX_AID | avid) ^ self.XOR_CODE
            for i in range(self.CODE_LEN):
                bvid[self.ENCODE_MAP[i]] = self.ALPHABET[tmp % self.BASE]
                tmp //= self.BASE
            return self.PREFIX + "".join(bvid)

        def bv2av(self, bvid: str) -> int:
            assert bvid[:3] == self.PREFIX

            bvid = bvid[3:]
            tmp = 0
            for i in range(self.CODE_LEN):
                idx = self.ALPHABET.index(bvid[self.DECODE_MAP[i]])
                tmp = tmp * self.BASE + idx
            return (tmp & self.MASK_CODE) ^ self.XOR_CODE
        def convert(self, id: str) -> int:
            '''
            增加
            自动判断是否为 av 号, 如不是则转换为 av 号
            '''
            try:
                retid = int(id)
                self.utils_instance.debug(f'[videoid/convert] avid: {retid}')
                return retid
            except:
                try:
                    retid = self.bv2av(id)
                except:
                    self.utils_instance.warning('Convert failed! av/bv id corrent?')
                    return None
                self.utils_instance.debug(f'[videoid/convert] bvid: {id} -> avid: {retid}')
                return retid
    videoid = videoid_init(utils_instance=None)
