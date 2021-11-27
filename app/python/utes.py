# utes.py

import tkinter as tk
import dev_tools as dt
from dev_tools import looky, seeline

# capitalize right
def titlize(stg):
    '''
        function by Yugal Jindle. Python's `title()` method doesn't work right
        if there are apostrophes etc. in the word, since it breaks words at
        punctuation. According to https://bugs.python.org/issue7008, the
        `string.capwords()` method is also buggy and should be deprecated. This
        is to make "Linda's Tree" not be "Linda'S Tree".
    '''
    lst = []
    for temp in stg.split(" "): lst.append(temp.capitalize())
    return ' '.join(lst)

# CENTERING

# def center_window(win):
    # '''
    # Code by Honest Abe at StackOverflow.
    # Centers a window in the screen taking account of non-tk elements.
    # Doesn't currently work with resize_window() and/or resize_scrollbar().
    # '''
    # win.update_idletasks()
    # width = win.winfo_reqwidth()
    # frm_width = win.winfo_rootx() - win.winfo_x()
    # win_width = width + 2 * frm_width
    # height = win.winfo_reqheight()
    # titlebar_height = win.winfo_rooty() - win.winfo_y()
    # win_height = height + titlebar_height + frm_width
    # x = win.winfo_screenwidth() // 2 - win_width // 2
    # y = win.winfo_screenheight() // 2 - win_height // 2
    # win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def center_dialog(dlg, frame=None):

    if frame:
        dlg.update_idletasks()
        win_width = frame.winfo_reqwidth()
        win_height = frame.winfo_reqheight()
        right_pos = int(dlg.winfo_screenwidth()/2 - win_width/2)
        down_pos = int(dlg.winfo_screenheight()/2 - win_height/2)
    else:
        dlg.update_idletasks()
        win_width = dlg.winfo_reqwidth()
        win_height = dlg.winfo_reqheight()
        right_pos = int(dlg.winfo_screenwidth()/2 - win_width/2)
        down_pos = int(dlg.winfo_screenheight()/2 - win_height/2)
    print("line", looky(seeline()).lineno, "right_pos, down_pos:", right_pos, down_pos)
    dlg.geometry("+{}+{}".format(right_pos, down_pos))

# def center_dialog(dlg, frame=None):

    # if frame:
        # dlg.update_idletasks()
        # win_width = frame.winfo_reqwidth()
        # win_height = frame.winfo_reqheight()
        # right_pos = int(dlg.winfo_screenwidth()/2 - win_width/2)
        # down_pos = int(dlg.winfo_screenheight()/2 - win_height/2)
    # else:
        # dlg.update_idletasks()
        # win_width = dlg.winfo_reqwidth()
        # win_height = dlg.winfo_reqheight()
        # right_pos = int(dlg.winfo_screenwidth()/2 - win_width/2)
        # down_pos = int(dlg.winfo_screenheight()/2 - win_height/2)
    # print("line", looky(seeline()).lineno, "right_pos, down_pos:", right_pos, down_pos)
    # return right_pos, down_pos 

#   -   -   -   see widgets.py for statusbar tooltips   -   -   -   #

class ToolTip(object):
    '''
        TOOLTIPS BY MICHAEL FOORD 
        (used for ribbon menu icons and widgets dynamically gridded). 
        Don't use for anything that'll be destroyed by clicking because
        tooltips are displayed by pointing w/ mouse and thus a tooltip 
        will be displaying when destroy takes place thus leaving the 
        tooltip on the screen since the FocusOut that is supposed to 
        destroy the tooltip can't take place.
    '''

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        ''' Display text in tooltip window '''

        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 27
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        try:
            # For Mac OS
            tw.tk.call("::tk::unsupported::MacWindowStyle",
                       "style", tw._w,
                       "help", "noActivates")
        except tk.TclError:
            pass
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                      background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                      font=("tahoma", 10, "normal"),
                      fg='black')
        label.pack(ipadx=6)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()    

def create_tooltip(widget, text):
    ''' Call w/ arguments to use M. Foord's ToolTip class. '''
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()

    toolTip = ToolTip(widget)
    widget.bind('<Enter>', enter, add="+")
    widget.bind('<Leave>', leave, add="+")

#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   #

# make a canvas scroll with mousewheel
def scroll_on_mousewheel(evt, canvas):
    canvas.yview_scroll(int(-1*(evt.delta/120)), 'units')

# Tkinter keysyms for keys that actually type a character with len(keysym) > 1:

OK_PRINT_KEYS = (
    "space",
    "parenleft",
    "parenright",
    "underscore",
    "minus",
    "asterisk",
    "slash",
    "period",
    "comma",
    "equal",
    "plus",
    "ampersand",
    "asciicircum",
    "percent",
    "dollar",
    "numbersign",
    "at",
    "exclam",
    "asciitilde",
    "quoteleft",
    "bar",
    "backslash",
    "less",
    "greater",
    "colon",
    "semicolon",
    "quotedbl",
    "quoteright",
    "bracketleft",
    "braceleft",
    "bracketright",
    "braceright",
)