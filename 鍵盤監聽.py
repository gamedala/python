from pynput import keyboard
from pynput.keyboard import Key, Controller, KeyCode

# 键盘控制对象
keyboard = Controller()

# 按下 a 键
keyboard.press('a')
# 释放 a 键
keyboard.release('a')

# 按下 Shift 键
keyboard.press(Key.shift)
keyboard.press('b')
keyboard.release('b')
keyboard.press('c')
keyboard.release('c')
# 释放 Shift 键
keyboard.release(Key.esc)

# 按下 Shift 键，然后依次按下其他按键，完成后Shift键自动释放
with keyboard.pressed(Key.shift):
    keyboard.press('d')
    keyboard.release('d')
    keyboard.press('e')
    keyboard.release('e')

# 依次按下 python （包括前面的空格）
keyboard.type(' python')

# 按下 vk值为56的键 shift 键
keyboard.touch(KeyCode.from_vk(56), True)
keyboard.touch('a', True)
keyboard.touch('a', False)
# 释放 shift 键
keyboard.touch(Key.shift, False)

# 按键按下监听
def on_press(key):
    try:
        print('press key {0}, vk: {1}'.format(key.char, key.vk))
    except AttributeError:
        print('special press key {0}, vk: {1}'.format(key, key.value.vk))


# 按键释放监听
def on_release(key):

    if key == keyboard.Key.esc:
        # 停止监听
        return False

    try:
        print('release key {0}, vk: {1}'.format(key.char, key.vk))
    except AttributeError:
        print('special release key {0}, vk: {1}'.format(key, key.value.vk))


# 键盘监听
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()