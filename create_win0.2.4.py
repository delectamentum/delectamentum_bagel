from unicurses import *
import threading, time
allwin = []
set_key = 'createWin'

stdscr = initscr()
curs_set(False)
noecho()
keypad(stdscr, True)
start_color()



def a():
    while 1:
        pass
t = threading.Thread(target=a)
t.start()

class Window():
    def __init__(self, name='win' + str(len(allwin)), ly=10, lx=10, y=0, x=0, is_visible=True, is_selected=True):
        self.name = str(name)
        self.ly = int(ly)
        self.lx = int(lx)
        self.y = int(y)
        self.x = int(x)
        self.is_visible = is_visible
        self.is_selected = is_selected
        self.win = newwin(ly, lx, y, x)
        self.panel = new_panel(self.win)
        self.select(is_selected)
        self.visible(is_visible)
        #mvwaddstr(self.win, 1, 1, self.name)

    def select(self, is_selected):
        self.is_selected = is_selected
        if self.is_selected:
            wborder(self.win, 32, 32, 32, 32, 0, 0, 0, 0)
        elif not self.is_selected:
            box(self.win)

    def visible(self, is_visible):
        if is_visible:
            show_panel(self.panel)
            self.is_visible = True
        elif not is_visible:
            hide_panel(self.panel)
            self.is_visible = False

    def delete(self):
        del_panel(self.panel)
        delwin(self.win)
        self.is_selected = None
        self.is_visible = None

    def clear_win(self):
        for i in range(1, self.ly - 1):
            mvwaddstr(self.win, i, 1, ' ' * (self.lx - 2), A_NORMAL)

class SwitchObjects(Window):
    def set_params(self, selection_mode, line_selection_objects, y, x, num_rows, *args):
        self.set_window_select_position()
        self.selection_mode = selection_mode
        self.line_selection_objects = line_selection_objects
        self.num_rows = num_rows
        self.width_col = args
        self.y_col = y
        self.x_col = x

    #selection_mode == 0: A_BLINK; 1: A_REVERS; line_selection_objects == 0: select 1 object; == 1: select all line
    def update_switch_object(self, data=None, id=None, name_of_col = None):
        self.active = True
        if data is not None:
            self.data = data
        if id is not None:
            self.id_selected = id
        if name_of_col is not None:
            self.name_of_col = name_of_col
        for i in range(1):
        #try:
            x_this_col = self.x_col
            for j in range(len(self.data)):
                y_this_row = self.y_col + 1
                mvwaddstr(self.win, self.y_col, x_this_col, str(self.name_of_col[j][:self.width_col[j]]), A_BOLD)
                if j != len(self.data) - 1:
                    mvwaddstr(self.win, self.y_col, x_this_col + self.width_col[j], '|', A_BOLD)
                for i in range(self.id_selected[1] - self.window_select_position,
                               len(self.data[j]) if self.num_rows - 1 - self.window_select_position >= len(self.data[j]) - 1 - self.id_selected[1]
                               else self.id_selected[1] + self.num_rows - self.window_select_position):
                    if len(self.data[j][i]) < self.width_col[j]:
                        fill_space = (self.width_col[j] - len(self.data[j][i])) * ' '
                    else:
                        fill_space = ''
                    if (i == self.id_selected[1] and j == self.id_selected[0] and self.line_selection_objects == 0) or \
                            (i == self.id_selected[1] and self.line_selection_objects == 1):
                        if self.selection_mode == 0:
                            mvwaddstr(self.win, i + y_this_row - (self.id_selected[1] - self.window_select_position), x_this_col, str(self.data[j][i][:self.width_col[j]] + fill_space),
                                      A_BOLD)
                        elif self.selection_mode == 1:
                            mvwaddstr(self.win, i + y_this_row - (self.id_selected[1] - self.window_select_position), x_this_col, str(self.data[j][i][:self.width_col[j]] + fill_space),
                                      A_REVERSE)
                    else:
                        mvwaddstr(self.win, i + y_this_row - (self.id_selected[1] - self.window_select_position), x_this_col, str(self.data[j][i][:self.width_col[j]]) + fill_space)
                    if j != len(self.data) - 1:
                        if self.selection_mode == 1 and i == self.id_selected[1] and self.line_selection_objects == 1:
                            mvwaddstr(self.win, i + y_this_row - (self.id_selected[1] - self.window_select_position), x_this_col + self.width_col[j], '|', A_REVERSE)
                        else:
                            mvwaddstr(self.win, i + y_this_row - (self.id_selected[1] - self.window_select_position), x_this_col + self.width_col[j], '|')
                x_this_col += self.width_col[j] + 1
        #except:
        #    print('List error')


    def set_window_select_position(self):
        try:
            if self.id_selected[1] <= self.num_rows - 1:
                self.window_select_position = self.id_selected[1]
            elif len(self.data[0]) - 1 - self.id_selected[1] <= self.num_rows - 1:
                self.window_select_position = (self.num_rows - 1) - ((len(self.data[0]) - 1) - self.id_selected[1])
            else:
                self.window_select_position = 0
        except:
            self.window_select_position = 0

    def clear(self):
        lenght = 1
        for j in range(len(self.data)):
            lenght += self.width_col[j]
            if j != len(self.data) - 1:
                lenght += 1
        for i in range(self.num_rows):
            mvwaddstr(self.win, i + self.y_col + 1, self.x_col, ' ' * lenght)

