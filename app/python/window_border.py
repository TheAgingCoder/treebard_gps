# window_border.py

import tkinter as tk
import sqlite3
from files import get_current_file, app_path, global_db_path, set_closing
from widgets import (
    LabelButtonImage, Frame, FrameTitleBar, LabelTitleBar, Toplevel, Canvas, 
    FrameHilited3) 
from toykinter_widgets import StatusbarTooltips
from styles import make_formats_dict, NEUTRAL_COLOR, config_generic
from utes import center_dialog
from query_strings import select_format_font_size
from PIL import Image, ImageTk
import dev_tools as dt
from dev_tools import looky, seeline



def close(evt):
    dlg = evt.widget.winfo_toplevel()
    if dlg.winfo_name() == 'tk':
        set_closing()
        dlg.quit()
    else:
        dlg.grab_release()
        dlg.destroy()

class Border(Canvas):

    pool = []

    def __init__(
            self, master, root, formats, menubar=False, 
            ribbon_menu=False, *args, **kwargs):
        Canvas.__init__(self, master, *args, **kwargs)

        '''
            This class replaces root and dialog borders with custom borders. 

            Since this custom "Toykinter" border is part of the app instead 
            of being controlled by Windows, its use allows clicks on the title 
            bar to be responded to with standard Tkinter configuration methods 
            and other Python code. 

            This class can't use Treebard as a master since Treebard is the 
            whole app and is only instantiated once, so this class has to use 
            its host toplevel as parent. Setting font size should change the 
            size of fonts, title bar, and max/min/quit buttons. The settings 
            are 3, 4, 7, or 11 pixels. The size shown is linked to changes in 
            font size (in progress--user still has to switch to person tab and
            redraw() to see change).

            The hard part to remember when using this is that the parts of the
            border including the canvas itself (`self` in the class) are gridded
            in this class. This causes confusion because I'm always trying to
            figure out where to grid the canvas and how to set columnconfigure()
            and rowconfigure() but it's already done here since it has to be
            the same wherever it's used. Also the dropdown menu and icon menu
            occupy rows 2 and 3 whether they're used or not, and they're only
            used in the root window.
        '''

        self.master = master # toplevel
        self.root = root
        self.formats = formats
        self.menubar = menubar
        self.ribbon_menu = ribbon_menu

        self.set_title_bar_size()

        self.changing_values = None
        self.maxxed = False

        self.make_widgets()

        self.BORDER_PARTS = (
            self.title_bar, self.title_frame, self.logo, self.title_1, 
            self.title_1b, self.title_2, self.txt_frm, self.buttonbox, 
            self.border_top, self.border_left, self.border_right, 
            self.border_bottom)

        Border.pool.append(self)
        if self.master.winfo_name() != "tk":
            self.master.bind("<Destroy>", self.clean_pool)
        self.colorize_border()

    def clean_pool(self, evt):
        '''
            Delete destroyed toplevel from list and highlight the title bar
            of the toplevel that's uppermost in the window stacking order.
        '''
        widg = evt.widget
        if (widg.winfo_class() == "Canvas" and 
                widg.winfo_subclass() == "Border"):
            idx = Border.pool.index(widg)
            del Border.pool[idx]
        if len(Border.pool) != 0: # hack to use Dialogue class in misc test module
            Border.pool[0].colorize_border()

    def set_title_bar_size(self):
        sizes = { 
            3 : ['tiny', 20, 0.25], 
            4 : ['small', 25, 0.75], 
            7 : ['medium', 31, 0.25], 
            11 : ['large', 45, 1.0]}

        current_file = get_current_file()[0]
        conn = sqlite3.connect(current_file)
        cur = conn.execute(select_format_font_size)
        font_size = cur.fetchone()
        cur.close()
        conn.close()

        if font_size[0] is None:
            font_size = font_size[1]
        else:
            font_size = font_size[0]
        if font_size < 11:
            self.size = 3
        elif font_size < 14:
            self.size = 4
        elif font_size < 20:
            self.size = 7
        elif font_size < 30:
            self.size = 11         

        for k,v in sizes.items():
            if self.size == k:
                self.icon_size = v[0]
                self.offset_x = v[1]
                self.rel_y = v[2]

    def make_widgets(self):

        self.border_top = FrameTitleBar(
            self.master, height=3, name='top')
        self.title_bar = FrameTitleBar(self.master)

        self.menu_frame = FrameHilited3(self.master)
        self.ribbon_frame = FrameHilited3(self.master)

        self.border_left = FrameTitleBar(self.master, width=3, name='left')
        self.border_right = FrameTitleBar(self.master, width=3, name='right')

        self.statusbar = StatusbarTooltips(self.master, self.formats)

        self.border_bottom = FrameTitleBar(
            self.master, height=3, name='bottom')

        self.border_top.config(cursor='sb_v_double_arrow')
        self.border_left.config(cursor='sb_h_double_arrow')
        self.border_right.config(cursor='sb_h_double_arrow')
        self.border_bottom.config(cursor='sb_v_double_arrow')

        # children of toplevel i.e. self.master
        self.master.columnconfigure(1, weight=1)
        self.master.rowconfigure(4, weight=1)
        self.border_top.grid(column=0, row=0, columnspan=4, sticky='ew')
        self.title_bar.grid(column=1, row=1, columnspan=2, sticky='ew')
        if self.menubar is True:
            self.menu_frame.grid(column=1, row=2, columnspan=2, sticky='ew')
        if self.ribbon_menu is True:
            self.ribbon_frame.grid(column=1, row=3, columnspan=2, sticky='w')
        self.grid(column=1, row=4, sticky='news')
        self.border_left.grid(column=0, row=1, rowspan=6, sticky='ns')
        self.border_right.grid(column=3, row=1, rowspan=6, sticky='ns')
        self.statusbar.grid(column=1, row=6, columnspan=2, sticky='ew')
        self.border_bottom.grid(column=0, row=7, columnspan=4, sticky='ew')

        self.config(cursor='arrow')

        # children of self.title_bar
        self.title_bar.columnconfigure(0, weight=1)
        self.title_bar.columnconfigure(1, weight=0)
        self.title_frame = FrameTitleBar(self.title_bar)
        self.buttonbox = FrameTitleBar(self.title_bar)

        self.title_frame.pack(side='left')
        self.buttonbox.place(relx=1.0, x=-100, rely=0.125, y=-2)

        # children of self.title_frame
        self.logo = TitleBarButtonSolidBG(
            self.title_frame,
            self.formats,
            icon='logo',
            icon_size=self.icon_size)

        self.txt_frm = FrameTitleBar(self.title_frame)
        self.logo.pack(side='left', pady=(0,3), padx=(0,12))
        self.txt_frm.pack(side='left')

        # children of text_frm
        self.title_1 = LabelTitleBar(
            self.txt_frm, 
            size=self.icon_size,
            text='Toykinter Demo')
        self.title_1b = FrameTitleBar(self.txt_frm, width=36)
        self.title_2 = LabelTitleBar(
            self.txt_frm,
            size=self.icon_size, 
            text='for all ages')

        self.title_1.grid(column=0, row=0)
        self.title_1b.grid(column=1, row=0, sticky='ew')
        self.title_2.grid(column=2, row=0)

        # children of self.buttonbox
        self.minn = TitleBarButton(
            self.buttonbox, icon='min', icon_size=self.icon_size)
        self.maxx = TitleBarButton(
            self.buttonbox, icon='max', icon_size=self.icon_size)
        self.restore = TitleBarButton(
            self.buttonbox, icon='restore', icon_size=self.icon_size)
        self.quitt = TitleBarButton(
            self.buttonbox, icon='quit', icon_size=self.icon_size)

        self.minn.grid(column=0, row=0, sticky='w')
        self.maxx.grid(
            column=1, row=0, sticky='w', padx=(0,3))
        self.restore.grid(
            column=1, row=0, sticky='w', padx=(0,3))
        self.restore.grid_remove()
        self.quitt.grid(
            column=2, row=0, sticky='e', 
            padx=(0, self.size))

        self.master.update_idletasks()
        to_the_left = self.buttonbox.winfo_reqwidth()
        self.buttonbox.place(relx=1.0, x=-to_the_left, rely=0.125, y=-2 * self.rel_y)

        # bindings
        self.master.bind('<Map>', self.hide_windows_titlebar)
        self.minn.bind('<Button-1>', self.minimize)
        self.maxx.bind('<Button-1>', self.toggle_max_restore)
        self.restore.bind('<Button-1>', self.toggle_max_restore)
        self.quitt.bind('<Button-1>', close)
        x = [i.bind(
            '<Map>', 
            self.recolorize_on_restore) for i in (self.minn, self.quitt)]

        for widg in (
                self.title_bar, self.title_frame, self.logo, self.title_1, 
                self.title_1b, self.title_2, self.txt_frm, self.buttonbox):
            widg.bind('<B1-Motion>', self.move_window)
            widg.bind('<Button-1>', self.get_pos)
            widg.bind('<Double-Button-1>', self.toggle_max_restore) 

        for widg in (
                self.border_top, self.border_left, 
                self.border_right, self.border_bottom):
            widg.bind('<Button-1>', self.start_edge_sizer)
            widg.bind('<B1-Motion>', self.stop_edge_sizer)
            widg.bind('<ButtonRelease-1>', self.stop_edge_sizer)

    def recolorize_on_restore(self, evt):
        evt.widget.config(bg=NEUTRAL_COLOR)

    def move_window(self, evt):
        ''' Drag the window by the title frame
        '''
        self.master.update_idletasks()
        x_mouse_move_screen = evt.x_root
        y_mouse_move_screen = evt.y_root
        new_x = x_mouse_move_screen + self.adjust_x
        new_y = y_mouse_move_screen + self.adjust_y

        evt.widget.winfo_toplevel().geometry('+{}+{}'.format(new_x, new_y))

    def get_pos(self, evt):
        ''' Prepare to drag the window by the title frame. '''
        evt.widget.winfo_toplevel().lift()
        self.colorize_border()
        
        left_edge = self.master.winfo_rootx()
        top_edge = self.master.winfo_rooty()
        x_click_screen = evt.x_root
        y_click_screen = evt.y_root

        self.adjust_x = left_edge - x_click_screen
        self.adjust_y = top_edge - y_click_screen

    def toggle_max_restore(self, evt):
        '''
            When window is maximized, change window border button
            to restore down and vice versa. Have to return the
            Windows title bar first or Tkinter won't let it be
            maximized.
        '''

        if self.maxxed is False:
            self.maxxed = True
            self.init_geometry = evt.widget.winfo_toplevel().geometry()
            self.maxx.grid_remove()
            self.restore.grid()
            self.restore.config(bg=NEUTRAL_COLOR)
            self.maximize(evt)
        elif self.maxxed is True:
            self.maxxed = False
            self.restore.grid_remove()
            self.maxx.grid()
            self.maxx.config(bg=NEUTRAL_COLOR)
            self.restore_down(evt)

    def minimize(self, evt):
        '''
            Withdraw so return of Windows titlebar isn't visible.
            Return Windows titlebar so window can be iconified.
        '''        
        dlg = evt.widget.winfo_toplevel()
        dlg.withdraw() # this hides it
        self.master.update_idletasks()
        dlg.overrideredirect(0)
        dlg.iconify() # this provides a taskbar icon to re-open it

    def hide_windows_titlebar(self, evt):
        self.update_idletasks()
        self.master.overrideredirect(1)

    def split_geometry_string(self, window):
        xy = window.geometry().split('+')
        wh = xy.pop(0).split('x')
        return int(wh[0]), int(wh[1]), int(xy[0]), int(xy[1])
       
    def maximize(self, evt):
        dlg = evt.widget.winfo_toplevel()
        self.master.update_idletasks()
        dlg.overrideredirect(0)
        dlg.attributes('-fullscreen', True)

    def restore_down(self, evt):
        dlg = evt.widget.winfo_toplevel()
        dlg.attributes('-fullscreen', False)
        dlg.geometry(self.init_geometry)

    def start_edge_sizer(self, evt):

        def pass_values():
            values =  (
                resizee, init_geometry, click_down_x, click_down_y, 
                orig_pos_x, orig_pos_y)
            return values

        resizee = evt.widget.winfo_toplevel()
        init_geometry = resizee.geometry()
        
        (click_down_x, click_down_y) = resizee.winfo_pointerxy()

        orig_pos_x = resizee.winfo_rootx()
        orig_pos_y = resizee.winfo_rooty()

        self.changing_values = pass_values()

    def stop_edge_sizer(self, evt):

        values = self.changing_values
        resizee = values[0]
        init_geometry = values[1]
        click_down_x = values[2]
        click_down_y = values[3]
        orig_pos_x = values[4]
        orig_pos_y = values[5]

        click_up_x = click_down_x  
        click_up_y = click_down_y
        new_pos_x = orig_pos_x
        new_pos_y = orig_pos_y

        klikt = evt.widget 

        xy = init_geometry.split('+')
        wh = xy.pop(0).split('x')

        new_w = orig_wd = int(wh[0])
        new_h = orig_ht = int(wh[1])  

        click_up_x = resizee.winfo_pointerx() 
        click_up_y = resizee.winfo_pointery()

        dx = click_down_x - click_up_x
        dy = click_down_y - click_up_y
        if klikt.winfo_name() == 'left':
            new_w = orig_wd + dx
            new_pos_x = orig_pos_x - dx
        elif klikt.winfo_name() == 'right':
            new_w = orig_wd - dx
        elif klikt.winfo_name() == 'top':
            new_h = orig_ht + dy
            new_pos_y = orig_pos_y - dy
        elif klikt.winfo_name() == 'bottom':
            new_h = orig_ht - dy

        if new_w < 10:
            new_w = 10
        if new_h < 10:
            new_h = 10
        resizee.geometry('{}x{}+{}+{}'.format(
            new_w, new_h, new_pos_x, new_pos_y))

    def colorize_border(self):
        '''
            Runs whenever title bar is clicked, called in get_pos().
        '''

        self.formats = make_formats_dict()
        for widg in self.BORDER_PARTS:
            widg.config(bg=self.formats['head_bg'])
        for widg in (self.title_1, self.title_2):
            widg.config(fg=self.formats['fg'])
        for border in Border.pool:
            if border != self:
                for widg in border.BORDER_PARTS:
                    widg.config(bg=NEUTRAL_COLOR)                    
            else:
                # Move active toplevel to the top of the list so it will be 
                #   highlighted by clean_pool() when a toplevel is destroyed.
                idx = Border.pool.index(border)
                Border.pool.insert(0, Border.pool.pop(idx))

