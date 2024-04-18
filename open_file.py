import os
import win32con
import win32ui


def browse(mode: bool,
           default_name: str = "",
           title: str = "选择您的文件",
           file_type: str = "所有文件(*.*)|*.*|",
           path: str = "desktop"):
    API_flag = win32con.OFN_OVERWRITEPROMPT | win32con.OFN_FILEMUSTEXIST
    dlg = win32ui.CreateFileDialog(mode, None, default_name, API_flag, file_type)
    dlg.SetOFNTitle(title)
    dlg.SetOFNInitialDir(os.path.abspath(path))
    dlg.DoModal()
    filename = dlg.GetPathName()
    fileExt = dlg.GetFileExt()
    if os.path.exists(filename):
        if_pass = True
    elif not mode:
        if os.path.split(filename)[0] == '':
            if_pass = False
        else:
            if_pass = True
    else:
        if_pass = False
    return [if_pass, filename, fileExt]



# respond = browse(True)
# pass