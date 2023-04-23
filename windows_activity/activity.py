#%%
import keyboard
import mouse
import time
import os
import platform
import requests


def get_os_name():
    return os.name

def get_platform_system():
    return platform.system()

def get_platform_release():
    return platform.release()

def get_platform_node():
    return platform.node()

def get_unix_timestamp():
    return int(time.time())


input_count = 0

def on_press(e):
    global input_count
    input_count += 1


def on_mouse():
    global input_count
    input_count += 1

keyboard.on_press(on_press)
mouse.on_button(on_mouse)


last_mouse_pos = None
frequency = 60 # seconds
while True:
    new_mouse_pos = mouse.get_position()

    if new_mouse_pos != last_mouse_pos:
        last_mouse_pos = new_mouse_pos
        input_count += 1

    if input_count > 0:
        info = {
            "time": int(time.time()),
            "frequency": frequency,
            "input_count": input_count,
            "os": get_os_name(),
            "platform": get_platform_system(),
            "release": get_platform_release(),
            "node": get_platform_node()
        }

        url = "https://liff-api.ostwilkens.se/add_machine_activity"
        requests.post(url, json=info)

        print(info)

        input_count = 0
    
    time.sleep(frequency)