class InputText():
    def __init__(self, win, x, y, lenght, show_mode, local_cursor, string=''):
        self._cursor = local_cursor
        self.win = win
        self.x = x
        self.y = y
        self.lenght = lenght
        self.show_mode = show_mode
        self.string = string
        self.update_cursor()
        self._cursor.set_params(self.win, self.y, self.x, self.window_cursor_position, str(self.string[self.string_cursor_position]))
        self._cursor.active = True
        #if self.show_mode == 1:
        #    mvwaddstr(self.win, self.y, self.x, self.string, A_REVERSE)

    def update_string(self, key):
        if key == 261:
            if self.string_cursor_position < len(self.string) - 1:
                self.string_cursor_position += 1
                if self.window_cursor_position < self.lenght - 1:
                    self.window_cursor_position += 1
            elif self.string_cursor_position == len(self.string) - 1:
                self.string_cursor_position += 1
                if self.window_cursor_position != self.lenght - 1:
                    self.window_cursor_position += 1
            else:
                beep()

        elif key == 260:
            if self.string_cursor_position != 0:
                self.string_cursor_position -= 1
            if self.window_cursor_position != 0:
                self.window_cursor_position -= 1
        elif key == 8: #backspace
            if len(self.string) > self.string_cursor_position:
                self.string = self.string[:self.string_cursor_position] + self.string[self.string_cursor_position + 1:]
                if len(self.string) == self.string_cursor_position and self.string_cursor_position != 0:
                    self.string_cursor_position -= 1
                    if self.window_cursor_position != 0:
                        self.window_cursor_position -= 1
            elif len(self.string) == self.string_cursor_position and self.string_cursor_position != 0:
                self.string_cursor_position -= 1
                if self.window_cursor_position == len(self.string) and self.window_cursor_position != 0:
                    self.window_cursor_position -= 1

        elif key == 10:
            self._cursor.active = False
            return self.string
        else:
            try:
                mvwaddstr(self.win, self.y, self.x, chr(key))
                if self.string_cursor_position == len(self.string):
                    self.string_cursor_position += 1
                    if self.window_cursor_position + 1 < self.lenght:
                        self.window_cursor_position += 1
                self.string = self.string[:self.string_cursor_position] + chr(key) + self.string[self.string_cursor_position:]
            except:
                beep()

        self.print_string()
        self._cursor.position = self.window_cursor_position
        try:
            self._cursor.char = str(self.string[self.string_cursor_position])
        except:
            self._cursor.char = ' '

    def print_string(self):
        self.del_row(self.win, self.y, self.x, self.lenght)
        if self.show_mode == 0:
            mvwaddstr(self.win, self.y, self.x, str(self.string[((self.string_cursor_position - self.window_cursor_position)
                                                    if (self.string_cursor_position - self.window_cursor_position > 0) else 0):
                                                    self.string_cursor_position + self.lenght - self.window_cursor_position]))
        elif self.show_mode == 1:
            mvwaddstr(self.win, self.y, self.x, str(self.string[((self.string_cursor_position - self.window_cursor_position)
                                                if (self.string_cursor_position - self.window_cursor_position > 0) else 0):
                                                self.string_cursor_position + self.lenght - self.window_cursor_position]),
                                                A_REVERSE)

    def del_row(self, win, y, x, lenght):
        if self.show_mode == 0:
            mvwaddstr(win, y, x, str(' ' * lenght))
        elif self.show_mode == 1:
            mvwaddstr(win, y, x, str(' ' * lenght), A_REVERSE)

    def update_cursor(self):
        self.window_cursor_position = (len(self.string) - 1 if len(self.string) - 1 >= 0 else 0) if len(self.string) <= self.lenght else (self.lenght - 1)
        self.string_cursor_position = len(self.string) - 1 if len(self.string) - 1 >= 0 else 0
        self._cursor.position = self.window_cursor_position
        try:
            self._cursor.char = str(self.string[self.string_cursor_position])
        except:
            self._cursor.char = ' '

