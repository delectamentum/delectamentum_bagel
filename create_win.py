__author__ = 'Daniil'
from unicurses import *
import threading, time
allwin = []

class Window():
    def __init__(self, name='win' + str(len(allwin)), ly=10, lx=10, y=0, x=0, isVisible=True, isSelected=True):
        self.name = str(name)
        self.ly = int(ly)
        self.lx = int(lx)
        self.y = int(y)
        self.x = int(x)
        self.isVisible = isVisible
        self.isSelected = isSelected
        self.win = newwin(ly, lx, y, x)
        self.panel = new_panel(self.win)
        self.select(isSelected)
        self.visible(isVisible)
        mvwaddstr(self.win, 1, 1, self.name)

    def select(self, isSelected):
        self.isSelected = isSelected
        if self.isSelected:
            wborder(self.win, 32, 32, 32, 32, 0, 0, 0, 0)
        else:
            box(self.win)

    def visible(self, isVisible):
        if isVisible:
            show_panel(self.panel)
            self.isVisible = True
        else:
            hide_panel(self.panel)
            self.isVisible = False




def movewin(window,key):
    update = False
    if key == 261:
        if window.x + window.lx < 80:
            window.x += 1
            update = True
        else:
            beep()
    elif key == 260:
        if window.x > 0:
            window.x -= 1
            update = True
        else:
            beep()
    elif key == 259:
        if window.y > 0:
            window.y -= 1
            update = True
        else:
            beep()
    elif key == 258:
        if window.y + window.ly < 25:
            window.y += 1
            update = True
        else:
            beep()
    if update:
        move_panel(window.panel, window.y, window.x)

def scale(window, key):
    update = False
    if key == 54:
        if window.x + window.lx < 80:
            window.lx += 1
            update = True
        else:
            beep()
    elif key == 52:
        if window.lx > 2:
            window.lx -= 1
            update = True
        else:
            beep()
    elif key == 56:
        if window.ly > 2:
            window.ly -= 1
            update = True
        else:
            beep()
    elif key == 50:
        if window.y + window.ly < 25:
            window.ly += 1
            update = True
        else:
            beep()
    elif key == 51:
        if window.x + window.lx < 80 and window.y + window.ly < 25:
            window.ly += 1
            window.lx += 1
            update = True
        else:
            beep()
    elif key == 55:
        if window.lx > 2 and window.ly > 2:
            window.lx -= 1
            window.ly -= 1
            update = True
        else:
            beep()
    if update:
        wclear(window.win)
        wrefresh(window.win)
        del_panel(window.panel)
        delwin(window.win)
        window.win = newwin(window.ly, window.lx, window.y, window.x)
        window.select(window.isSelected)
        window.panel = new_panel(window.win)

def switchWindow(nowwin, k):
    if nowwin + k > len(allwin) - 1:
        nowwin = 0
    elif nowwin + k < 0:
        nowwin = len(allwin) - 1
    else:
        nowwin += k
    return  nowwin






stdscr = initscr()
start_color()
curs_set(False)
noecho()
keypad(stdscr, True)


def a():
    while 1:
        pass
t = threading.Thread(target=a)
t.start()

#if __name__ == 'main':
'''info = newwin(5, 20, 10, 30)
wborder(info, 32, 32, 32, 32, 0, 0, 0, 0)
infop = new_panel(info)'''


windowList = Window('windowList', 7, 20, 0, 0, False, False)

allwin.append(Window(name='win' + str(len(allwin))))
nowwin = len(allwin) - 1
focus = allwin[nowwin]

update_panels()
doupdate()
while 1:

    key = int(getch())
    if key == 96:
        windowList.visible(not windowList.isVisible)

    if key == 49:
        panel_below(windowList.panel)
    if key == 465:
        allwin.append(Window(name='win' + str(len(allwin))))
        focus.select(False)
        nowwin = len(allwin) - 1
        focus = allwin[nowwin]
        wborder(focus.win, 32, 32, 32, 32, 0, 0, 0, 0)

    if key == 44:
        focus.select(False)
        nowwin = switchWindow(nowwin, -1)
        focus = allwin[nowwin]
        focus.select(True)
    if key == 46:
        focus.select(False)
        nowwin = switchWindow(nowwin, 1)
        focus = allwin[nowwin]
        focus.select(True)


    if key == 261 or key == 260 or key == 259 or key == 258:
        movewin(focus, key)

    if key == 54 or key == 52 or key == 56 or key == 50 or key == 51 or key == 55:
        scale(focus, key)

    for i in range(len(allwin)):
        mvwaddstr(allwin[i].win, 1, 1, str(allwin[i].name))
    #top_panel(windowList.panel)



    if key == 10:
        data = ''
        name = 'name'
        save = open(name, 'w')
        for i in range(len(allwin)):
            data += str(allwin[i].name) + '{\nlength_y: ' \
                    + str(allwin[i].ly) + '\nlength_x: ' \
                    + str(allwin[i].lx) + '\nposition_y: ' \
                    + str(allwin[i].y) + '\nposition_x: ' \
                    + str(allwin[i].x) + '\nvisible: ' \
                    + str(allwin[i].isVisible) + '\n}\n'
        save.write(data)
        save.close()


    update_panels()
    doupdate()





input()