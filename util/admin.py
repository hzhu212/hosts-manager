# -*- coding: utf-8 -*-

import sys, os

def is_admin_nt():
    import ctypes
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def is_admin_posix():
    return os.geteuid() == 0


def run_as_admin(cmd_line=None, wait=True):

    if os.name != 'nt':
        raise RuntimeError('This function is only implemented on Windows.')

    import win32api, win32con, win32event, win32process
    from win32com.shell.shell import ShellExecuteEx
    from win32com.shell import shellcon

    python_exe = sys.executable

    if cmd_line is None:
        cmd_line = [python_exe] + sys.argv
    elif type(cmd_line) not in (tuple, list):
        raise ValueError('cmd_line is not a sequence.')
    cmd = '"%s"' % (cmd_line[0],)
    # XXX TODO: isn't there a function or something we can call to massage command line params?
    params = " ".join(['"%s"' % (x,) for x in cmd_line[1:]])
    cmdDir = ''
    showCmd = win32con.SW_SHOWNORMAL
    #showCmd = win32con.SW_HIDE
    lpVerb = 'runas'  # causes UAC elevation prompt.

    # print "Running", cmd, params

    # ShellExecute() doesn't seem to allow us to fetch the PID or handle
    # of the process, so we can't get anything useful from it. Therefore
    # the more complex ShellExecuteEx() must be used.

    # procHandle = win32api.ShellExecute(0, lpVerb, cmd, params, cmdDir, showCmd)

    procInfo = ShellExecuteEx(
        nShow=showCmd,
        fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
        lpVerb=lpVerb,
        lpFile=cmd,
        lpParameters=params)

    if wait:
        procHandle = procInfo['hProcess']
        obj = win32event.WaitForSingleObject(procHandle, win32event.INFINITE)
        rc = win32process.GetExitCodeProcess(procHandle)
        #print "Process handle %s returned code %s" % (procHandle, rc)
    else:
        rc = None

    return rc