class Cursor(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.active = False
        self.delay = 0.4

    def set_params(self, win, y, x, position, char):
        self.win = win
        self.y = y
        self.x = x
        self.position = position
        self.char = char

    def run(self):
        k = 0
        while True:
            if self.active:
                if k == 0:
                    wattron(self.win, A_REVERSE)
                    try:
                        mvwaddstr(self.win, self.y, self.x + self.position, self.char)
                    except:
                        mvwaddstr(self.win, self.y, self.x + self.position, ' ')
                    wattroff(self.win, A_REVERSE)
                    k = 1
                elif k == 1:
                    wattron(self.win, A_NORMAL)
                    try:
                        mvwaddstr(self.win, self.y, self.x + self.position, self.char)
                    except:
                        mvwaddstr(self.win, self.y, self.x + self.position, ' ')
                    wattroff(self.win, A_NORMAL)
                    k = 0
                doupdate()
                update_panels()
                time.sleep(self.delay)

cursor = Cursor()
cursor.start()


def movewin(window, key, position=(0, 0)):
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
    elif key is None:
        if 0 <= position[1] and position[1] + window.lx <= 80:
            window.x = position[1]
            update = True
        else:
            beep()
        if 0 <= position[0] and position[0] + window.ly <= 25:
            window.y = position[0]
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
        window.select(window.is_selected)
        window.panel = new_panel(window.win)

def switch_window(k):
    global nowwin
    if nowwin + k > len(allwin) - 1:
        nowwin = 0
    elif nowwin + k < 0:
        nowwin = len(allwin) - 1
    else:
        nowwin += k

def replace_window(k):
    global nowwin
    if nowwin + k >= 0 and nowwin + k <= len(allwin) - 1:
        allwin[nowwin], allwin[nowwin + k] = allwin[nowwin + k], allwin[nowwin]
        nowwin += k
        return True
    else:
        beep()
        return  False

def key_action(key):
    global focus, nowwin, set_key
    if set_key == 'createWin':
        if key == 96: # `
            windowList.visible(not windowList.is_visible)
            if windowList.is_visible:
                set_key = 'switchWindows'
                windowList.active = True
                windowList.id_selected[1] = nowwin
                windowList.set_window_select_position()
            else:
                set_key = 'createWin'
                windowList.active = False
        if key == 465: # num +
            allwin.append(Window(name='win' + str(len(allwin))))
            focus.select(False)
            nowwin = len(allwin) - 1
            focus = allwin[nowwin]
            wborder(focus.win, 32, 32, 32, 32, 0, 0, 0, 0)
        if key == 44: # ,
            focus.select(False)
            switch_window(-1)
            focus = allwin[nowwin]
            focus.select(True)
        if key == 46: # .
            focus.select(False)
            switch_window(1)
            focus = allwin[nowwin]
            focus.select(True)
        if key == 261 or key == 260 or key == 259 or key == 258: #right/left/up/down
            movewin(focus, key)
        if key == 54 or key == 52 or key == 56 or key == 50 or key == 51 or key == 55:
            scale(focus, key)
        if key == 330:
            if nowwin > 0:
                allwin[nowwin].delete()
                allwin.pop(nowwin)
                nowwin -= 1
                focus = allwin[nowwin]
                focus.select(True)
            else:
                beep()
        if key == 10: #Enter
            data = ''
            name = 'name'
            save = open(name, 'w')
            for i in range(len(allwin)):
                data += str(allwin[i].name) + '{\nlenght y: ' \
                        + str(allwin[i].ly) + '\nlenght x: ' \
                        + str(allwin[i].lx) + '\nposition y: ' \
                        + str(allwin[i].y) + '\nposition x: ' \
                        + str(allwin[i].x) + '\nvisible: ' \
                        + str(allwin[i].is_visible) + '\n}\n'
            save.write(data)
            save.close()


    elif set_key == 'switchWindows':
        windowList.active = True
        if key == 56 or key == 50 or key == 54 or key == 52:
            windowList.active = False
            if key == 56:
                movewin(windowList, 259)
            if key == 50:
                movewin(windowList, 258)
            if key == 54:
                movewin(windowList, 261)
            if key == 52:
                movewin(windowList, 260)
        if key == 259: #up
            if windowList.line_selection_objects == 0:
                if windowList.selection_mode == 0:
                    if windowList.window_select_position > 0:
                            windowList.window_select_position -= 1
                    else:
                        if windowList.id_selected[1] == 0:
                            if len(windowList.data[0]) - 1 < windowList.num_rows - 1:
                                windowList.window_select_position = len(windowList.data[0]) - 1
                            else:
                                windowList.window_select_position = windowList.num_rows - 1
                        else:
                            pass
                    if windowList.id_selected[1] > 0:
                        windowList.id_selected[1] -= 1
                    else:
                        windowList.id_selected[1] = len(windowList.data[windowList.id_selected[0]]) - 1
                    focus.select(False)
                    switch_window(-1)
                    focus = allwin[nowwin]
                    focus.select(True)
                elif windowList.selection_mode == 1:
                    if windowList.id_selected[0] == 2:
                        allwin[windowList.id_selected[1]].visible(not allwin[windowList.id_selected[1]].is_visible)
            elif windowList.line_selection_objects == 1:
                if replace_window(-1):
                    if windowList.window_select_position > 0:
                            windowList.window_select_position -= 1
                    else:
                        if windowList.id_selected[1] == 0:
                            if len(windowList.data[0]) - 1 < windowList.num_rows - 1:
                                windowList.window_select_position = len(windowList.data[0]) - 1
                            else:
                                windowList.window_select_position = windowList.num_rows - 1
                        else:
                            pass
                    windowList.id_selected[1] -= 1
                windowList.data[windowList.id_selected[0]][windowList.id_selected[1]] = '-'

        if key == 258: #down
            if windowList.line_selection_objects == 0:
                if windowList.selection_mode == 0:
                    if windowList.window_select_position < windowList.num_rows - 1 and windowList.id_selected[1] != len(windowList.data[0]) - 1:
                        windowList.window_select_position += 1
                    else:
                        if windowList.id_selected[1] == len(windowList.data[0]) - 1:
                            windowList.window_select_position = 0
                        else:
                            pass
                    if windowList.id_selected[1] + 1 <= len(windowList.data[windowList.id_selected[0]]) - 1:
                        windowList.id_selected[1] += 1
                    else:
                        windowList.id_selected[1] = 0
                    focus.select(False)
                    switch_window(1)
                    focus = allwin[nowwin]
                    focus.select(True)
                elif windowList.selection_mode == 1:
                    if windowList.id_selected[0] == 2:
                        allwin[windowList.id_selected[1]].visible(not allwin[windowList.id_selected[1]].is_visible)
            elif windowList.line_selection_objects == 1:
                if replace_window(1):
                    if windowList.window_select_position < windowList.num_rows - 1:
                        windowList.window_select_position += 1
                    else:
                        if windowList.id_selected[1] == len(windowList.data[0]) - 1:
                            windowList.window_select_position = 0
                        else:
                            pass
                    windowList.id_selected[1] += 1
                windowList.data[windowList.id_selected[0]][windowList.id_selected[1]] = '-'

        if key == 261: #right
            if windowList.selection_mode == 0:
                if windowList.id_selected[0] < len(windowList.data) - 1:
                    windowList.id_selected[0] += 1
                else:
                    beep()
            else:
                beep()

        if key == 260: #left
            if windowList.selection_mode == 0:
                if windowList.id_selected[0] > 0:
                    windowList.id_selected[0] -= 1
                else:
                    beep()
            else:
                beep()
        if key == 96: # `
            windowList.visible(not windowList.is_visible)
            if windowList.is_visible:
                set_key = 'switchWindows'
                windowList.active = True
                windowList.id_selected[1] = nowwin
                windowList.set_window_select_position()
            else:
                set_key = 'createWin'
                windowList.active = False
                windowList.selection_mode = 0
                windowList.line_selection_objects = 0

        if key == 330:
            if windowList.id_selected[0] == 0 and windowList.line_selection_objects == 1 and len(windowList.data[0]) != 1:
                windowList.clear()
                allwin[windowList.id_selected[1]].delete()
                allwin.pop(windowList.id_selected[1])
                windowList.data[0] = [str(i) for i in range(len(allwin))]
                windowList.line_selection_objects = 0
                windowList.selection_mode = 0
                if windowList.id_selected[1] > 0:
                    nowwin -= 1
                    windowList.id_selected[1] -= 1
                    if windowList.window_select_position > 0:
                        windowList.window_select_position -= 1
                        if windowList.num_rows - 1 - windowList.window_select_position > len(windowList.data[0]) - 1 - windowList.id_selected[1] and len(windowList.data[0]) > windowList.num_rows:
                            windowList.window_select_position = windowList.num_rows - (len(windowList.data[0]) - 1 - windowList.id_selected[1]) - 1






                focus = allwin[nowwin]
                focus.select(True)

            else:
                beep()

        if key == 10: #Enter
            if windowList.id_selected[0] == 0:
                if windowList.selection_mode == 1:
                    windowList.selection_mode = 0
                    windowList.line_selection_objects = 0
                elif windowList.selection_mode == 0:
                    windowList.selection_mode = 1
                    windowList.line_selection_objects = 1
                    windowList.data[windowList.id_selected[0]][windowList.id_selected[1]] = '-'
            else:
                if windowList.selection_mode == 1:
                    windowList.selection_mode = 0
                elif windowList.selection_mode == 0:
                    windowList.selection_mode = 1
                if windowList.id_selected[0] == 1:
                    global new_name
                    windowList.active = False
                    new_name = InputText(windowList.win, windowList.width_col[0] + windowList.x_col + 1, windowList.y_col +
                                         windowList.window_select_position + 1, windowList.width_col[1], 1, cursor,
                                         windowList.data[windowList.id_selected[0]][windowList.id_selected[1]])
                    new_name.print_string()
                    set_key = 'rename'
                if windowList.id_selected[0] == 3:
                    global new_x
                    windowList.active = False
                    x = windowList.x_col
                    for i in range(windowList.id_selected[0]):
                        x += windowList.width_col[i]
                        if i != len(windowList.data) - 1:
                            x += 1
                    new_x = InputText(windowList.win, x, windowList.y_col + windowList.window_select_position + 1,
                                      windowList.width_col[windowList.id_selected[0]], 1, cursor, windowList.data[windowList.id_selected[0]][windowList.id_selected[1]])
                    new_x.print_string()
                    set_key = 'change_x'
                if windowList.id_selected[0] == 4:
                    global new_y
                    windowList.active = False
                    x = windowList.x_col
                    for i in range(windowList.id_selected[0]):
                        x += windowList.width_col[i]
                        if i != len(windowList.data) - 1:
                            x += 1
                    new_y = InputText(windowList.win, x, windowList.y_col + windowList.window_select_position + 1,
                                      windowList.width_col[windowList.id_selected[0]], 1, cursor, windowList.data[windowList.id_selected[0]][windowList.id_selected[1]])
                    new_y.print_string()
                    set_key = 'change_y'

    elif set_key == 'rename':
        name = new_name.update_string(key)
        if type(name) == str:
            allwin[windowList.id_selected[1]].name = name
            windowList.active = True
            windowList.selection_mode = 0
            set_key = 'switchWindows'
    elif set_key == 'change_x':
        if key == 259 or key == 258:
            if key == 259:
                movewin(allwin[windowList.id_selected[1]], None, [allwin[windowList.id_selected[1]].y,
                                                                  allwin[windowList.id_selected[1]].x + 1])
            elif key == 258:
                movewin(allwin[windowList.id_selected[1]], None, [allwin[windowList.id_selected[1]].y,
                                                                  allwin[windowList.id_selected[1]].x - 1])
            windowList.active = True
            new_x.string = str(allwin[windowList.id_selected[1]].x)
            new_x.update_cursor()
        else:
            windowList.active = False
            name = new_x.update_string(key)
            if type(name) == str:
                try:
                    movewin(allwin[windowList.id_selected[1]], None, [allwin[windowList.id_selected[1]].y, int(name)])
                    windowList.active = True
                    windowList.selection_mode = 0
                    set_key = 'switchWindows'
                except:
                    beep()
    elif set_key == 'change_y':
        if key == 259 or key == 258:
            if key == 259:
                movewin(allwin[windowList.id_selected[1]], None, [allwin[windowList.id_selected[1]].y + 1,
                                                                  allwin[windowList.id_selected[1]].x])
            elif key == 258:
                movewin(allwin[windowList.id_selected[1]], None, [allwin[windowList.id_selected[1]].y - 1,
                                                                  allwin[windowList.id_selected[1]].x])
            windowList.active = True
            new_y.string = str(allwin[windowList.id_selected[1]].y)
            new_y.update_cursor()
        else:
            windowList.active = False
            name = new_y.update_string(key)
            if type(name) == str:
                try:
                    int(name)
                    movewin(allwin[windowList.id_selected[1]], None, [int(name), allwin[windowList.id_selected[1]].x])
                    windowList.active = True
                    windowList.selection_mode = 0
                    set_key = 'switchWindows'
                except:
                    beep()

    return set_key






allwin.append(Window(name='win' + str(len(allwin))))
nowwin = len(allwin) - 1
focus = allwin[nowwin]
windowList = SwitchObjects('windowList', 8, 22, 17, 0, False, False)
windowList.set_params(0, 0, 1, 1, 5, 2, 4, 5, 2, 2)
windowList.update_switch_object([[str(i) for i in range(len(allwin))], [i.name for i in allwin], [str(i.is_visible) for i in allwin],
                                   [str(i.x) for i in allwin], [str(i.y) for i in allwin]],
                                [0, nowwin], ['N*', 'name', 'show', 'x', 'y'])
for i in range(len(allwin)):
        mvwaddstr(allwin[i].win, 1, 1, str(allwin[i].name))

update_panels()
doupdate()



while 1:
    windowList.data[0] = [str(i) for i in range(len(allwin))]
    key = int(getch())
    key_action(key)
    if windowList.active:
        windowList.update_switch_object([windowList.data[0], [i.name for i in allwin], [str(i.is_visible) for i in allwin],
                                       [str(i.x) for i in allwin], [str(i.y) for i in allwin]], [windowList.id_selected[0], nowwin])
    for i in reversed(range(len(allwin))):
        if allwin[i].is_visible:
            mvwaddstr(allwin[i].win, 1, 1, str(allwin[i].name))
            top_panel(allwin[i].panel)
    if windowList.is_visible:
        top_panel(windowList.panel)


    update_panels()
    doupdate()





getch()
input()