# !/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4
from tkinter import *
from tkinter import messagebox

import openpyxl
import os
import sys, traceback, types


def isUserAdmin():
    if os.name == 'nt':
        import ctypes
        # WARNING: requires Windows XP SP2 or higher!
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            traceback.print_exc()
            print("Admin check failed, assuming not an admin.")
            return False
    else:
        # Check for root on Posix
        return os.getuid() == 0


def runAsAdmin(cmdLine=None, wait=True):


    if os.name != 'nt':
        raise RuntimeError("This function is only implemented on Windows.")

    import win32api, win32con, win32event, win32process
    from win32com.shell.shell import ShellExecuteEx
    from win32com.shell import shellcon

    python_exe = sys.executable

    if cmdLine is None:
        cmdLine = [python_exe] + sys.argv
    elif type(cmdLine) not in (types.TupleType, types.ListType):
        raise ValueError("cmdLine is not a sequence.")
    cmd = '"%s"' % (cmdLine[0],)
    # XXX TODO: isn't there a function or something we can call to massage command line params?
    params = " ".join(['"%s"' % (x,) for x in cmdLine[1:]])
    cmdDir = ''
    showCmd = win32con.SW_SHOWNORMAL
    lpVerb = 'runas'  # causes UAC elevation prompt.

    # print "Running", cmd, params

    # ShellExecute() doesn't seem to allow us to fetch the PID or handle
    # of the process, so we can't get anything useful from it. Therefore
    # the more complex ShellExecuteEx() must be used.

    # procHandle = win32api.ShellExecute(0, lpVerb, cmd, params, cmdDir, showCmd)

    procInfo = ShellExecuteEx(nShow=showCmd,
                              fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
                              lpVerb=lpVerb,
                              lpFile=cmd,
                              lpParameters=params)

    if wait:
        procHandle = procInfo['hProcess']
        obj = win32event.WaitForSingleObject(procHandle, win32event.INFINITE)
        rc = win32process.GetExitCodeProcess(procHandle)
    else:
        rc = None

    return rc


def test():
    """A simple test function; check if we're admin, and if not relaunch
    the script as admin."""
    rc = 0
    if not isUserAdmin():
        print("You're not an admin.", os.getpid(), "params: ", sys.argv)
        rc = runAsAdmin()
    else:
        print("You are an admin!", os.getpid(), "params: ", sys.argv)
        rc = 0
    input('Press Enter to exit.')
    return rc


if __name__ == "__main__":
    res = test()

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'htmltext.txt')

def clean_file():
    file = open(my_file, 'w')
    file.close()


def search(htmlfile):
    lines = htmlfile.readlines()
    link_list = []
    for strings in lines:
        links = re.findall(r'/resume/\w{38}\b', strings)
        for i in links:
            link_list.append('https://hh.ru' + i)
    return link_list


def clicked():
    workfile = open(my_file, 'r', encoding='utf-8')
    result = search(workfile)
    workfile.close()
    wb = openpyxl.Workbook()
    ws1 = wb.worksheets[0]
    ws1['A1'] = 'Ссылка'
    ws1['B1'] = 'Просмотрено'
    ws1['C1'] = 'Кем'
    ws1['D1'] = 'Одобрено'
    ws1.column_dimensions['A'].width = 60.0
    ws1.column_dimensions['B'].width = 30.0
    ws1.column_dimensions['C'].width = 25.0
    ws1.column_dimensions['D'].width = 10.0
    ws1.title = txt1.get()
    data_create = txt2.get()
    r = 2
    for i in result:
        ws1.cell(row=r, column=1).value = i
        r += 1
    os.chdir(THIS_FOLDER)
    wb.save(filename=ws1.title + '_' + data_create + '.xlsx', )
    messagebox.showinfo(message='Готово!')


window = Tk()
window.geometry('400x100')
window.title('HRcreate_v0_1')

lbl1 = Label(window, text='Название')
lbl1.grid(column=2, row=2)
lbl2 = Label(window, text='Дата(ДДММГГГГ)')
lbl2.grid(column=4, row=2)

txt1 = Entry(window, width=30)
txt1.grid(column=2, row=3)
txt1.focus()
txt2 = Entry(window, width=15)
txt2.grid(column=4, row=3)

btn = Button(window, text='Создать', command=clicked)
btn.grid(column=5, row=3)
btn1 = Button(window, text='Очистить файл', command=clean_file)
btn1.grid(column=2, row=4)

window.mainloop()
