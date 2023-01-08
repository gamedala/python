import win32gui

def show_window_attr(hWnd,window):
    '''
    显示窗口的属性
    :return:
    '''
    if not hWnd:
        return
    window_hwnd = []
    title = win32gui.GetWindowText(hWnd)
    if window == title:
        window_hwnd.append(hWnd)
        clsname = win32gui.GetClassName(hWnd)
        print ('窗口句柄:%s 窗口标题:%s 窗口类名:%s' %(hWnd,title,clsname))

def show_windows(hWndList,window):
    for h in hWndList:
        show_window_attr(h,window)

def demo_top_windows(window):
    '''
    演示如何列出所有的顶级窗口
    :return:
    '''
    hWndList = []
    window_hwnd = []
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)
    for h in hWndList:
        if not h:
            return
        title = win32gui.GetWindowText(h)
        if window == title:
            window_hwnd.append(h)
            clsname = win32gui.GetClassName(h)
            print ('窗口句柄:%s 窗口标题:%s 窗口类名:%s' %(h,title,clsname))
    return window_hwnd
 
 
hWndList = demo_top_windows('RO仙境傳說：愛如初見')
print(hWndList)
for window in hWndList:
    print(window)
#assert len(hWndList)

#parent = hWndList[20]
#若无法遍历，需要使用spy++确认是否存在子窗口
#hWndChildList = demo_child_windows(parent)