class TitleBarButton(LabelButtonImage):
    def __init__(self, master, icon='', icon_size='tiny', *args, **kwargs):
        LabelButtonImage.__init__(self, master, *args, **kwargs)
        '''
            The icons are 32x32 but they can be set to any integer size
            between 12 and 32 and a thumbnail will be displayed if less 
            than 32. But sizes between 22 and 30 make a bad X for some
            reason. Sizes 12, 16, 21, and 32 look best so I've hard-coded
            it with those four size options only. (Using Pillow...)

            This class is for buttons with transparent backgrounds so it
            uses my standard neutral color #878787 which doesn't change.
            For buttons with darker colors filling the whole button, 
            #a8afc4 might show as a bright border contrasting too much
            with the image on the button, so a class has been inherited
            from this one which has a darker background color.
        '''

        font_icon_file = {
            'tiny' : (
                10, '{}images/icons/{}_{}.png'.format(app_path, icon, 12)), 
            'small' : (
                12, '{}images/icons/{}_{}.png'.format(app_path, icon, 17)), 
            'medium' : (
                14, '{}images/icons/{}_{}.png'.format(app_path, icon, 21)), 
            'large' : (
                18, '{}images/icons/{}_{}.png'.format(app_path, icon, 32))}

        for k,v in font_icon_file.items():
            if icon_size == k:
                icon_size = v[0]
                file = v[1]
        img = Image.open(file)
        self.tk_img = ImageTk.PhotoImage(img, master=master)

        self.config(
            font=('arial', icon_size, 'bold'), 
            bd=2, 
            relief='raised',
            bg=NEUTRAL_COLOR,
            image=self.tk_img)

