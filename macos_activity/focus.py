#%%
from AppKit import NSWorkspace
import time
import psutil
import os
import platform
import requests


def get_focused_app():
    return NSWorkspace.sharedWorkspace().frontmostApplication()

# def get_app_window_title(app):

app = get_focused_app()
localized_name = app.localizedName()
bundle_id = app.bundleIdentifier()


print(f"App: {localized_name} ({bundle_id})")

# get_app_window_title(get_focused_app())

#%%

def get_foreground_window_pid():
    return win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())[-1]

def get_pid_process_name(pid):
    return(psutil.Process(pid).name())

def get_pid_process_description(pid):
    p = psutil.Process(pid)
    ExecutablePath = p.exe()
    langs = win32api.GetFileVersionInfo(ExecutablePath, "\VarFileInfo\Translation")
    key = "StringFileInfo\%04x%04x\FileDescription" % (langs[0][0], langs[0][1])
    description=(win32api.GetFileVersionInfo(ExecutablePath, key))
    return description

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


current_active_title = None

while True:
    new_title = get_foreground_window_title()
    if len(new_title) > 0 and new_title != current_active_title:
        current_active_title = new_title

        pid = get_foreground_window_pid()

        info = {
            "time": get_unix_timestamp(),
            "title": current_active_title,
            "process": get_pid_process_name(pid),
            "description": get_pid_process_description(pid),
            "os": get_os_name(),
            "platform": get_platform_system(),
            "release": get_platform_release(),
            "node": get_platform_node()
        }

        url = "https://liff-api.ostwilkens.se/add_window_focus"
        requests.post(url, json=info)

        print(info)
    
    time.sleep(10)
