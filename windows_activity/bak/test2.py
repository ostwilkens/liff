#%%
import sys
import time
import ctypes
import ctypes.wintypes

user32 = ctypes.windll.user32
ole32 = ctypes.windll.ole32
ole32.CoInitialize(0)


def get_hwnd_title(hwnd):
    length = user32.GetWindowTextLengthA(hwnd)
    buff = ctypes.create_string_buffer(length + 1)
    user32.GetWindowTextA(hwnd, buff, length + 1)
    return buff.value


#%%

# get focused hwnd
focused_hwnd = user32.GetForegroundWindow()

#%%
# get_hwnd_title(focused_hwnd)


#%%
pid = ctypes.wintypes.DWORD()
user32.GetWindowThreadProcessId(focused_hwnd, ctypes.byref(pid))
print(pid.value)

#%%

# get pid process name
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010
PROCESS_ALL_ACCESS = 0x1F0FFF
PROCESS_TERMINATE = 0x0001

kernel32 = ctypes.windll.kernel32
kernel32.OpenProcess.restype = ctypes.wintypes.HANDLE

process_handle = kernel32.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ | PROCESS_ALL_ACCESS | PROCESS_TERMINATE, False, pid.value)
print(process_handle)

# get process name
MAX_PATH = 260
GetModuleBaseName = ctypes.windll.psapi.GetModuleBaseNameA

lpBaseName = ctypes.create_string_buffer(MAX_PATH)
size = ctypes.c_ulong(MAX_PATH)
GetModuleBaseName(process_handle, None, ctypes.byref(lpBaseName), ctypes.byref(size))
print(lpBaseName.value)