class TitleBarButtonSolidBG(TitleBarButton):
    def __init__(self, master, formats, *args, **kwargs):
        TitleBarButton.__init__(self, master, *args, **kwargs)
        '''
            For buttons with a solid image and darker color
            backgrounds so a bright border doesn't show through
            around the edge of the image.
        '''
        self.config(bg=formats['highlight_bg'])

class Dialogue(Toplevel):
    '''
        Generic unscrolled dialogue with Toykinter border. Border class is a
        Canvas which is gridded in its home class. Rows are reserved for the
        menu bar and icon ribbon menu although usually not used so they are
        False by default, but their unused rows have to be taken into account
        (ignored) here. This is used for error messages and small dialogs which
        don't change size and will never need to scroll.
    '''

    def __init__(self, master, *args, **kwargs):
        Toplevel.__init__(self, master, *args, **kwargs)

        formats = make_formats_dict()
        self.withdraw()
        self.columnconfigure(1, weight=1)
        self.canvas = Border(self, master, formats)
        self.window = Frame(self.canvas)
        self.canvas.create_window(0, 0, anchor='nw', window=self.window)

    def resize_window(self):
        """ Call this to show the dialog. Added to requested width and height 
            are allowances for widgets not in self.window such as borders, 
            title bar, and status bar.
        """
        self.update_idletasks()    
        width = self.window.winfo_reqwidth() + 6
        height = self.window.winfo_reqheight() + 42
        self.geometry("{}x{}".format(width, height))
        center_dialog(self)
        self.deiconify()






 
