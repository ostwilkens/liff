#%%
import sys
import time
import ctypes
import ctypes.wintypes

EVENT_OBJECT_FOCUS = 0x8005
EVENT_OBJECT_NAMECHANGE = 0x800C
EVENT_SYSTEM_DIALOGSTART = 0x0010
WINEVENT_OUTOFCONTEXT = 0x0000

user32 = ctypes.windll.user32
ole32 = ctypes.windll.ole32

ole32.CoInitialize(0)

WinEventProcType = ctypes.WINFUNCTYPE(
    None, 
    ctypes.wintypes.HANDLE,
    ctypes.wintypes.DWORD,
    ctypes.wintypes.HWND,
    ctypes.wintypes.LONG,
    ctypes.wintypes.LONG,
    ctypes.wintypes.DWORD,
    ctypes.wintypes.DWORD
)

focused_hwnd = None

def get_hwnd_title(hwnd):
    length = user32.GetWindowTextLengthA(hwnd)
    buff = ctypes.create_string_buffer(length + 1)
    user32.GetWindowTextA(hwnd, buff, length + 1)
    return buff.value

def callback(hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime):
    global focused_hwnd

    if event == EVENT_OBJECT_FOCUS:
        focused_hwnd = hwnd
        new_title = get_hwnd_title(hwnd)
        print(f"changed focus to '{new_title}'")
    elif event == EVENT_OBJECT_NAMECHANGE:
        if focused_hwnd == hwnd:
            new_title = get_hwnd_title(hwnd)
            print(f"changed name to '{new_title}'")
        # else:
        #     print("other window changed name")
            


WinEventProc = WinEventProcType(callback)

user32.SetWinEventHook.restype = ctypes.wintypes.HANDLE
hook = user32.SetWinEventHook(
    EVENT_OBJECT_FOCUS,
    EVENT_OBJECT_NAMECHANGE,
    0,
    WinEventProc,
    0,
    0,
    WINEVENT_OUTOFCONTEXT
)
if hook == 0:
    print('SetWinEventHook failed')
    sys.exit(1)

msg = ctypes.wintypes.MSG()
while user32.GetMessageW(ctypes.byref(msg), 0, 0, 0) != 0:
    user32.TranslateMessageW(msg)
    user32.DispatchMessageW(msg)

user32.UnhookWinEvent(hook)
ole32.CoUninitialize()
