__author__ = 'yami'
from unicurses import *
import threading

stdscr = initscr()
start_color()
curs_set(False)
noecho()
keypad(stdscr, True)

class Window():
    def __init__(self, name='win', ly=10, lx=10, y=0, x=0, isVisible=True, isSelected=True):
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

def a():
    while 1:
        pass
t = threading.Thread(target=a)
t.start()

file = open('name').readlines()
windows = []
window = {'name': 'name', 'length_x' : 0, 'length_y' : 0, 'position_y': 0, 'position_x': 0, 'visible': 'no'}
find = 0
for row in range(len(file)):
    if find == 0:
        name = ""
        for sym in file[row]:
            if sym!='{':
                name+=sym
            else:
                find = 1
                window['name'] = name
    elif find == 1:
        data = file[row].split(':')
        #print(data)
        if data[0] != '}\n':
            if data[0] == 'length_y':
                window['length_y'] = int(data[1][1:])
            elif data[0] == 'length_x':
                window['length_x'] = int(data[1][1:])
            elif data[0] == 'position_y':
                window['position_y'] = int(data[1][1:])
            elif data[0] == 'position_x':
                window['position_x'] = int(data[1][1:])
            elif data[0] == 'visible':
                visible = data[1][1:]
                visible = visible.replace('\n','')
                window['visible'] = visible
        else:
            find = 0
            windows.append(window.copy())
allwin = []
for window in windows:
    allwin.append(Window(window['name'],window['length_y'],window['length_x'],window['position_y'],window['position_x'],isSelected=False))

update_panels()
doupdate()

input()