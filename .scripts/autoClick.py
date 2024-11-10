# coding: utf-8

import yaml  # pyyaml
import keyboard  # keyboard
import pyautogui  # pyautogui
from time import sleep


def main():
    # 从配置文件中加载快捷键和坐标
    with open('autoClick_config.yml', 'r') as f:
        config = yaml.safe_load(f)

    print(f'Add hotkey: ctrl+shift+0 -> mouse_click_2()')
    keyboard.add_hotkey(shortcut, mouse_click_2)
    # 注册按键监听事件
    for shortcut, coordinates in config.items():
        print(f'Add hotkey: {shortcut} -> {coordinates}')
        keyboard.add_hotkey(shortcut, mouse_click, args=(coordinates,))

    # 开始监听按键事件
    print('Start waiting')
    keyboard.wait()


def mouse_click(coordinates):
    print(f'Trigged click: {coordinates}')
    x, y = coordinates['x'], coordinates['y']
    pyautogui.click(1198, 1079)
    pyautogui.click(x, y)

def mouse_click_2():
    print(f'Trigged click: muse_click_2()')
    st = 0.05
    pyautogui.click(1198, 1079)
    sleep(st)
    pyautogui.rightClick(787, 549)
    sleep(st)
    pyautogui.click(1020, 871)
    sleep(st)
    pyautogui.click(1193, 871)


if __name__ == '__main__':
    main()
