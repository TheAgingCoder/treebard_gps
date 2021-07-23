# widgets.py

import tkinter as tk
from tkinter import ttk
import sqlite3
from files import current_drive, project_path
from tkinter import messagebox
from styles import make_formats_dict, NEUTRAL_COLOR
from utes import create_tooltip
from query_strings import select_current_person_id    
import dev_tools as dt
from dev_tools import looky, seeline



formats = make_formats_dict()

# print('formats is', formats)
# formats is {'bg': '#34615f', 'highlight_bg': '#4a8a87', 'head_bg': '#486a8c', 'fg': '#b9ddd9', 'output_font': ('courier', 16), 'input_font': ('tahoma', 16), 'heading1': ('courier', 32, 'bold'), 'heading2': ('courier', 24, 'bold'), 'heading3': ('courier', 17, 'bold'), 'heading4': ('courier', 13, 'bold'), 'status': ('tahoma', 13), 'boilerplate': ('tahoma', 10), 'show_font': ('tahoma', 16, 'italic'), 'titlebar_0': ('tahoma', 10, 'bold'), 'titlebar_1': ('tahoma', 14, 'bold'), 'titlebar_2': ('tahoma', 16, 'bold'), 'titlebar_3': ('tahoma', 20, 'bold'), 'titlebar_hilited_0': ('tahoma', 10), 'titlebar_hilited_1': ('tahoma', 14), 'titlebar_hilited_2': ('tahoma', 16), 'titlebar_hilited_3': ('tahoma', 20), 'unshow_font': ('tahoma', 14, 'italic')}

class Framex(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        pass

    def winfo_subclass(self):
        ''' 
            Like built-in tkinter method
            w.winfo_class() except it gets subclass names.
        '''
        subclass = type(self).__name__
        return subclass

class FrameStay(Framex):
    ''' 
        Frame background color will not change when color scheme changes.
    '''

    def __init__(self, master, *args, **kwargs):
        Framex.__init__(self, master, *args, **kwargs)
        pass

class Frame(Framex):
    ''' 
        Frame background color changes when color scheme changes. 
    '''

    def __init__(self, master, *args, **kwargs):
        Framex.__init__(self, master, *args, **kwargs)

        self.config(bg=formats['bg'])

class FrameTest(Framex):
    ''' 
        Frame background color can be altered for testing/visibility. 
    '''

    def __init__(self, master, *args, **kwargs):
        Framex.__init__(self, master, *args, **kwargs)
        self.config(bg='orange')

class FrameTest2(Framex):
    ''' 
        Frame background color can be altered for testing/visibility. 
    '''

    def __init__(self, master, *args, **kwargs):
        Framex.__init__(self, master, *args, **kwargs)
        self.config(bg='green')

class FrameTitleBar(Framex):
    ''' 
        Frame hilited by border and a different background color.
    '''

    def __init__(self, master, *args, **kwargs):
        Framex.__init__(self, master, *args, **kwargs)
        self.config(bg=NEUTRAL_COLOR)


class FrameHilited(Framex):
    ''' 
        Frame hilited by groove border and background color.
    '''

    def __init__(self, master, *args, **kwargs):
        Framex.__init__(self, master, *args, **kwargs)
        self.config(bg=formats['highlight_bg'], bd=3, relief='groove')

class FrameHilited1(Framex):
    ''' 
        Used for narrow resizing sash on left edge of
        attributes table. Could be used as vertical 
        separator.
    '''

    def __init__(self, master, *args, **kwargs):
        Framex.__init__(self, master, *args, **kwargs)
        self.config(bg=formats['highlight_bg'], bd=6, relief='ridge')

class FrameHilited2(Framex):
    ''' 
        Frame hilited by border and a different background color.
    '''

    def __init__(self, master, *args, **kwargs):
        Framex.__init__(self, master, *args, **kwargs)
        self.config(bg=formats['head_bg'])

class FrameHilited3(Framex):
    ''' 
        Frame hilited by different background color but not border.
    '''

    def __init__(self, master, *args, **kwargs):
        Framex.__init__(self, master, *args, **kwargs)
        self.config(bg=formats['highlight_bg'])

class FrameHilited4(Framex):
    ''' 
        Frame hilited by sunken border and background color.
    '''

    def __init__(self, master, *args, **kwargs):
        Framex.__init__(self, master, *args, **kwargs)
        self.config(bg=formats['highlight_bg'], bd=2, relief='sunken')

class FrameHilited5(Framex):
    ''' 
        Frame hilited by sunken border and background color.
    '''

    def __init__(self, master, *args, **kwargs):
        Framex.__init__(self, master, *args, **kwargs)
        self.config(bg=formats['highlight_bg'], bd=1, relief='solid')

class LabelFramex(tk.LabelFrame):
    def __init__(self, master, *args, **kwargs):
        tk.LabelFrame.__init__(self, master, *args, **kwargs)
        pass

    def winfo_subclass(self):
        ''' 
            Like built-in tkinter method
            w.winfo_class() except it gets subclass names.
        '''
        subclass = type(self).__name__
        return subclass

class LabelFrame(LabelFramex):
        def __init__(self, master, *args, **kwargs):
            LabelFramex.__init__(self, master, *args, **kwargs)

            self.config(
                bg=formats['bg'], 
                fg=formats['fg'], 
                font=formats['output_font']) 

class Messagex(tk.Message):
    def __init__(self, master, *args, **kwargs):
        tk.Message.__init__(self, master, *args, **kwargs)
        pass

    def winfo_subclass(self):
        ''' 
            Like built-in tkinter method
            w.winfo_class() except it gets subclass names.
        '''
        subclass = type(self).__name__
        return subclass

class Message(Messagex):
    def __init__(self, master, *args, **kwargs):
        Messagex.__init__(self, master, *args, **kwargs)

        self.config(
            bg=formats['bg'], fg=formats['fg'], font=formats['output_font'])

class MessageHilited(Messagex):
    def __init__(self, master, *args, **kwargs):
        Messagex.__init__(self, master, *args, **kwargs)

        self.config(
            bd=3, relief='raised',
            bg=formats['highlight_bg'], 
            fg=formats['fg'], 
            font=formats['output_font']) 
      
class Labelx(tk.Label):
    def __init__(self, master, *args, **kwargs):
        tk.Label.__init__(self, master, *args, **kwargs)

    def winfo_subclass(self):
        ''' a method that works like built-in tkinter method
            w.winfo_class() except it gets subclass names
            of widget classes custom-made by inheritance '''
        subclass = type(self).__name__
        return subclass

class Label(Labelx):
    ''' 
        If this subclass is detected it will be reconfigured
        according to user preferences. 
    '''
    def __init__(self, master, *args, **kwargs):
        Labelx.__init__(self, master, *args, **kwargs)
        self.config(
            bg=formats['bg'], 
            fg=formats['fg'],
            font=formats['output_font'])

class LabelTest(Labelx):
    ''' 
        Color can be changed for testing/visibility. 
    '''

    def __init__(self, master, *args, **kwargs):
        Labelx.__init__(self, master, *args, **kwargs)
        self.config(
            bg='purple', 
            fg=formats['fg'],
            font=formats['output_font'])
 
class LabelItalic(Labelx):
    ''' 
        Uses input font and italics to display errors & such. 
    '''

    def __init__(self, master, *args, **kwargs):
        Labelx.__init__(self, master, *args, **kwargs)
        self.config(
            bg=formats['bg'],
            fg=formats['fg'],
            font=formats['show_font'])

class LabelHilited(Labelx):
    ''' 
        Like Label with a different background.  
    '''
    def __init__(self, master, *args, **kwargs):
        Labelx.__init__(self, master, *args, **kwargs)

        self.formats = make_formats_dict()

        self.config(
            bg=self.formats['highlight_bg'], 
            fg=self.formats['fg'],
            font=self.formats['output_font'])

    def highlight(self, evt):
        self.config(bg=self.formats['head_bg'])

    def unhighlight(self, evt):
        self.config(bg=self.formats['highlight_bg'])


class LabelHilited2(Labelx):
    ''' 
        Like Label with a different background. 
    '''
    def __init__(self, master, *args, **kwargs):
        Labelx.__init__(self, master, *args, **kwargs)

        self.config(
            bg=formats['head_bg'], 
            fg=formats['fg'],
            font=formats['output_font'])

class LabelTip(LabelHilited):
    ''' 
        Like Label with a different background. For tooltips. 
    '''
    def __init__(self, master, *args, **kwargs):
        LabelHilited.__init__(self, master, *args, **kwargs)
        self.config(font=formats['status'], bd=0, relief='solid')

class LabelTip2(LabelHilited2):
    ''' 
        Like Label with a different background. For tooltips. 
    '''
    def __init__(self, master, *args, **kwargs):
        LabelHilited2.__init__(self, master, *args, **kwargs)
        self.config(font=formats['status'], bd=1, relief='solid')

class LabelTipBold(LabelHilited):
    ''' 
        Like Label with a different background. 
    '''
    def __init__(self, master, *args, **kwargs):
        LabelTip.__init__(self, master, *args, **kwargs)
        self.config(font=formats['titlebar_1'])

class LabelNegative(Labelx):
    ''' 
        Usual bg and fg reversed. 
    '''
    def __init__(self, master, *args, **kwargs):
        Labelx.__init__(self, master, *args, **kwargs)
        self.config(
            bg=formats['fg'], 
            fg=formats['bg'],
            font=formats['output_font'])

class LabelH1(Label):
    ''' 
        For largest subheadings. 
    '''
    def __init__(self, master, *args, **kwargs):
        Label.__init__(self, master, *args, **kwargs)

        self.config(font=formats['heading1'])


class LabelH2(Label):
    ''' 
        For large subheadings. 
    '''
    def __init__(self, master, *args, **kwargs):
        Label.__init__(self, master, *args, **kwargs)

        self.config(font=formats['heading2'])

class LabelH3(Label):
    ''' 
        For small subheadings. 
    '''
    def __init__(self, master, *args, **kwargs):
        Label.__init__(self, master, *args, **kwargs)

        self.config(font=formats['heading3'])

class LabelH4(Label):
    ''' 
        For tiny subheadings. 
    '''
    def __init__(self, master, *args, **kwargs):
        Label.__init__(self, master, *args, **kwargs)

        self.config(font=formats['heading4'])

class LabelButtonImage(Labelx):
    ''' 
        A label that looks and works like a button. Good for
        images since it sizes itself to its contents, so don't
        add width and height to this class or change its color.
    '''

    def __init__(self, master, *args, **kwargs):
        Labelx.__init__(self, master, *args, **kwargs)

        self.bind('<FocusIn>', self.show_focus)
        self.bind('<FocusOut>', self.unshow_focus)
        self.bind('<Button-1>', self.on_press)
        self.bind('<ButtonRelease-1>', self.on_release)
        self.bind('<Enter>', self.on_hover)
        self.bind('<Leave>', self.on_unhover)

    def show_focus(self, evt):
        self.config(borderwidth=2)

    def unshow_focus(self, evt):
        self.config(borderwidth=1)

    def on_press(self, evt):
        formats = make_formats_dict()
        self.config(relief='sunken', bg=formats['head_bg'])

    def on_release(self, evt):
        formats = make_formats_dict()
        self.config(relief='raised', bg=formats['bg'])

    def on_hover(self, evt):
        self.config(relief='groove')

    def on_unhover(self, evt):
        self.config(relief='raised')

class LabelButtonText(LabelButtonImage):
    ''' 
        A label that looks and works like a button. Displays Text.
    '''

    def __init__(self, master, width=8, *args, **kwargs):
        LabelButtonImage.__init__(self, master, *args, **kwargs)

        self.config(
            anchor='center',
            borderwidth=1, 
            relief='raised', 
            takefocus=1,
            bg=formats['bg'],
            width=width,
            font=formats['input_font'],
            fg=formats['fg'])

class LabelDots(LabelButtonText):
    ''' 
        Display clickable dots if more info, no dots 
        if no more info. 
    '''
    def __init__(
            self, 
            master,
            current_file,
            dialog_class,
            *args, **kwargs):
        LabelButtonText.__init__(self, master, *args, **kwargs)

        self.master = master
        self.root = master.master
        self.dialog_class = dialog_class

        self.finding_id = None
        self.header = None
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        cur.execute(select_current_person_id)
        self.current_person = cur.fetchone()[0]
        self.config(width=5, font=formats['heading3'])
        self.bind('<Button-1>', self.open_dialog)
        cur.close()
        conn.close()

    def open_dialog(self, evt):
        dialog = self.dialog_class(
            self.root,
            self.current_person,
            finding_id=self.finding_id,
            header=self.header,
            pressed=evt.widget)

class LabelBoilerplate(Labelx):
    ''' 
        Like Label for fine print.  
    '''

    def __init__(self, master, *args, **kwargs):
        Labelx.__init__(self, master, *args, **kwargs)

        self.config(
            bg=formats['bg'], 
            fg=formats['fg'], 
            font=formats['boilerplate'])

class LabelTitleBar(Labelx):
    ''' 
        Like Label for fine print. Can be sized independently
        of other font sizes so users who want larger fonts 
        elsewhere can keep titles tiny if they want. Used for 
        window titlebar and menu strip since people are
        so used to Windows' tiny fonts on these widgets that some
        people will not want to see the font get bigger even if 
        they can't read it. 
    '''

    def __init__(self, master, size='tiny', *args, **kwargs):
        Labelx.__init__(self, master, *args, **kwargs)

        self.config(
            bg=NEUTRAL_COLOR, fg=formats['fg'])
 
        if size == 'tiny':
            self.config(font=formats['titlebar_0'])
        elif size == 'small':
            self.config(font=formats['titlebar_1'])
        elif size == 'medium':
            self.config(font=formats['titlebar_2'])
        elif size == 'large':
            self.config(font=formats['titlebar_3'])

class LabelMenuBarTest(LabelTitleBar):
    '''
        Color can be changed for testing/visibility.
    '''

    def __init__(self, master, size='tiny',  *args, **kwargs):
        LabelTitleBar.__init__(self, master,**options)

        self.config(bg='blue')

        self.bind('<Enter>', self.enrise)
        self.bind('<Leave>', self.flatten)
        self.bind('<Button-1>', self.sink)

        if size == 'tiny':
            self.config(font=formats['titlebar_hilited_0'])
        elif size == 'small':
            self.config(font=formats['titlebar_hilited_1'])
        elif size == 'medium':
            self.config(font=formats['titlebar_hilited_2'])
        elif size == 'large':
            self.config(font=formats['titlebar_hilited_3'])

    def enrise(self, evt):
        evt.widget.config(relief='raised')

    def flatten(self, evt):
        evt.widget.config(relief='flat')

    def sink(self, evt):
        evt.widget.config(relief='sunken')

class LabelMenuBar(Labelx):
    '''
        Like LabelTitleBar but normal font weight.
    '''

    def __init__(self, master, size='tiny', *args, **kwargs):
        Labelx.__init__(self, master, *args, **kwargs)

        self.config(bg=formats['head_bg'])

        if size == 'tiny':
            self.config(font=formats['titlebar_hilited_0'])
        elif size == 'small':
            self.config(font=formats['titlebar_hilited_1'])
        elif size == 'medium':
            self.config(font=formats['titlebar_hilited_2'])
        elif size == 'large':
            self.config(font=formats['titlebar_hilited_3'])

class LabelTitleBarHilited(Labelx):
    '''
        Like LabelTitleBar but instead of using a highlight
        color as its normal background, it uses the normal
        background color so it will be highlighted.
    '''

    def __init__(self, master, size='tiny', *args, **kwargs):
        Labelx.__init__(self, master, *args, **kwargs)

        self.config(bg=formats['highlight_bg'])
 
        if size == 'tiny':
            self.config(font=formats['titlebar_hilited_0'])
        elif size == 'small':
            self.config(font=formats['titlebar_hilited_1'])
        elif size == 'medium':
            self.config(font=formats['titlebar_hilited_2'])
        elif size == 'large':
            self.config(font=formats['titlebar_hilited_3'])
       
class LabelStay(Labelx):
    ''' 
        If this subclass is detected its background won't be reconfigured. 
    '''

    def __init__(self, master, *args, **kwargs):
        Labelx.__init__(self, master, *args, **kwargs)

        pass

class LabelButtonImage(Labelx):
    ''' 
        A label that looks and works like a button. Good for
        images since it sizes itself to its contents, so don't
        add width and height to this class or change its color.
    '''

    def __init__(self, master, *args, **kwargs):
        Labelx.__init__(self, master, *args, **kwargs)

        self.bind('<FocusIn>', self.show_focus)
        self.bind('<FocusOut>', self.unshow_focus)
        self.bind('<Button-1>', self.on_press)
        self.bind('<ButtonRelease-1>', self.on_release)
        self.bind('<Enter>', self.on_hover)
        self.bind('<Leave>', self.on_unhover)

    def show_focus(self, evt):
        self.config(borderwidth=2)

    def unshow_focus(self, evt):
        self.config(borderwidth=1)

    def on_press(self, evt):
        formats = make_formats_dict()
        self.config(relief='sunken', bg=formats['head_bg'])

    def on_release(self, evt):
        formats = make_formats_dict()
        self.config(relief='raised', bg=formats['bg'])

    def on_hover(self, evt):
        self.config(relief='groove')

    def on_unhover(self, evt):
        self.config(relief='raised')

class LabelButtonText(LabelButtonImage):
    ''' 
        A label that looks and works like a button. Displays Text.
    '''

    def __init__(self, master, width=8, *args, **kwargs):
        LabelButtonImage.__init__(self, master, *args, **kwargs)

        self.config(
            bg=formats['bg'],
            fg=formats['fg'],
            font=formats['input_font'],
            anchor='center',
            borderwidth=1, 
            relief='raised', 
            takefocus=1,
            width=width)

class KinTip(FrameHilited5):
    '''
        Display kin name when user points to a kin_type button in kin column
        on events table.
    '''
    def __init__(self, master, text='', *args, **kwargs):
        FrameHilited5.__init__(self, master, *args, **kwargs)

        instrux1 = LabelTip(
            self, text='Click to make', bd=0)
        instrux2 = LabelTipBold(
            self, 
            text=text)
        instrux3 = LabelTip(
            self, text='the current person', bd=0)

        instrux1.grid(padx=1, pady=1, ipadx=3, ipady=3)
        instrux2.grid(padx=1, pady=1, ipadx=3, ipady=3)
        instrux3.grid(padx=1, pady=1, ipadx=3, ipady=3)

class LabelMovable(LabelHilited):
    ''' 
        A label that can be moved to a different grid position
        by trading places with another widget on press of an
        arrow key. The master can't contain anything but LabelMovables. 
        The ipadx, ipady, padx, pady, and sticky grid options can
        be used as long as they're the same for every LabelMovable in
        the master. With some more coding, columnspan and rowspan
        could be set too but as is the spans should be left at
        their default values which is 1.
    '''

    def __init__(self, master, first_column=0, first_row=0, *args, **kwargs):
        LabelHilited.__init__(self, master, *args, **kwargs)

        self.formats = make_formats_dict()

        self.master = master
        self.first_column = first_column
        self.first_row = first_row

        self.config(
            takefocus=1, 
            bg=formats['highlight_bg'], 
            fg=formats['fg'], 
            font=formats['output_font'])
        self.bind('<FocusIn>', self.highlight_on_focus)
        self.bind('<FocusOut>', self.unhighlight_on_unfocus)
        self.bind('<Key>', self.locate)
        self.bind('<Key>', self.move)

    def locate(self, evt):
        ''' 
            Get the grid position of the two widgets that will
            trade places.
        '''

        self.mover = evt.widget

        mover_dict = self.mover.grid_info()
        self.old_col = mover_dict['column']
        self.old_row = mover_dict['row']
        self.ipadx = mover_dict['ipadx']
        self.ipady = mover_dict['ipady']
        self.pady = mover_dict['pady']
        self.padx = mover_dict['padx']
        self.sticky = mover_dict['sticky']        

        self.less_col = self.old_col - 1
        self.less_row = self.old_row - 1
        self.more_col = self.old_col + 1
        self.more_row = self.old_row + 1

        self.last_column = self.master.grid_size()[0] - 1
        self.last_row = self.master.grid_size()[1] - 1

    def move(self, evt):
        ''' 
            Determine which arrow key was pressed and make the trade. 
        '''

        def move_left():
            if self.old_col > self.first_column:
                for child in self.master.winfo_children():
                    if (child.grid_info()['column'] == self.less_col and 
                            child.grid_info()['row'] == self.old_row):
                        movee = child
                        movee.grid_forget()
                        movee.grid(
                            column=self.old_col, row=self.old_row, 
                            ipadx=self.ipadx, ipady=self.ipady, padx=self.padx, 
                            pady=self.pady, sticky=self.sticky)
                self.mover.grid_forget()
                self.mover.grid(
                    column=self.less_col, row=self.old_row, ipadx=self.ipadx, 
                    ipady=self.ipady, padx=self.padx, pady=self.pady, 
                    sticky=self.sticky)

        def move_right():
            if self.old_col < self.last_column:
                for child in self.master.winfo_children():
                    if (child.grid_info()['column'] == self.more_col and 
                            child.grid_info()['row'] == self.old_row):
                        movee = child
                        movee.grid_forget()
                        movee.grid(
                            column=self.old_col, row=self.old_row, 
                            ipadx=self.ipadx, ipady=self.ipady, padx=self.padx, 
                            pady=self.pady, sticky=self.sticky)
                self.mover.grid_forget()
                self.mover.grid(
                    column=self.more_col, row=self.old_row, ipadx=self.ipadx, 
                    ipady=self.ipady, padx=self.padx, pady=self.pady, 
                    sticky=self.sticky) 

        def move_up():
            if self.old_row > self.first_row:
                for child in self.master.winfo_children():
                    if (child.grid_info()['column'] == self.old_col and 
                            child.grid_info()['row'] == self.less_row):
                        movee = child
                        movee.grid_forget()
                        movee.grid(
                            column=self.old_col, row=self.old_row, 
                            ipadx=self.ipadx, ipady=self.ipady, padx=self.padx, 
                            pady=self.pady, sticky=self.sticky)
                self.mover.grid_forget()
                self.mover.grid(
                    column=self.old_col, row=self.less_row, ipadx=self.ipadx, 
                    ipady=self.ipady, padx=self.padx, pady=self.pady, 
                    sticky=self.sticky)

        def move_down():
            if self.old_row < self.last_row:
                for child in self.master.winfo_children():
                    if (child.grid_info()['column'] == self.old_col and 
                            child.grid_info()['row'] == self.more_row):
                        movee = child
                        movee.grid_forget()
                        movee.grid(
                            column=self.old_col, row=self.old_row, 
                            ipadx=self.ipadx, ipady=self.ipady, padx=self.padx, 
                            pady=self.pady, sticky=self.sticky)
                self.mover.grid_forget()
                self.mover.grid(
                    column=self.old_col, row=self.more_row, ipadx=self.ipadx, 
                    ipady=self.ipady, padx=self.padx, pady=self.pady, 
                    sticky=self.sticky)

        self.locate(evt)

        keysyms = {
            'Left' : move_left,
            'Right' : move_right,
            'Up' : move_up,
            'Down' : move_down}

        for k,v in keysyms.items():
            if evt.keysym == k:
                v()

        self.fix_tab_order()

    def fix_tab_order(self):
        new_order = []
        for child in self.master.winfo_children():
            new_order.append((
                child, 
                child.grid_info()['column'], 
                child.grid_info()['row']))
            new_order.sort(key=lambda i: (i[1], i[2])) 
        for tup in new_order:
            widg = tup[0]
            widg.lift()        

    def highlight_on_focus(self, evt):        
        evt.widget.config(bg=self.formats['head_bg'])

    def unhighlight_on_unfocus(self, evt):        
        evt.widget.config(bg=self.formats['highlight_bg'])

class Buttonx(tk.Button):
    def __init__(self, master, *args, **kwargs):
        tk.Button.__init__(self, master, *args, **kwargs)
        pass

    def winfo_subclass(self):
        ''' a method that works like built-in tkinter method
            w.winfo_class() except it gets subclass names
            of widget classes custom-made by inheritance '''
        subclass = type(self).__name__
        return subclass

# BUTTONS should not use a medium background color because the highlightthickness
    # and highlightcolor options don't work and the button highlight focus might not
    # be visible since Tkinter or Windows is choosing the color of the focus highlight
    # and it can't be made thicker.
class Button(Buttonx):
    ''' Includes tk.Button in the colorizer scheme. '''
    def __init__(self, master, *args, **kwargs):
        Buttonx.__init__(self, master, *args, **kwargs)

        self.config(
            font=(formats['output_font']),
            overrelief=tk.GROOVE, 
            activebackground=formats['head_bg'],
            bg=formats['bg'],
            fg=formats['fg'])

class ButtonFlatHilited(Buttonx):
    '''
        A button with no relief or border. Used for the Combobox dropdown.
    '''
    def __init__(self, master, *args, **kwargs):
        Buttonx.__init__(self, master, *args, **kwargs)

        self.config(
            bg=formats['highlight_bg'],
            relief='flat',
            fg=formats['fg'],
            activebackground=formats['fg'], # bg color while pressed
            activeforeground=formats['bg'], # fg color while pressed
            overrelief='flat', # relief when hovered by mouse
            bd=0) # prevents sunken relief while pressed
        self.grid_configure(sticky='ew') 

        def highlight(self, evt):
            self.config(
                bg=formats['highlight_bg'],
                fg=formats['fg'],
                activebackground=formats['fg'],
                activeforeground=formats['bg'])

class ButtonQuiet(Buttonx):
    ''' Same color as background, no text. '''
    def __init__(self, master, *args, **kwargs):
        Buttonx.__init__(self, master, *args, **kwargs)

        self.config(
            text='',
            width=3,
            overrelief=tk.GROOVE, 
            activebackground=formats['head_bg'],
            bg=formats['bg'],  
            fg=formats['fg'])

class ButtonPlain(Buttonx):
    ''' Sans serif font. '''
    def __init__(self, master, *args, **kwargs):
        Buttonx.__init__(self, master, *args, **kwargs)

        self.config(
            font=(formats['input_font']),
            bd=0, 
            activebackground=formats['head_bg'],
            bg=formats['bg'],  
            fg=formats['fg'])
        self.bind('<Enter>', self.highlight)

    def highlight(self, evt):
        self.config(cursor='hand2')
    
class Entryx(tk.Entry):
    def __init__(self, master, *args, **kwargs):
        tk.Entry.__init__(self, master, *args, **kwargs)
        pass

    def winfo_subclass(self):
        ''' a method that works like built-in tkinter method
            w.winfo_class() except it gets subclass names
            of widget classes custom-made by inheritance '''
        subclass = type(self).__name__
        return subclass

class Entry(Entryx):
    def __init__(self, master, *args, **kwargs):
        Entryx.__init__(self, master, *args, **kwargs)
        
        self.config(
            bg=formats['highlight_bg'], 
            fg=formats['fg'], 
            font=formats['input_font'], 
            insertbackground=formats['fg'])

class EntryUnhilited(Entryx):
    '''
        Looks like a Label.
    '''
    def __init__(self, master, *args, **kwargs):
        Entryx.__init__(self, master, *args, **kwargs)
        
        self.config(
            bd=0,
            bg=formats['bg'], 
            fg=formats['fg'], 
            font=formats['input_font'], 
            insertbackground=formats['fg'])


class EntryHilited1(Entryx):
    '''
        Looks like a Label but different background color.
    '''
    def __init__(self, master, *args, **kwargs):
        Entryx.__init__(self, master, *args, **kwargs)
        
        self.config(
            bd=0,
            bg=formats['highlight_bg'], 
            fg=formats['fg'], 
            font=formats['input_font'], 
            insertbackground=formats['fg'])


class EntryHilited2(Entryx):
    '''
        Looks like a Label but different background color.
    '''
    def __init__(self, master, *args, **kwargs):
        Entryx.__init__(self, master, *args, **kwargs)
        
        self.config(
            bd=0,
            bg=formats['head_bg'], 
            fg=formats['fg'], 
            font=formats['output_font'], 
            insertbackground=formats['fg'])

class EntryAutofill(EntryUnhilited):
    ''' 
        Simple case-insensitive autofill entry with no dropdown 
        list, lets you type as fast as you want. Values option 
        is not a real tkinter option, so you can't use
        instance.config(values=new_values). Change values list 
        like this: instance.values = [5, 15, 19, 42]. Autofills 
        nothing till you type up to the first unique character. 
        Example: If the list has "Bill" and "Bilbo", nothing 
        will autofill till you type the second b or the l. You can 
        backspace and keep typing a different word with no extra 
        key strokes or controls and it still fills correctly. 
        Width is set to fit the longest item in the values list.
        instance.config(textvariable=instance.var) is required 
        in the instance to turn on the autofill functionality.
    '''

    def __init__(self, master, *args, **kwargs):
        EntryUnhilited.__init__(self, master, *args, **kwargs)

        self.values = ['red', 'rust', 'black', 'blue', 'Bill', 'Bilbo', 'billboard']
        self.autofill = False

        self.var = tk.StringVar()
        self.bind('<KeyRelease>', self.get_typed)
        self.bind('<Key>', self.detect_pressed)

    def match_string(self):
        hits = []
        got = self.var.get()
        for item in self.values:
            if item.lower().startswith(got.lower()):
                hits.append(item)
        return hits    

    def get_typed(self, event):
        if self.autofill is False:
            return
        if len(event.keysym) == 1:
            hits = self.match_string()
            self.show_hit(hits)

    def detect_pressed(self, event):
        if self.autofill is False:
            return
        key = event.keysym
        pos = self.index('insert')
        self.delete(pos, 'end') 

    def show_hit(self, lst):
        if len(lst) == 1:
            self.var.set(lst[0])

class EntryAutofillHilited(EntryAutofill):
    ''' 
        Same as EntryAutofill but has a highlighted background
        like a typical Entry.
    '''
    def __init__(self, master, *args, **kwargs): 
        EntryAutofill.__init__(self, master, *args, **kwargs)

        self.config(bg=formats['highlight_bg'])

class EntryDefaultText(Entry):
    def __init__(self, master, default_text, *args, **kwargs):
        Entry.__init__(self, master, *args, **kwargs)
        ''' 
            For entries that need to have instructions/default text.
            Can't use this with a widget that automatically
            comes into focus since the default text would be cleared.
        '''
        self.default_text = default_text
        self.formats = make_formats_dict()
        var = tk.StringVar()
        var.set(self.default_text)
        self.config(
            fg=self.formats['head_bg'],
            bg=self.formats['highlight_bg'], 
            font=self.formats['show_font'], 
            textvariable=var)
        self.textvariable = var

        self.bind('<Button-1>', self.clear_default_text)
        self.bind('<FocusIn>', self.clear_default_text)
        self.bind('<FocusOut>', self.clear_selection)

    def clear_default_text(self, evt=None):
        if self.cget('state') == 'disabled':
            print('disabled')
            return
        if self.get() == self.default_text:
            self.delete(0, 'end')
            self.config(
                bg=self.formats['highlight_bg'], 
                font=self.formats['input_font'])            
        else:
            self.config(
                bg=self.formats['highlight_bg'], 
                font=self.formats['input_font'],
                fg=self.formats['fg'])

    def clear_selection(self, evt):
        if len(self.get()) == 0:
            self.insert(0, self.default_text)
            self.config(
                font=self.formats['show_font'], 
                fg=formats['head_bg'])
        self.select_clear()

    def replace_default_text(self):
        self.insert(0, self.default_text) 
        self.config(fg=formats['head_bg'], font=self.formats['show_font'])         

class LabelCopiable(Entryx):
    ''' 
        To use as a Label whose text can be selected 
        with mouse, set the state to disabled after 
        constructing the widget and giving it text. 
        Enable temporarily to change color or text, for example.
    '''

    def __init__(self, master, *args, **kwargs):
        Entryx.__init__(self, master, *args, **kwargs)

        self.config(
            readonlybackground=self.cget('background'), 
            justify='center', 
            bd=0, 
            takefocus=0)

class LabelGoTo(Labelx):
    '''          
        Ctrl+click runs code relevant to the entity named in 
        the clicked Label. For example, if label says John 
        Doe, Ctrl+click label can be used to make John Doe the 
        current person. The subject_id parameter can be used for
        any entity with an ID such as person, place, citation.

        The EntryLabel/LabelGoTo in dialogs can't be used with Ctrl+click to
        change the current person. Probably could be done once but
        not twice because the findings table that existed when the
        dialog was made would be destroyed upon making a new table
        for a new current person. So trying to change the current
        person wouldn't work a 2nd time, so I'm not going to allow
        it at all. 
    '''

    def __init__(
            self, 
            master,  
            table=None,
            change_person=None,
            subject_id=None,
            place_id=None,
            source_id=None,
            citation_id=None,
            *args, **kwargs):

        Labelx.__init__(self, master, *args, **kwargs)

        self.formats = make_formats_dict()

        self.table = table
        self.change_person = change_person
        self.subject_id = subject_id

        self.bind('<Enter>', self.highlight_on_enter)
        self.bind('<Leave>', self.unhighlight_on_leave)
        self.bind('<Button-1>', self.set_focus, add='+')

        self.bind('<Control-Button-1>', self.go_to_entity)

        self.config(
            takefocus=1, 
            anchor='w', 
            bg=self.formats['bg'], 
            fg=self.formats['fg'], 
            font=self.formats['input_font'])
        self.grid_configure(sticky='ew')

    def go_to_entity(self, evt):
        '''
            self.change_person is for the name of the function passed
            to this widget when it's made which changes the current
            person displayed on the persons tab.
        '''

        if self.table is None:
            return

        self.change_person(
            self.table.master,
            self.table.main.persons.attributes_content,
            self.table.main.new_person_fill,
            self.table.main.persons.top_pic_button,
            self.table.main,
            self.table.main.tabs.store['person'],
            self.subject_id)

    def set_focus(self, evt):
        self.focus_set()

    def highlight_on_enter(self, evt):
        self.config(bg=self.formats['highlight_bg'])

    def unhighlight_on_leave(self, evt):
        self.config(bg=self.formats['bg'])

# for demo of LabelCopiable see label_with_selectable_text.py

class Textx(tk.Text):
    def __init__(self, master, *args, **kwargs):
        tk.Text.__init__(self, master, *args, **kwargs)

    def winfo_subclass(self):
        '''  '''
        subclass = type(self).__name__
        return subclass

class Text(Textx):
    def __init__(self, master, *args, **kwargs): 
        Textx.__init__(self, master, *args, **kwargs)

        self.config(
            wrap='word', 
            bg=formats['highlight_bg'], 
            fg=formats['fg'],
            font=formats['input_font'],
            insertbackground=formats['fg'])

        self.bind("<Tab>", self.focus_next_window)

    def focus_next_window(self, evt):
        evt.widget.tk_focusNext().focus()
        return("break")

class LabelStylable(Textx):
    def __init__(self, master, *args, **kwargs):
        Textx.__init__(self, master, *args, **kwargs)

        self.master = master
        self.bind('<Map>', lambda event: self.set_height())
        self.tag_config('bold', font="courier 12 bold")
        self.tag_config('italic', font="courier 12 italic")
        self.config(wrap='word', padx=12, pady=12, bd=0)

    def set_height(self):

        height = self.count(1.0, 'end', 'displaylines')
        self.config(height=height)
        self.configure(state="disabled")

# # to use LabelStylable:
# stylin = LabelStylable(root, width=75)
# stylin.insert("end", "Hello, ") 
# stylin.insert("end", "silly ", "italic") 
# stylin.insert("end", "world", "bold")

class MessageCopiable(Textx):
    ''' 
        To use as a Label whose text can be selected 
        with mouse, set the state to disabled after 
        constructing the widget and giving it text. 
        Enable temporarily to change color or text, for example.
    '''

    def __init__(self, master, *args, **kwargs):
        Textx.__init__(self, master, *args, **kwargs)

        self.config(
            bg=formats['bg'],
            fg=formats['fg'],
            borderwidth=0, 
            wrap='word',
            state='disabled',
            font=(formats['output_font']),  
            takefocus=0)
       
    def set_height(self):
        # answer is wrong first time thru mainloop so update:
        self.update_idletasks()
        lines = self.count('1.0', 'end', 'displaylines')
        self.config(height=lines)

        self.tag_configure('center', justify='center')
        self.tag_add('center', '1.0', 'end')
        self.config(state='disabled')
    # How to use:
    # www = MessageCopiable(root, width=32)
    # www.insert(1.0, 
        # 'Maecenas quis elit eleifend, lobortis turpis at, iaculis '
        # 'odio. Phasellus congue, urna sit amet posuere luctus, mauris '
        # 'risus tincidunt sapien, vulputate scelerisque ipsum libero at '
        # 'neque. Nunc accumsan pellentesque nulla, a ultricies ex '
        # 'convallis sit amet. Etiam ut sollicitudi felis, sit amet '
        # 'dictum lacus. Mauris sed mattis diam. Pellentesque eu malesuada '
        # 'ipsum, vitae sagittis nisl Morbi a mi vitae nunc varius '
        # 'ullamcorper in ut urna. Maecenas auctor ultrices orci. '
        # 'Donec facilisis a tortor pellentesque venenatis. Curabitur '
        # 'pulvinar bibendum sem, id eleifend lorem sodales nec. Mauris '
        # 'eget scelerisque libero. Lorem ipsum dolor sit amet, consectetur '
        # 'adipiscing elit. Integer vel tellus nec orci finibus ornare. '
        # 'Praesent pellentesque aliquet augue, nec feugiat augue posuere ')
    # www.grid()
    # www.set_height()
        
class Checkbuttonx(tk.Checkbutton):
    def __init__(self, master, *args, **kwargs):
        tk.Checkbutton.__init__(self, master, *args, **kwargs)
        pass

    def winfo_subclass(self):
        '''  '''
        subclass = type(self).__name__
        return subclass

class Checkbutton(Checkbuttonx):
    def __init__(self, master, *args, **kwargs):
        Checkbuttonx.__init__(self, master, *args, **kwargs)
        ''' 
            To see selection set the selectcolor 
            option to either bg or highlight_bg.
        '''
        self.config(
            bg=formats['bg'],
            fg=formats['fg'], 
            activebackground=formats['highlight_bg'],
            selectcolor=formats['bg'], 
            padx=6, pady=6) 
       
class Radiobuttonx(tk.Radiobutton):
    def __init__(self, master, *args, **kwargs):
        tk.Radiobutton.__init__(self, master, *args, **kwargs)
        pass

    def winfo_subclass(self):
        '''  '''
        subclass = type(self).__name__
        return subclass 

class Radiobutton(Radiobuttonx):
    def __init__(self, master, *args, **kwargs):
        Radiobuttonx.__init__(self, master, *args, **kwargs)
        ''' 
            To see selection set the selectcolor 
            option to either bg or highlight_bg.
        '''
        self.config(
            bg=formats['bg'],
            fg=formats['fg'], 
            activebackground=formats['highlight_bg'],
            selectcolor=formats['bg'], 
            padx=6, pady=6) 

class RadiobuttonBig(Radiobutton):
    def __init__(self, master, *args, **kwargs):
        Radiobutton.__init__(self, master, *args, **kwargs)
        ''' 
            If the main content of a dialog is a set of radiobuttons,
            use standard text size.
        '''
        self.config(font=formats['output_font'])

class RadiobuttonHilited(Radiobuttonx):
    def __init__(self, master, *args, **kwargs):
        Radiobuttonx.__init__(self, master, *args, **kwargs)

        self.config(
            bg=formats['highlight_bg'], 
            activebackground=formats['bg'],
            highlightthickness=3,
            overrelief='sunken',
            font=formats['output_font'],
            fg=formats['fg'],
            selectcolor=formats['highlight_bg'], 
            padx=6, pady=6) 

class Toplevelx(tk.Toplevel):
    '''
        All my toplevels have to declare a parent whether they need one or not.
        This keeps the code consistent and symmetrical across all widgets,
        even though Tkinter doesn't require a parent for its Toplevel.
    '''

    def __init__(self, master, *args, **kwargs):
        tk.Toplevel.__init__(self, master, *args, **kwargs)

    def winfo_subclass(self):
        '''  '''
        subclass = type(self).__name__
        return subclass

class Toplevel(Toplevelx):
    def __init__(self, master, *args, **kwargs):
        Toplevelx.__init__(self, master, *args, **kwargs)

        self.config(bg=formats['bg'])

class ToplevelHilited(Toplevelx):
    def __init__(self, *args, **kwargs):
        Toplevelx.__init__(self, *args, **kwargs)

        self.config(bg=formats['highlight_bg'])

class Scalex(tk.Scale):
    def __init__(self, master, *args, **kwargs):
        tk.Scale.__init__(self, master, *args, **kwargs)

    def winfo_subclass(self):
        '''  '''
        subclass = type(self).__name__
        return subclass

class Scale(Scalex):
    def __init__(self, master, *args, **kwargs):
        Scalex.__init__(self, master, *args, **kwargs)
        
        self.config(
            bg=formats['bg'], 
            fg=formats['fg'], 
            font=formats['output_font'],
            troughcolor=formats['highlight_bg'],
            activebackground=formats['head_bg'],
            highlightthickness=0)
        

class ToolTip(Toplevelx):

    ''' 
        I think I stopped working on this for some reason so it's
        probably not finished.
        
        Text tips that show full text when some text doesn't show
        due to the column being too narrow. Part of my 
        never-ending quest to eradicate resizable columns from GUI 
        applications that wouldn't need resizable columns if they
        were designed for their space to hold the information they
        are supposed to display.

        To use:
        instance = ToolTip(parent, overwidthtip=True)
        instance.hoverees.extend([ent2, ent1, lab3, radio2])
        instance.bind_widgets()
    '''

    def __init__(self, master, overwidthtip=False, *args, **kwargs):
        Toplevelx.__init__(self, master, *args, **kwargs)
        
        self.withdraw()

        self.overwidthtip = overwidthtip
        self.widget = None
        self.text = ''
        self.hoverees = []

        self.x = self.y =  0  

        self.wm_overrideredirect(1)

        self.make_widgets()

    def make_widgets(self): 

        self.label = LabelNegative(
            self, 
            justify='left',
            relief='solid', 
            bd=1)
        self.label.pack(ipadx=6, ipady=3)

    def bind_widgets(self):
        for widg in self.hoverees:
            widg.bind('<Enter>', self.enter)
            widg.bind('<Leave>', self.leave)

    def do_the_geometry(self):

        maxvert = self.widget.winfo_screenheight()

        x, y, cx, cy = self.widget.bbox('insert')  

        mouse_at = self.widget.winfo_pointerxy()

        tip_shift = 32 

        if mouse_at[1] < maxvert - tip_shift * 2:
            x = mouse_at[0] + tip_shift
            y = mouse_at[1] + tip_shift
        else:
            x = mouse_at[0] + tip_shift
            y = mouse_at[1] - tip_shift

        self.wm_geometry('+{}+{}'.format(x, y))

    def show_tip(self):
        self.do_the_geometry()
        self.deiconify()

    def enter(self, evt):
        self.widget = evt.widget
        self.text = self.widget.get()
        self.config_tip()

    def leave(self, evt):
        self.hide_tip()

    def hide_tip(self):
        self.withdraw()
        self.label.config(text='')

    def config_tip(self):
        if self.overwidthtip is True:
            self.config_overwidthtip()
            return
        self.label.config(text=self.text)
        self.show_tip()

    def config_overwidthtip(self):
        if len(self.text) > self.widget.cget('width'):
            self.label.config(text=self.text)
            self.show_tip()

class Canvasx(tk.Canvas):
    def __init__(self, master, *args, **kwargs):
        tk.Canvas.__init__(self, master, *args, **kwargs)
        pass

    def winfo_subclass(self):
        '''  '''
        subclass = type(self).__name__
        return subclass

class Canvas(Canvasx):
    def __init__(self, master, *args, **kwargs):
        Canvasx.__init__(self, master, *args, **kwargs)

        self.config(bg=formats['bg'], bd=0, highlightthickness=0)

class CanvasHilited(Canvasx):
    def __init__(self, master, *args, **kwargs):
        Canvasx.__init__(self, master, *args, **kwargs)

        self.config(bg=formats['highlight_bg'], bd=0, highlightthickness=0)  

# ttk only below this point *********************************************

class Notebookx(ttk.Notebook):
    def __init__(self, master, *args, **kwargs):
        ttk.Notebook.__init__(self, master, *args, **kwargs)

    def winfo_subclass(self):
        subclass = type(self).__name__
        return subclass

class Tabs(Notebookx):
    def __init__(self, master, tab_names, *args, **kwargs):
        Notebookx.__init__(self, master, *args, **kwargs)

        self.master = master
        self.tab_names = tab_names

        self.store = {}

        self.enable_traversal()

        for tup in self.tab_names:
            tab_frm = Frame(self, name='{}_tab'.format(tup[0]))
            self.add(tab_frm)
            self.tab(tab_frm, text=tup[0].title(), underline=tup[1], padding='16')
            self.store[tup[0]] = tab_frm

class Comboboxx(ttk.Combobox):
    '''
        Provides a way of changing colors in the combobox listbox
        dropdown/popdown as well as the ability to detect subclass.
    '''

    def __init__(self, master, *args, **kwargs):
        ttk.Combobox.__init__(self, master, *args, **kwargs)

    def winfo_subclass(self):
        subclass = type(self).__name__
        return subclass

    def config_popdown(self, **kwargs):
        self.tk.eval(
            '[ttk::combobox::PopdownWindow {}].f.l configure {}'.format(
                self, 
                ' '.join(self._options(kwargs))))

class ClickAnywhereCombo(Comboboxx):
    ''' 
        User can ctrl+click in entry box or arrow--not just arrow--
        to make dropdown fly down. Not needed for readonly combobox 
        which already does this. Problem with using plain click for
        this: it prevents dragging in the entry to select text.
        So ctrl+click is a compromise, so that dragging to highlight 
        will still work normally, and the arrow works normally.
    '''

    def __init__(self, master, *args, **kwargs):
        Comboboxx.__init__(self, master, *args, **kwargs)
        self.bind('<Control-Button-1>', self.fly_down_on_click)
        self.config(font=formats['input_font'])

    def fly_down_on_click(self, evt):
        if int(evt.type) == 4:
            w = evt.widget
            w.event_generate('<Down>', when='head')  

class ClearableReadonlyCombobox(Comboboxx):
    '''
        User can clear mistaken selection by pressing Delete, 
        Escape, or Backspace.
    '''

    def __init__(self, master, *args, **kwargs):
        Comboboxx.__init__(self, master, *args, **kwargs)
        self.state(['readonly'])
        self.bind("<Key-Delete>", self.allow_manual_deletion)
        self.bind("<Key-Escape>", self.allow_manual_deletion)
        self.bind("<Key-BackSpace>", self.allow_manual_deletion)

    def allow_manual_deletion(self, evt):
        if self.get() != "":
            if evt.keysym in ("Escape", "Delete", "BackSpace"):
                self.delete_content()

    def delete_content(self):
        self.state(['!readonly', 'selected'])
        self.set("")
        self.state(['readonly'])

# DO NOT DELETE YET the following is a complete copy of this module before the recent creation of a Toykinter demo app and the subsequent removal of Toykinter widgets from this module. Also wait till there is no more ttk in Treebard before deleting the commented old version below.

# formats = make_formats_dict()

# # print('formats is', formats)
# # formats is {
    # # 'bg': '#232931', 'highlight_bg': '#393e46', 'head_bg': '#2E5447', 
    # # 'fg': '#eeeeee', 'output_font': ('courier', 14), 'input_font': ('tahoma', 14), 
    # # 'heading1': ('courier', 28, 'bold'), 'heading2': ('courier', 21, 'bold'), 
    # # 'heading3': ('courier', 15, 'bold'), 'heading4': ('courier', 11, 'bold'), 
    # # 'status': ('tahoma', 11), 'boilerplate': ('tahoma', 9)}

# class Framex(tk.Frame):
    # def __init__(self, master, *args, **kwargs):
        # tk.Frame.__init__(self, master, *args, **kwargs)
        # pass

    # def winfo_subclass(self):
        # ''' 
            # Like built-in tkinter method
            # w.winfo_class() except it gets subclass names.
        # '''
        # subclass = type(self).__name__
        # return subclass

# class FrameStay(Framex):
    # ''' 
        # Frame background color will not change when color scheme changes.
    # '''

    # def __init__(self, master, *args, **kwargs):
        # Framex.__init__(self, master, *args, **kwargs)
        # pass

# class Frame(Framex):
    # ''' 
        # Frame background color changes when color scheme changes. 
    # '''

    # def __init__(self, master, *args, **kwargs):
        # Framex.__init__(self, master, *args, **kwargs)

        # self.config(bg=formats['bg'])

# class FrameTest(Framex):
    # ''' 
        # Frame background color can be altered for testing/visibility. 
    # '''

    # def __init__(self, master, *args, **kwargs):
        # Framex.__init__(self, master, *args, **kwargs)
        # self.config(bg='orange')

# class FrameTest2(Framex):
    # ''' 
        # Frame background color can be altered for testing/visibility. 
    # '''

    # def __init__(self, master, *args, **kwargs):
        # Framex.__init__(self, master, *args, **kwargs)
        # self.config(bg='green')

# class FrameTitleBar(Framex):
    # ''' 
        # Frame hilited by border and a different background color.
    # '''

    # def __init__(self, master, *args, **kwargs):
        # Framex.__init__(self, master, *args, **kwargs)
        # self.config(bg=NEUTRAL_COLOR)


# class FrameHilited(Framex):
    # ''' 
        # Frame hilited by groove border and background color.
    # '''

    # def __init__(self, master, *args, **kwargs):
        # Framex.__init__(self, master, *args, **kwargs)
        # self.config(bg=formats['highlight_bg'], bd=3, relief='groove')

# class FrameHilited1(Framex):
    # ''' 
        # Used for narrow resizing sash on left edge of
        # attributes table. Could be used as vertical 
        # separator.
    # '''

    # def __init__(self, master, *args, **kwargs):
        # Framex.__init__(self, master, *args, **kwargs)
        # self.config(bg=formats['highlight_bg'], bd=6, relief='ridge')

# class FrameHilited2(Framex):
    # ''' 
        # Frame hilited by border and a different background color.
    # '''

    # def __init__(self, master, *args, **kwargs):
        # Framex.__init__(self, master, *args, **kwargs)
        # self.config(bg=formats['head_bg'])

# class FrameHilited3(Framex):
    # ''' 
        # Frame hilited by different background color but not border.
    # '''

    # def __init__(self, master, *args, **kwargs):
        # Framex.__init__(self, master, *args, **kwargs)
        # self.config(bg=formats['highlight_bg'])

# class FrameHilited4(Framex):
    # ''' 
        # Frame hilited by sunken border and background color.
    # '''

    # def __init__(self, master, *args, **kwargs):
        # Framex.__init__(self, master, *args, **kwargs)
        # self.config(bg=formats['highlight_bg'], bd=2, relief='sunken')

# class FrameHilited5(Framex):
    # ''' 
        # Frame hilited by sunken border and background color.
    # '''

    # def __init__(self, master, *args, **kwargs):
        # Framex.__init__(self, master, *args, **kwargs)
        # self.config(bg=formats['highlight_bg'], bd=1, relief='solid')

# class LabelFramex(tk.LabelFrame):
    # def __init__(self, master, *args, **kwargs):
        # tk.LabelFrame.__init__(self, master, *args, **kwargs)
        # pass

    # def winfo_subclass(self):
        # ''' 
            # Like built-in tkinter method
            # w.winfo_class() except it gets subclass names.
        # '''
        # subclass = type(self).__name__
        # return subclass

# class LabelFrame(LabelFramex):
        # def __init__(self, master, *args, **kwargs):
            # LabelFramex.__init__(self, master, *args, **kwargs)

            # self.config(
                # bg=formats['bg'], font=formats['output_font'], fg=formats['fg']) 

# class Messagex(tk.Message):
    # def __init__(self, master, *args, **kwargs):
        # tk.Message.__init__(self, master, *args, **kwargs)
        # pass

    # def winfo_subclass(self):
        # ''' 
            # Like built-in tkinter method
            # w.winfo_class() except it gets subclass names.
        # '''
        # subclass = type(self).__name__
        # return subclass

# class Message(Messagex):
    # def __init__(self, master, *args, **kwargs):
        # Messagex.__init__(self, master, *args, **kwargs)

        # self.config(
            # bg=formats['bg'], fg=formats['fg'], font=formats['output_font'])

# class MessageHilited(Messagex):
    # def __init__(self, master, *args, **kwargs):
        # Messagex.__init__(self, master, *args, **kwargs)

        # self.config(
            # bd=3, relief='raised',
            # bg=formats['highlight_bg'], 
            # fg=formats['fg'], 
            # font=formats['output_font'])
 
# class Separator(Framex):
    # ''' 
        # Horizontal separator like ttk.Separator but 
        # can be sized and utilize the user pref colors.
    # '''

    # def __init__(
        # self, master, height, 
        # color1=formats['head_bg'], 
        # color2=formats['highlight_bg'], 
        # color3=formats['bg'], *args, **kwargs):
        # Framex.__init__(self, master, *args, **kwargs)

        # self.grid_columnconfigure(0, weight=1)
        # self.grid_rowconfigure(1, weight=0)
        # self.grid_rowconfigure(2, weight=0)

        # self.height = int(height/5)
        # self.color1 = color1
        # self.color2 = color2
        # self.color3 = color3

        # if self.height > 0:
            # self.line1 = FrameStay(
                # self, bg=self.color1, height=self.height)
            # self.line1.grid(column=0, row=0, sticky='ew')

            # self.line2 = FrameStay(
                # self, bg=self.color2, height=self.height)
            # self.line2.grid(column=0, row=1, sticky='ew')

            # self.line3 = FrameStay(
                # self, bg=self.color3, height=self.height)
            # self.line3.grid(column=0, row=2, sticky='ew')

            # self.line4 = FrameStay(
                # self, bg=self.color2, height=self.height)
            # self.line4.grid(column=0, row=4, sticky='ew')

            # self.line5 = FrameStay(
                # self, bg=self.color1, height=self.height)
            # self.line5.grid(column=0, row=5, sticky='ew')
        # else:
            # self.line1 = FrameStay(
                # self, bg=self.color1, height=self.height)
            # self.line1.grid(column=0, row=0, sticky='ew')

            # self.line2 = FrameStay(
                # self, bg=self.color2, height=self.height)
            # self.line2.grid(column=0, row=1, sticky='ew')

            # self.line3 = FrameStay(
                # self, bg=self.color3, height=self.height)
            # self.line3.grid(column=0, row=2, sticky='ew')

    # def colorize(self):
        # formats = make_formats_dict()
        # self.color1=formats['head_bg'], 
        # self.color2=formats['highlight_bg'], 
        # self.color3=formats['bg']
        # if self.height > 0:
            # self.line1.config(bg=self.color1)
            # self.line2.config(bg=self.color2)
            # self.line3.config(bg=self.color3)
            # self.line4.config(bg=self.color2)
            # self.line5.config(bg=self.color1)
        # else:
            # self.line1.config(bg=self.color1)
            # self.line2.config(bg=self.color2)
            # self.line3.config(bg=self.color3)
        
# class Labelx(tk.Label):
    # def __init__(self, master, *args, **kwargs):
        # tk.Label.__init__(self, master, *args, **kwargs)

    # def winfo_subclass(self):
        # ''' a method that works like built-in tkinter method
            # w.winfo_class() except it gets subclass names
            # of widget classes custom-made by inheritance '''
        # subclass = type(self).__name__
        # return subclass

# class Label(Labelx):
    # ''' 
        # If this subclass is detected it will be reconfigured
        # according to user preferences. 
    # '''
    # def __init__(self, master, *args, **kwargs):
        # Labelx.__init__(self, master, *args, **kwargs)
        # self.config(
            # bg=formats['bg'], 
            # fg=formats['fg'],
            # font=formats['output_font'])

# class LabelEntrylike(Labelx):
    # ''' 
        # Normal Label that uses the same font as an Entry. 
    # '''
    # def __init__(self, master, *args, **kwargs):
        # Labelx.__init__(self, master, *args, **kwargs)
        # self.config(
            # bg=formats['bg'], 
            # fg=formats['fg'],
            # font=formats['input_font'])

# class LabelTest(Labelx):
    # ''' 
        # Color can be changed for testing/visibility. 
    # '''

    # def __init__(self, master, *args, **kwargs):
        # Labelx.__init__(self, master, *args, **kwargs)
        # self.config(
            # bg='purple', 
            # fg=formats['fg'],
            # font=formats['output_font'])
 
# class LabelItalic(Labelx):
    # ''' 
        # Uses input font and italics to display errors & such. 
    # '''

    # def __init__(self, master, *args, **kwargs):
        # Labelx.__init__(self, master, *args, **kwargs)
        # self.config(font=formats['show_font'])
 
# class LabelItalicHilited(Labelx):
    # ''' 
        # Uses input font and italics to display errors & such. 
    # '''

    # def __init__(self, master, *args, **kwargs):
        # Labelx.__init__(self, master, *args, **kwargs)
        # self.config(
            # font=formats['show_font'],
            # bg=formats['head_bg'])

# class LabelHilited(Label):
    # ''' 
        # Like Label with a different background. 
    # '''
    # def __init__(self, master, *args, **kwargs):
        # Label.__init__(self, master, *args, **kwargs)
        # self.config(bg=formats['highlight_bg'])

# class LabelHilited2(Label):
    # ''' 
        # Like Label with a different background. 
    # '''
    # def __init__(self, master, *args, **kwargs):
        # Label.__init__(self, master, *args, **kwargs)

        # self.config(bg=formats['head_bg'])

# class LabelTip(LabelHilited):
    # ''' 
        # Like Label with a different background. For tooltips. 
    # '''
    # def __init__(self, master, *args, **kwargs):
        # LabelHilited.__init__(self, master, *args, **kwargs)
        # self.config(font=formats['status'], bd=0, relief='solid')
        # # changed bd to 0 20210425 so KinTip interior labels would
        # #   not have borders

# class LabelTip2(LabelHilited2):
    # ''' 
        # Like Label with a different background. For tooltips. 
    # '''
    # def __init__(self, master, *args, **kwargs):
        # LabelHilited2.__init__(self, master, *args, **kwargs)
        # self.config(font=formats['status'], bd=1, relief='solid')

# class LabelTipBold(LabelHilited):
    # ''' 
        # Like Label with a different background. 
    # '''
    # def __init__(self, master, *args, **kwargs):
        # LabelTip.__init__(self, master, *args, **kwargs)
        # self.config(font=formats['titlebar_1'])

# class LabelNegative(Labelx):
    # ''' 
        # Usual bg and fg reversed. 
    # '''
    # def __init__(self, master, *args, **kwargs):
        # Labelx.__init__(self, master, *args, **kwargs)
        # self.config(bg=formats['fg'], fg=formats['bg'])

# class LabelH2(Label):
    # ''' 
        # For large subheadings. 
    # '''
    # def __init__(self, master, *args, **kwargs):
        # Label.__init__(self, master, *args, **kwargs)

        # self.config(
            # font=formats['heading3'])

# class LabelH3(Label):
    # ''' 
        # For small subheadings. 
    # '''
    # def __init__(self, master, *args, **kwargs):
        # Label.__init__(self, master, *args, **kwargs)

        # self.config(font=formats['heading3'])

# class LabelColumn(Labelx):
    # '''
        # For column headings in tables.
    # '''
    # def __init__(self, master, *args, **kwargs):
        # Labelx.__init__(self, master, *args, **kwargs)

        # self.config(
            # bg=formats['bg'], 
            # font=formats['heading3'],
            # anchor='w')

# class LabelColumnCenter(LabelColumn):
    # ''' 
        # Like LabelColumn for centered table column headings. 
    # '''
    # def __init__(self, master, *args, **kwargs):
        # LabelColumn.__init__(self, master, *args, **kwargs)

# class KinTip(FrameHilited5):
    # '''
        # Display kin name when user points to a kin_type button in kin column
        # on events table.
    # '''
    # def __init__(self, master, text='', *args, **kwargs):
        # FrameHilited5.__init__(self, master, *args, **kwargs)

        # instrux1 = LabelTip(
            # self, text='Click to make', bd=0)
        # instrux2 = LabelTipBold(
            # self, 
            # text=text)
        # instrux3 = LabelTip(
            # self, text='the current person', bd=0)

        # instrux1.grid(padx=1, pady=1, ipadx=3, ipady=3)
        # instrux2.grid(padx=1, pady=1, ipadx=3, ipady=3)
        # instrux3.grid(padx=1, pady=1, ipadx=3, ipady=3)

# class LabelSearch(Labelx):
    # ''' 
        # For search results column cells. Since this
        # widget responds to so many different events, and
        # then still has to respond to the colorizer, 
        # the code is simpler if the colorizer can
        # treat this class separately from other labels. 
    # '''

    # def __init__(self, master, *args, **kwargs):
        # Labelx.__init__(self, master, *args, **kwargs)

        # self.formats = make_formats_dict()
        # self.config(anchor='w')

# class LabelBoilerplate(Labelx):
    # ''' 
        # Like Label for fine print.  
    # '''

    # def __init__(self, master, *args, **kwargs):
        # Labelx.__init__(self, master, *args, **kwargs)

        # self.config(bg=formats['bg'])

# class LabelTitleBar(Labelx):
    # ''' 
        # Like Label for fine print. Can be sized independently
        # of other font sizes so users who want larger fonts 
        # elsewhere can keep titles tiny if they want. Used for 
        # window titlebar and menu strip since people are
        # so used to Windows' tiny fonts on these widgets that some
        # people will not want to see the font get bigger even if 
        # they can't read it. 
    # '''

    # def __init__(self, master, size='tiny', *args, **kwargs):
        # Labelx.__init__(self, master, *args, **kwargs)

        # # self.config(
            # # bg=formats['head_bg'], fg=formats['fg'])

        # self.config(
            # bg=NEUTRAL_COLOR, fg=formats['fg'])
 
        # if size == 'tiny':
            # self.config(font=formats['titlebar_0'])
        # elif size == 'small':
            # self.config(font=formats['titlebar_1'])
        # elif size == 'medium':
            # self.config(font=formats['titlebar_2'])
        # elif size == 'large':
            # self.config(font=formats['titlebar_3'])

# class LabelMenuBarTest(LabelTitleBar):
    # '''
        # Color can be changed for testing/visibility.
    # '''

    # def __init__(self, master, size='tiny',  *args, **kwargs):
        # LabelTitleBar.__init__(self, master,**options)

        # self.config(bg='blue')

        # self.bind('<Enter>', self.enrise)
        # self.bind('<Leave>', self.flatten)
        # self.bind('<Button-1>', self.sink)

        # if size == 'tiny':
            # self.config(font=formats['titlebar_hilited_0'])
        # elif size == 'small':
            # self.config(font=formats['titlebar_hilited_1'])
        # elif size == 'medium':
            # self.config(font=formats['titlebar_hilited_2'])
        # elif size == 'large':
            # self.config(font=formats['titlebar_hilited_3'])

    # def enrise(self, evt):
        # evt.widget.config(relief='raised')

    # def flatten(self, evt):
        # evt.widget.config(relief='flat')

    # def sink(self, evt):
        # evt.widget.config(relief='sunken')

# class LabelMenuBar(Labelx):
    # '''
        # Like LabelTitleBar but normal font weight.
    # '''

    # def __init__(self, master, size='tiny', *args, **kwargs):
        # Labelx.__init__(self, master, *args, **kwargs)

        # self.config(bg=formats['head_bg'])

        # if size == 'tiny':
            # self.config(font=formats['titlebar_hilited_0'])
        # elif size == 'small':
            # self.config(font=formats['titlebar_hilited_1'])
        # elif size == 'medium':
            # self.config(font=formats['titlebar_hilited_2'])
        # elif size == 'large':
            # self.config(font=formats['titlebar_hilited_3'])

# class LabelTitleBarHilited(Labelx):
    # '''
        # Like LabelTitleBar but instead of using a highlight
        # color as its normal background, it uses the normal
        # background color so it will be highlighted.
    # '''

    # def __init__(self, master, size='tiny', *args, **kwargs):
        # Labelx.__init__(self, master, *args, **kwargs)

        # self.config(bg=formats['highlight_bg'])
 
        # if size == 'tiny':
            # self.config(font=formats['titlebar_hilited_0'])
        # elif size == 'small':
            # self.config(font=formats['titlebar_hilited_1'])
        # elif size == 'medium':
            # self.config(font=formats['titlebar_hilited_2'])
        # elif size == 'large':
            # self.config(font=formats['titlebar_hilited_3'])
       
# class LabelStay(Labelx):
    # ''' 
        # If this subclass is detected it won't be reconfigured. 
    # '''

    # def __init__(self, master, *args, **kwargs):
        # Labelx.__init__(self, master, *args, **kwargs)
        # pass

# class LabelButtonImage(Labelx):
    # ''' 
        # A label that looks and works like a button. Good for
        # images since it sizes itself to its contents, so don't
        # add width and height to this class or change its color.
    # '''

    # def __init__(self, master, *args, **kwargs):
        # Labelx.__init__(self, master, *args, **kwargs)

        # self.bind('<FocusIn>', self.show_focus)
        # self.bind('<FocusOut>', self.unshow_focus)
        # self.bind('<Button-1>', self.on_press)
        # self.bind('<ButtonRelease-1>', self.on_release)
        # self.bind('<Enter>', self.on_hover)
        # self.bind('<Leave>', self.on_unhover)

    # def show_focus(self, evt):
        # self.config(borderwidth=2)

    # def unshow_focus(self, evt):
        # self.config(borderwidth=1)

    # def on_press(self, evt):
        # formats = make_formats_dict()
        # self.config(relief='sunken', bg=formats['head_bg'])

    # def on_release(self, evt):
        # formats = make_formats_dict()
        # self.config(relief='raised', bg=formats['bg'])

    # def on_hover(self, evt):
        # self.config(relief='groove')

    # def on_unhover(self, evt):
        # self.config(relief='raised')

# class LabelButtonText(LabelButtonImage):
    # ''' 
        # A label that looks and works like a button. Displays Text.
    # '''

    # def __init__(self, master, width=8, *args, **kwargs):
        # LabelButtonImage.__init__(self, master, *args, **kwargs)

        # self.config(
            # anchor='center',
            # borderwidth=1, 
            # relief='raised', 
            # takefocus=1,
            # bg=formats['bg'],
            # width=width,
            # font=formats['input_font'],
            # fg=formats['fg'])

# class LabelDots(LabelButtonText):
    # ''' 
        # Display clickable dots if more info, no dots 
        # if no more info. 
    # '''
    # def __init__(
            # self, 
            # master,
            # current_file,
            # dialog_class,
            # *args, **kwargs):
        # LabelButtonText.__init__(self, master, *args, **kwargs)

        # self.master = master
        # self.root = master.master
        # self.dialog_class = dialog_class

        # self.finding_id = None
        # self.header = None
        # conn = sqlite3.connect(current_file)
        # cur = conn.cursor()
        # cur.execute(select_current_person_id)
        # self.current_person = cur.fetchone()[0]
        # self.config(width=5, font=formats['heading3'])
        # self.bind('<Button-1>', self.open_dialog)
        # cur.close()
        # conn.close()

    # def open_dialog(self, evt):
        # dialog = self.dialog_class(
            # self.root,
            # self.current_person,
            # finding_id=self.finding_id,
            # header=self.header,
            # pressed=evt.widget)

# class LabelMovable(LabelHilited):
    # ''' 
        # A label that can be moved to a different grid position
        # by trading places with another widget on press of an
        # arrow key. The master can't contain anything but LabelMovables. 
        # The ipadx, ipady, padx, pady, and sticky grid options can
        # be used as long as they're the same for every LabelMovable in
        # the master. With some more coding, columnspan and rowspan
        # could be set too but as is the spans should be left at
        # their default values which is 1.
    # '''

    # def __init__(self, master, first_column=0, first_row=0, *args, **kwargs):
        # LabelHilited.__init__(self, master, *args, **kwargs)

        # self.formats = make_formats_dict()

        # self.master = master
        # self.first_column = first_column
        # self.first_row = first_row

        # self.config(
            # takefocus=1, 
            # bg=formats['highlight_bg'], 
            # fg=formats['fg'], 
            # font=formats['output_font'])
        # self.bind('<FocusIn>', self.highlight_on_focus)
        # self.bind('<FocusOut>', self.unhighlight_on_unfocus)
        # self.bind('<Key>', self.locate)
        # self.bind('<Key>', self.move)

    # def locate(self, evt):
        # ''' 
            # Get the grid position of the two widgets that will
            # trade places.
        # '''

        # self.mover = evt.widget

        # mover_dict = self.mover.grid_info()
        # self.old_col = mover_dict['column']
        # self.old_row = mover_dict['row']
        # self.ipadx = mover_dict['ipadx']
        # self.ipady = mover_dict['ipady']
        # self.pady = mover_dict['pady']
        # self.padx = mover_dict['padx']
        # self.sticky = mover_dict['sticky']        

        # self.less_col = self.old_col - 1
        # self.less_row = self.old_row - 1
        # self.more_col = self.old_col + 1
        # self.more_row = self.old_row + 1

        # self.last_column = self.master.grid_size()[0] - 1
        # self.last_row = self.master.grid_size()[1] - 1

    # def move(self, evt):
        # ''' 
            # Determine which arrow key was pressed and make the trade. 
        # '''

        # def move_left():
            # if self.old_col > self.first_column:
                # for child in self.master.winfo_children():
                    # if (child.grid_info()['column'] == self.less_col and 
                            # child.grid_info()['row'] == self.old_row):
                        # movee = child
                        # movee.grid_forget()
                        # movee.grid(
                            # column=self.old_col, row=self.old_row, 
                            # ipadx=self.ipadx, ipady=self.ipady, padx=self.padx, 
                            # pady=self.pady, sticky=self.sticky)
                # self.mover.grid_forget()
                # self.mover.grid(
                    # column=self.less_col, row=self.old_row, ipadx=self.ipadx, 
                    # ipady=self.ipady, padx=self.padx, pady=self.pady, 
                    # sticky=self.sticky)

        # def move_right():
            # if self.old_col < self.last_column:
                # for child in self.master.winfo_children():
                    # if (child.grid_info()['column'] == self.more_col and 
                            # child.grid_info()['row'] == self.old_row):
                        # movee = child
                        # movee.grid_forget()
                        # movee.grid(
                            # column=self.old_col, row=self.old_row, 
                            # ipadx=self.ipadx, ipady=self.ipady, padx=self.padx, 
                            # pady=self.pady, sticky=self.sticky)
                # self.mover.grid_forget()
                # self.mover.grid(
                    # column=self.more_col, row=self.old_row, ipadx=self.ipadx, 
                    # ipady=self.ipady, padx=self.padx, pady=self.pady, 
                    # sticky=self.sticky) 

        # def move_up():
            # if self.old_row > self.first_row:
                # for child in self.master.winfo_children():
                    # if (child.grid_info()['column'] == self.old_col and 
                            # child.grid_info()['row'] == self.less_row):
                        # movee = child
                        # movee.grid_forget()
                        # movee.grid(
                            # column=self.old_col, row=self.old_row, 
                            # ipadx=self.ipadx, ipady=self.ipady, padx=self.padx, 
                            # pady=self.pady, sticky=self.sticky)
                # self.mover.grid_forget()
                # self.mover.grid(
                    # column=self.old_col, row=self.less_row, ipadx=self.ipadx, 
                    # ipady=self.ipady, padx=self.padx, pady=self.pady, 
                    # sticky=self.sticky)

        # def move_down():
            # if self.old_row < self.last_row:
                # for child in self.master.winfo_children():
                    # if (child.grid_info()['column'] == self.old_col and 
                            # child.grid_info()['row'] == self.more_row):
                        # movee = child
                        # movee.grid_forget()
                        # movee.grid(
                            # column=self.old_col, row=self.old_row, 
                            # ipadx=self.ipadx, ipady=self.ipady, padx=self.padx, 
                            # pady=self.pady, sticky=self.sticky)
                # self.mover.grid_forget()
                # self.mover.grid(
                    # column=self.old_col, row=self.more_row, ipadx=self.ipadx, 
                    # ipady=self.ipady, padx=self.padx, pady=self.pady, 
                    # sticky=self.sticky)

        # self.locate(evt)

        # keysyms = {
            # 'Left' : move_left,
            # 'Right' : move_right,
            # 'Up' : move_up,
            # 'Down' : move_down}

        # for k,v in keysyms.items():
            # if evt.keysym == k:
                # v()

        # self.fix_tab_order()

    # def fix_tab_order(self):
        # new_order = []
        # for child in self.master.winfo_children():
            # new_order.append((
                # child, 
                # child.grid_info()['column'], 
                # child.grid_info()['row']))
            # new_order.sort(key=lambda i: (i[1], i[2])) 
        # for tup in new_order:
            # widg = tup[0]
            # widg.lift()        

    # def highlight_on_focus(self, evt):        
        # evt.widget.config(bg=self.formats['head_bg'])

    # def unhighlight_on_unfocus(self, evt):        
        # evt.widget.config(bg=self.formats['highlight_bg'])

# class Buttonx(tk.Button):
    # def __init__(self, master, *args, **kwargs):
        # tk.Button.__init__(self, master, *args, **kwargs)
        # pass

    # def winfo_subclass(self):
        # ''' a method that works like built-in tkinter method
            # w.winfo_class() except it gets subclass names
            # of widget classes custom-made by inheritance '''
        # subclass = type(self).__name__
        # return subclass

# # BUTTONS should not use a medium background color because the highlightthickness
    # # and highlightcolor options don't work and the button highlight focus might not
    # # be visible since Tkinter or Windows is choosing the color of the focus highlight
    # # and it can't be made thicker.
# class Button(Buttonx):
    # ''' Includes tk.Button in the colorizer scheme. '''
    # def __init__(self, master, *args, **kwargs):
        # Buttonx.__init__(self, master, *args, **kwargs)

        # self.config(
            # font=(formats['output_font']),
            # overrelief=tk.GROOVE, 
            # activebackground=formats['head_bg'],
            # bg=formats['bg'],
            # fg=formats['fg'])

# class ButtonFlatHilited(Buttonx):
    # '''
        # A button with no relief or border.
    # '''
    # def __init__(self, master, *args, **kwargs):
        # Buttonx.__init__(self, master, *args, **kwargs)

        # self.config(
            # bg=formats['highlight_bg'],
            # relief='flat',
            # fg=formats['fg'],
            # activebackground=formats['fg'], # bg color while pressed
            # activeforeground=formats['bg'], # fg color while pressed
            # overrelief='flat', # relief when hovered by mouse
            # bd=0) # prevents sunken relief while pressed
        # self.grid_configure(sticky='ew') 

# class ButtonQuiet(Buttonx):
    # ''' Same color as background, no text. '''
    # def __init__(self, master, *args, **kwargs):
        # Buttonx.__init__(self, master, *args, **kwargs)

        # self.config(
            # text='',
            # width=3,
            # overrelief=tk.GROOVE, 
            # activebackground=formats['head_bg'],
            # bg=formats['bg'],  
            # fg=formats['fg'])

# class ButtonPlain(Buttonx):
    # ''' Sans serif font. '''
    # def __init__(self, master, *args, **kwargs):
        # Buttonx.__init__(self, master, *args, **kwargs)

        # self.config(
            # font=(formats['input_font']),
            # bd=0, 
            # activebackground=formats['head_bg'],
            # bg=formats['bg'],  
            # fg=formats['fg'])
        # self.bind('<Enter>', self.highlight)

    # def highlight(self, evt):
        # self.config(cursor='hand2')
    
# class Entryx(tk.Entry):
    # def __init__(self, master, *args, **kwargs):
        # tk.Entry.__init__(self, master, *args, **kwargs)
        # pass

    # def winfo_subclass(self):
        # ''' a method that works like built-in tkinter method
            # w.winfo_class() except it gets subclass names
            # of widget classes custom-made by inheritance '''
        # subclass = type(self).__name__
        # return subclass

# class Entry(Entryx):
    # def __init__(self, master, *args, **kwargs):
        # Entryx.__init__(self, master, *args, **kwargs)
        
        # self.config(
            # bg=formats['highlight_bg'], 
            # fg=formats['fg'], 
            # font=formats['input_font'], 
            # insertbackground=formats['fg'])

# class EntryUnhilited(Entryx):
    # '''
        # Background same as Label, Frame, etc.
    # '''
    # def __init__(self, master, *args, **kwargs):
        # Entryx.__init__(self, master, *args, **kwargs)
        
        # self.config(
            # bd=0,
            # bg=formats['bg'], 
            # fg=formats['fg'], 
            # font=formats['input_font'], 
            # insertbackground=formats['fg'],
            # disabledbackground=formats['bg'],
            # disabledforeground=formats['fg'])

# class EntryAutofill(EntryUnhilited):
    # ''' 
        # Simple case-insensitive autofill entry with no dropdown 
        # list, lets you type as fast as you want. Values option 
        # is not a real tkinter option, so you can't use
        # instance.config(values=new_values). Change values list 
        # like this: instance.values = [5, 15, 19, 42]. Autofills 
        # nothing till you type up to the first unique character. 
        # Example: If the list has "Bill" and "Bilbo", nothing 
        # will autofill till you type the second b or the l. You can 
        # backspace and keep typing a different word with no extra 
        # key strokes or controls and it still fills correctly. 
        # Width is set to fit the longest item in the values list.
        # instance.config(textvariable=instance.var) is required 
        # in the instance to turn on the autofill functionality.
    # '''

    # def __init__(self, master, *args, **kwargs):
        # EntryUnhilited.__init__(self, master, *args, **kwargs)

        # self.values = ['red', 'black', 'blue']
        # self.autofill = False

        # self.var = tk.StringVar()
        # self.filled = False 
        # self.bind('<KeyRelease>', self.get_typed)
        # self.bind('<Key>', self.detect_pressed)

    # def match_string(self):
        # hits = []
        # got = self.var.get()
        # for item in self.values:
            # if item.lower().startswith(got.lower()):
                # hits.append(item)
        # return hits    

    # def get_typed(self, event):
        # if self.autofill is False:
            # return
        # if len(event.keysym) == 1:
            # hits = self.match_string()
            # self.show_hit(hits)

    # def show_hit(self, lst):
        # if len(lst) == 1:
            # self.var.set(lst[0])
            # self.filled = True

    # def detect_pressed(self, event):
        # if self.autofill is False:
            # return
        # key = event.keysym
        # if len(key) == 1 and self.filled is True:
            # pos = self.index('insert')
            # self.delete(pos, 'end') 

# class EntryAutofillHilited(EntryAutofill):
    # ''' 
        # Same as EntryAutofill but has a highlighted background
        # like a typical Entry.
    # '''
    # def __init__(self, master, *args, **kwargs): 
        # EntryAutofill.__init__(self, master, *args, **kwargs)

        # self.config(bg=formats['highlight_bg'])

# class EntryDefaultText(Entry):
    # def __init__(self, master, default_text, *args, **kwargs):
        # Entry.__init__(self, master, *args, **kwargs)
        # ''' 
            # For entries that need to have instructions/default text.
            # Can't use this with a widget that automatically
            # comes into focus since the default text would be cleared.
        # '''
        # self.default_text = default_text
        # self.formats = make_formats_dict()
        # var = tk.StringVar()
        # var.set(self.default_text)
        # self.config(
            # fg=self.formats['head_bg'],
            # bg=self.formats['highlight_bg'], 
            # font=self.formats['show_font'], 
            # textvariable=var)
        # self.textvariable = var

        # self.bind('<Button-1>', self.clear_default_text)
        # self.bind('<FocusIn>', self.clear_default_text)
        # self.bind('<FocusOut>', self.clear_selection)

    # def clear_default_text(self, evt=None):
        # if self.cget('state') == 'disabled':
            # print('disabled')
            # return
        # if self.get() == self.default_text:
            # self.delete(0, 'end')
            # self.config(
                # bg=self.formats['highlight_bg'], 
                # font=self.formats['input_font'])            
        # else:
            # self.config(
                # bg=self.formats['highlight_bg'], 
                # font=self.formats['input_font'],
                # fg=self.formats['fg'])

    # def clear_selection(self, evt):
        # if len(self.get()) == 0:
            # self.insert(0, self.default_text)
            # self.config(
                # font=self.formats['show_font'], 
                # fg=formats['head_bg'])
        # self.select_clear()

    # def replace_default_text(self):
        # self.insert(0, self.default_text) 
        # self.config(fg=formats['head_bg'], font=self.formats['show_font'])         

# class LabelCopiable(Entryx):
    # ''' 
        # To use as a Label whose text can be selected 
        # with mouse, set the state to disabled after 
        # constructing the widget and giving it text. 
        # Enable temporarily to change color or text, for example.
    # '''

    # def __init__(self, master, *args, **kwargs):
        # Entryx.__init__(self, master, *args, **kwargs)

        # self.config(
            # readonlybackground=self.cget('background'), 
            # justify='center', 
            # bd=0, 
            # takefocus=0)

# class LabelGoTo(Labelx):
    # '''          
        # Ctrl+click runs code relevant to the entity named in 
        # the clicked Label. For example, if label says John 
        # Doe, Ctrl+click label can be used to make John Doe the 
        # current person. The subject_id parameter can be used for
        # any entity with an ID such as person, place, citation.

        # The EntryLabel/LabelGoTo in dialogs can't be used with Ctrl+click to
        # change the current person. Probably could be done once but
        # not twice because the findings table that existed when the
        # dialog was made would be destroyed upon making a new table
        # for a new current person. So trying to change the current
        # person wouldn't work a 2nd time, so I'm not going to allow
        # it at all. 
    # '''

    # def __init__(
            # self, 
            # master,  
            # table=None,
            # change_person=None,
            # subject_id=None,
            # place_id=None,
            # source_id=None,
            # citation_id=None,
            # *args, **kwargs):

        # Labelx.__init__(self, master, *args, **kwargs)

        # self.formats = make_formats_dict()

        # self.table = table
        # self.change_person = change_person
        # self.subject_id = subject_id

        # self.bind('<Enter>', self.highlight_on_enter)
        # self.bind('<Leave>', self.unhighlight_on_leave)
        # self.bind('<Button-1>', self.set_focus, add='+')

        # self.bind('<Control-Button-1>', self.go_to_entity)

        # self.config(
            # takefocus=1, 
            # anchor='w', 
            # bg=self.formats['bg'], 
            # fg=self.formats['fg'], 
            # font=self.formats['input_font'])
        # self.grid_configure(sticky='ew')

    # def go_to_entity(self, evt):
        # '''
            # self.change_person is for the name of the function passed
            # to this widget when it's made which changes the current
            # person displayed on the persons tab.
        # '''

        # if self.table is None:
            # return

        # self.change_person(
            # self.table.master,
            # self.table.main.persons.attributes_content,
            # self.table.main.new_person_fill,
            # self.table.main.persons.top_pic_button,
            # self.table.main,
            # self.table.main.tabs.store['person'],
            # self.subject_id)

    # def set_focus(self, evt):
        # self.focus_set()

    # def highlight_on_enter(self, evt):
        # self.config(bg=self.formats['highlight_bg'])

    # def unhighlight_on_leave(self, evt):
        # self.config(bg=self.formats['bg'])

# # for demo of LabelCopiable see label_with_selectable_text.py

# class Textx(tk.Text):
    # def __init__(self, master, *args, **kwargs):
        # tk.Text.__init__(self, master, *args, **kwargs)

    # def winfo_subclass(self):
        # '''  '''
        # subclass = type(self).__name__
        # return subclass

# class Text(Textx):
    # def __init__(self, master, *args, **kwargs): 
        # Textx.__init__(self, master, *args, **kwargs)
        # self.config(
            # wrap='word', 
            # bg=formats['bg'], 
            # fg=formats['fg'],
            # insertbackground=formats['fg'])

# class LabelStylable(Textx):
    # def __init__(self, master, *args, **kwargs):
        # Textx.__init__(self, master, *args, **kwargs)

        # self.master = master
        # self.bind('<Map>', lambda event: self.set_height())
        # self.tag_config('bold', font="Helvetica 12 bold")
        # self.tag_config('italic', font="Helvetica 12 italic")
        # self.config(wrap='word', padx=12, pady=12)

    # def set_height(self):

        # height = self.count(1.0, 'end', 'displaylines')
        # self.config(height=height)
        # self.configure(state="disabled")

# # # to use LabelStylable:
# # stylin = LabelStylable(root, width=75)
# # stylin.insert("end", "Hello, ") 
# # stylin.insert("end", "silly ", "italic") 
# # stylin.insert("end", "world", "bold")

# class MessageCopiable(Textx):
    # ''' 
        # To use as a Label whose text can be selected 
        # with mouse, set the state to disabled after 
        # constructing the widget and giving it text. 
        # Enable temporarily to change color or text, for example.
    # '''

    # def __init__(self, master, *args, **kwargs):
        # Textx.__init__(self, master, *args, **kwargs)

        # self.config(
            # bg=formats['bg'],
            # fg=formats['fg'],
            # borderwidth=0, 
            # wrap='word',
            # state='disabled',
            # font=(formats['output_font']),  
            # takefocus=0)
       
    # def set_height(self):
        # # answer is wrong first time thru mainloop so update:
        # self.update_idletasks()
        # lines = self.count('1.0', 'end', 'displaylines')
        # self.config(height=lines)

        # self.tag_configure('center', justify='center')
        # self.tag_add('center', '1.0', 'end')
        # self.config(state='disabled')
    # # How to use above by example:
    # # www = wdg.MessageCopiable(root, width=32)
    # # www.insert(1.0, 
        # # 'Maecenas quis elit eleifend, lobortis turpis at, iaculis '
        # # 'odio. Phasellus congue, urna sit amet posuere luctus, mauris '
        # # 'risus tincidunt sapien, vulputate scelerisque ipsum libero at '
        # # 'neque. Nunc accumsan pellentesque nulla, a ultricies ex '
        # # 'convallis sit amet. Etiam ut sollicitudi felis, sit amet '
        # # 'dictum lacus. Mauris sed mattis diam. Pellentesque eu malesuada '
        # # 'ipsum, vitae sagittis nisl Morbi a mi vitae nunc varius '
        # # 'ullamcorper in ut urna. Maecenas auctor ultrices orci. '
        # # 'Donec facilisis a tortor pellentesque venenatis. Curabitur '
        # # 'pulvinar bibendum sem, id eleifend lorem sodales nec. Mauris '
        # # 'eget scelerisque libero. Lorem ipsum dolor sit amet, consectetur '
        # # 'adipiscing elit. Integer vel tellus nec orci finibus ornare. '
        # # 'Praesent pellentesque aliquet augue, nec feugiat augue posuere ')
    # # www.grid()
    # # www.set_height()
        
# class Checkbuttonx(tk.Checkbutton):
    # def __init__(self, master, *args, **kwargs):
        # tk.Checkbutton.__init__(self, master, *args, **kwargs)
        # pass

    # def winfo_subclass(self):
        # '''  '''
        # subclass = type(self).__name__
        # return subclass

# class Checkbutton(Checkbuttonx):
    # def __init__(self, master, *args, **kwargs):
        # Checkbuttonx.__init__(self, master, *args, **kwargs)
        # ''' 
            # To see selection set the selectcolor 
            # option to either bg or highlight_bg.
        # '''
        # self.config(
            # bg=formats['bg'],
            # fg=formats['fg'], 
            # activebackground=formats['highlight_bg'],
            # selectcolor=formats['bg'], 
            # padx=6, pady=6) 
       
# class Radiobuttonx(tk.Radiobutton):
    # def __init__(self, master, *args, **kwargs):
        # tk.Radiobutton.__init__(self, master, *args, **kwargs)
        # pass

    # def winfo_subclass(self):
        # '''  '''
        # subclass = type(self).__name__
        # return subclass 

# class Radiobutton(Radiobuttonx):
    # def __init__(self, master, *args, **kwargs):
        # Radiobuttonx.__init__(self, master, *args, **kwargs)
        # ''' 
            # To see selection set the selectcolor 
            # option to either bg or highlight_bg.
        # '''
        # self.config(
            # bg=formats['bg'],
            # fg=formats['fg'], 
            # activebackground=formats['highlight_bg'],
            # selectcolor=formats['bg'], 
            # padx=6, pady=6) 

# class RadiobuttonBig(Radiobutton):
    # def __init__(self, master, *args, **kwargs):
        # Radiobutton.__init__(self, master, *args, **kwargs)
        # ''' 
            # If the main content of a dialog is a set of radiobuttons,
            # use standard text size.
        # '''
        # self.config(font=formats['output_font'])

# class RadiobuttonHilited(Radiobuttonx):
    # def __init__(self, master, *args, **kwargs):
        # Radiobuttonx.__init__(self, master, *args, **kwargs)

        # self.config(
            # bg=formats['highlight_bg'], 
            # activebackground=formats['bg'],
            # highlightthickness=3,
            # overrelief='sunken',
            # font=formats['output_font'],
            # fg=formats['fg'],
            # selectcolor=formats['highlight_bg'], 
            # padx=6, pady=6) 

# class Toplevelx(tk.Toplevel):
    # '''
        # All my toplevels have to declare a parent whether they need one or not.
        # This keeps the code consistent and symmetrical across all widgets,
        # even though Tkinter doesn't require a parent for its Toplevel.
    # '''

    # def __init__(self, master, *args, **kwargs):
        # tk.Toplevel.__init__(self, master, *args, **kwargs)

    # def winfo_subclass(self):
        # '''  '''
        # subclass = type(self).__name__
        # return subclass

# class Toplevel(Toplevelx):
    # def __init__(self, master, *args, **kwargs):
        # Toplevelx.__init__(self, master, *args, **kwargs)

        # self.config(bg=formats['bg'])

# class ToplevelHilited(Toplevelx):
    # def __init__(self, *args, **kwargs):
        # Toplevelx.__init__(self, *args, **kwargs)

        # self.config(bg=formats['highlight_bg'])

# class ToolTip(Toplevelx):

    # ''' 
        # I think I stopped working on this for some reason so it's
        # probably not finished.
        
        # Text tips that show full text when some text doesn't show
        # due to the column being too narrow. Part of my 
        # never-ending quest to eradicate resizable columns from GUI 
        # applications that wouldn't need resizable columns if they
        # were designed for their space to hold the information they
        # are supposed to display.

        # To use:
        # instance = ToolTip(parent, overwidthtip=True)
        # instance.hoverees.extend([ent2, ent1, lab3, radio2])
        # instance.bind_widgets()
    # '''

    # def __init__(self, master, overwidthtip=False, *args, **kwargs):
        # Toplevelx.__init__(self, master, *args, **kwargs)
        
        # self.withdraw()

        # self.overwidthtip = overwidthtip
        # self.widget = None
        # self.text = ''
        # self.hoverees = []

        # self.x = self.y =  0  

        # self.wm_overrideredirect(1)

        # self.make_widgets()

    # def make_widgets(self): 

        # self.label = LabelNegative(
            # self, 
            # justify='left',
            # relief='solid', 
            # bd=1)
        # self.label.pack(ipadx=6, ipady=3)

    # def bind_widgets(self):
        # for widg in self.hoverees:
            # widg.bind('<Enter>', self.enter)
            # widg.bind('<Leave>', self.leave)

    # def do_the_geometry(self):

        # maxvert = self.widget.winfo_screenheight()

        # x, y, cx, cy = self.widget.bbox('insert')  

        # mouse_at = self.widget.winfo_pointerxy()

        # tip_shift = 32 

        # if mouse_at[1] < maxvert - tip_shift * 2:
            # x = mouse_at[0] + tip_shift
            # y = mouse_at[1] + tip_shift
        # else:
            # x = mouse_at[0] + tip_shift
            # y = mouse_at[1] - tip_shift

        # self.wm_geometry('+{}+{}'.format(x, y))

    # def show_tip(self):
        # self.do_the_geometry()
        # self.deiconify()

    # def enter(self, evt):
        # self.widget = evt.widget
        # self.text = self.widget.get()
        # self.config_tip()

    # def leave(self, evt):
        # self.hide_tip()

    # def hide_tip(self):
        # self.withdraw()
        # self.label.config(text='')

    # def config_tip(self):
        # if self.overwidthtip is True:
            # self.config_overwidthtip()
            # return
        # self.label.config(text=self.text)
        # self.show_tip()

    # def config_overwidthtip(self):
        # if len(self.text) > self.widget.cget('width'):
            # self.label.config(text=self.text)
            # self.show_tip()

# class Canvasx(tk.Canvas):
    # def __init__(self, master, *args, **kwargs):
        # tk.Canvas.__init__(self, master, *args, **kwargs)
        # pass

    # def winfo_subclass(self):
        # '''  '''
        # subclass = type(self).__name__
        # return subclass

# class Canvas(Canvasx):
    # def __init__(self, master, *args, **kwargs):
        # Canvasx.__init__(self, master, *args, **kwargs)

        # self.config(bg=formats['bg'], bd=0, highlightthickness=0)

# class CanvasHilited(Canvasx):
    # def __init__(self, master, *args, **kwargs):
        # Canvasx.__init__(self, master, *args, **kwargs)

        # self.config(bg=formats['highlight_bg'], bd=0, highlightthickness=0)  

# # ************** statusbar tooltips sizegrip **************

# '''
    # Statusbar messages on focus-in to individual widgets,
    # non-obtrusive tooltips, and non-ttk replacement for ttk.Sizegrip.
# '''

# def run_statusbar_tooltips(visited, status_label, tooltip_label):
    # '''
        # Uses lambda to add args to event
        # since tkinter expects only one arg in a callback.
    # '''

    # def handle_statusbar_tooltips(event):
        # for tup in visited:
            # if tup[0] is event.widget:
                # if event.type == '9': # FocusIn
                    # status_label.config(text=tup[1])
                # elif event.type == '10': # FocusOut
                    # status_label.config(text='')
                # elif event.type == '7': # Enter
                    # tooltip_label.grid(
                        # column=1, row=0, 
                        # sticky='e', padx=(6,24))
                    # tooltip_label.config(
                        # text=tup[2],
                        # bg='black',
                        # fg='white',
                        # font=formats['status'])
                # elif event.type == '8': # Leave
                    # tooltip_label.grid_remove()
                    # tooltip_label.config(
                        # bg=formats['bg'], text='', fg=formats['bg'])

    # statusbar_events = ['<FocusIn>', '<FocusOut>', '<Enter>', '<Leave>']

    # for tup in visited:
        # widg = tup[0]
        # status = tup[1]
        # tooltip = tup[2]
        # for event_pattern in statusbar_events:
            # # error if tup[0] has been destroyed 
            # #   so don't use these with destroyable widgets
            # # different tooltips are available in utes.py
            # widg.bind(event_pattern, handle_statusbar_tooltips, add='+')

        # status_label.config(font=formats['status'])

# class StatusbarTooltips(Frame):
    # '''
        # To use this:
        # In self.make_widgets()...
            # some_statusbar = wdg.StatusbarTooltips(self)
            # some_statusbar.grid(column=0, row=2, sticky='ew') # use last row in toplevel
            # visited = (
                # (self.widget1, 
                    # 'status bar message on focus in', 
                    # 'tooltip message on mouse hover.'),
                # (self.widget2, 
                    # 'status bar message on focus in', 
                    # 'tooltip message on mouse hover.'))        
            # wdg.run_statusbar_tooltips(
                # visited, 
                # roles_statusbar.status_label, 
                # roles_statusbar.tooltip_label)
        # If parent is a Toplevel and you don't want the Toplevel to be resizable,
        # use resizer=False when instantiating the Statusbar and add this:
            # dialog.resizable(False, False) --that's width and height in that order.

    # '''

    # def __init__(self, master, resizer=True, *args, **kwargs):
        # Frame.__init__(self, master, *args, **kwargs)

        # self.master = master # root or toplevel

        # self.sizer = Sizer(self.master)

        # self.grid_columnconfigure(0, weight=1)
        # # With custom window border, you can't use the otherwise 
        # #   desirable option bd=2, relief='sunken' for a border on statusbar
        # #   because edge grabber for resizing is below statusbar 
        # #   so border looks wrong there. Instead put a Separator 
        # #   above the statusbar frame.
        # # relief = Frame(self, bd=2, relief='sunken')
        # relief = Frame(self, bd=0)
        # relief.grid(column=0, row=0, sticky='news')
        # relief.grid_columnconfigure(0, weight=1)

        # self.status_label = Label(
            # relief, cursor='arrow', anchor='w', )
        # self.tooltip_label = Label(
            # relief, bd=2, relief='sunken', anchor='e')

        # if resizer is True:
            # self.sizer.place(relx=1.0, x=-3, rely=1.0, anchor='se')
            # self.sizer.bind('<Button-1>', self.sizer.get_pos)
        # self.status_label.grid(column=0, row=0, sticky='w')

# class Sizer(Label):
    # def __init__(self, master, icon='sizer_15_dark', *args, **kwargs):
        # Label.__init__(self, master, *args, **kwargs)
        # ''' 
            # SE corner gripper/resizer. Replaces ttk.Sizegrip.
            # The master has to be the toplevel window being resized.
            # Since it's placed, not gridded, it will overlap so
            # the statusbar tooltips had to be moved to the left
            # with padding. See StatusbarTooltips class in widgets.py
            # for an example of how to place() and bind() this. 
        # '''

        # self.master = master
        # self.click_x = 0
        # self.click_y = 0
# # D:\treebard_gps\app\python\images\icons
        # print("line", looky(seeline()).lineno, "current_drive:", current_drive)
        # print("line", looky(seeline()).lineno, "project_path:", project_path)
        # file = '{}images/icons/{}.png'.format(project_path, icon)
        # print("line", looky(seeline()).lineno, "file:", file)
        # img = Image.open(file)
        # self.tk_img = ImageTk.PhotoImage(img)

        # self.config(
            # bg=formats['bg'], 
            # bd=0, 
            # cursor='size_nw_se',
            # image=self.tk_img)

    # def get_pos(self, evt):

        # def resize_se(event):
            # x_on_move = event.x_root
            # y_on_move = event.y_root
            # dx = x_on_move - click_x
            # dy = y_on_move - click_y
            # new_w = orig_w + dx
            # new_h = orig_h + dy

            # if new_w < 10:
                # new_w = 10
            # if new_h < 10:
                # new_h = 10
            # self.master.geometry('{}x{}'.format(new_w, new_h))

        # orig_geom = self.master.geometry()
        # orig_geom = orig_geom.split('+')[0].split('x')
        # orig_w = int(orig_geom[0])
        # orig_h = int(orig_geom[1])
        # click_x = evt.x_root
        # click_y = evt.y_root

        # self.bind('<B1-Motion>', resize_se)

# # class TabBook(Framex):

    # # def __init__(
            # # self, master, root=None, side='nw', bd=0, tabwidth=9, 
            # # selected='', tabs=[],  minx=0.90, 
            # # miny=0.85, case='title', *args, **kwargs):
        # # Framex.__init__(self, master, *args, **kwargs)
        # # '''
            # # The tab is the part that sticks out with the title 
            # # you click to activate the page which holds that 
            # # tab's content. To add widgets grid them with 
            # # instance.store[page] as the master. For example: 
            # # inst.store['place'] where 'place' is a string from 
            # # the original tabs parameter (list of tuples). 
        # # '''

        # # self.master = master
        # # self.side = side
        # # self.bd = bd
        # # self.tabwidth = tabwidth
        # # self.selected = selected
        # # self.minx = self.master.winfo_screenwidth() * minx
        # # self.miny = self.master.winfo_screenheight() * miny
        # # self.case = case

        # # self.formats = make_formats_dict()
        
        # # self.tabdict = {}
        # # for tab in tabs:
            # # self.tabdict[tab[0]] = [tab[1]]
            # # # key is 'title', value is ['acceLerator']
            # # # value will have page appended to it

        # # self.store = {}

        # # self.active = None

        # # self.make_widgets()   
        # # self.open_tab_alt(root)

    # # def make_widgets(self):
        # # '''  '''

        # # self.tab_base = Frame(self)
        # # self.border_base = FrameHilited2(self)
        # # self.notebook = Frame(self.border_base)
        # # self.tab_frame = FrameHilited2(self.tab_base)
        # # self.tabless = Frame(self.tab_base)
        # # self.spacer = Frame(self.tabless)
        # # self.top_border = FrameHilited2(self.tabless, height=1)

        # # self.grid_columnconfigure(1, weight=1)
        # # self.grid_rowconfigure(0, weight=1)
        # # self.grid_rowconfigure(1, weight=1)

        # # self.notebook.grid_columnconfigure(0, weight=1, minsize=self.minx)
        # # self.notebook.grid_rowconfigure(0, weight=1, minsize=self.miny)

        # # self.grid_tabs()  

        # # c = 0
        # # for tab in self.tabdict:
            # # lab = Label(
                # # self.tab_frame,
                # # width=int(self.tabwidth),
                # # takefocus=1)  
            # # if self.case == 'title':
                # # lab.config(text=tab.title())   
            # # elif self.case == 'lower':
                # # lab.config(text=tab.lower())    
            # # elif self.case == 'upper':
                # # lab.config(text=tab.upper())     
            # # self.tabdict[tab].append(lab)

            # # if self.side in ('ne', 'nw'):
                # # lab.grid(column=c, row=0, padx=1, pady=(1, 0))
            # # elif self.side in ('se', 'sw'):
                # # lab.grid(column=c, row=0, padx=1, pady=(0, 1))

            # # lab.bind('<Button-1>', self.make_active)
            # # lab.bind('<FocusIn>', self.highlight_tab)
            # # lab.bind('<FocusOut>', self.unhighlight_tab)
            # # lab.bind('<Key-space>', self.make_active)
            # # lab.bind('<Key-Return>', self.make_active)
            # # lab.bind('<ButtonRelease-1>', self.unhighlight_tab)
            # # create_tooltip(lab, 'Alt + {}'.format(self.tabdict[tab][0]))
            # # page = Frame(self.notebook)
            # # page.grid(column=0, row=0, sticky='news')
            # # page.grid_remove()
            # # self.tabdict[tab].append(page)
            # # # simplify tab references w/ a dict whose value is just a widget
            # # self.store[tab] = page
            # # c += 1
        
        # # selected_page = self.tabdict[self.selected][2] # page
        # # selected_page.grid()

        # # self.active = self.tabdict[self.selected][1] # tab
        # # self.make_active()

    # # def grid_tabs(self):

        # # if self.side in ('nw', 'ne'):
            # # pady = (0, 1)
            # # tab_row = 0
            # # body_row = 1
            # # spacer_row = 0
            # # border_row = 1

        # # elif self.side in ('sw', 'se'):
            # # pady=(1, 0)
            # # tab_row = 1
            # # body_row = 0
            # # spacer_row = 1
            # # border_row = 0

        # # if self.side in ('nw', 'sw'):
            # # tab_col = 0
            # # tabless_col = 1                

        # # elif self.side in ('ne', 'se'):
            # # tab_col = 1
            # # tabless_col = 0                

        # # # self.notebook switches pady
        # # self.notebook.grid(column=0, row=0, padx=1, pady=pady, sticky='news')
        # # # self.tab_base and borderbase switch rows
        # # self.tab_base.grid(column=0, row=tab_row, sticky='news')
        # # self.tab_base.grid_columnconfigure(tabless_col, weight=1)
        # # self.tab_base.grid_rowconfigure(0, weight=1)
        # # self.border_base.grid(column=0, row=body_row, sticky='news')
        # # # self.tab_frame and self.tabless switch cols
        # # self.tab_frame.grid(column=tab_col, row=0, sticky='ew')
        # # self.tabless.grid(column=tabless_col, row=0, sticky='news')
        # # self.tabless.grid_columnconfigure(0, weight=1)
        # # self.tabless.grid_rowconfigure(spacer_row, weight=1)
        # # # self.spacer and self.top_border switch rows
        # # self.spacer.grid(column=0, row=tab_row, sticky='ns')
        # # self.top_border.grid(column=0, row=border_row, sticky='ew') 

    # # def highlight_tab(self, evt):
        # # # accelerators don't work if notebook not visible
        # # if evt.widget in self.store.values():
            # # evt.widget.config(fg='yellow')

    # # def unhighlight_tab(self, evt):
        # # # accelerators don't work if notebook not visible
        # # if evt.widget in self.store.values():
            # # evt.widget.config(fg=self.formats['fg'])

    # # def make_active(self, evt=None):
        # # ''' Open the selected tab & reconfigure it to look open. '''

        # # self.formats = make_formats_dict()

        # # # position attributes are needed in the instance
        # # self.posx = self.winfo_rootx()
        # # self.posy = self.winfo_rooty()    

        # # # if not running on load
        # # if evt:
            # # self.active = evt.widget
            # # self.active.focus_set()

            # # # if evt was alt key accelerator
            # # if (evt.widget is self.master or 
                    # # evt.keysym not in ('space', 'Return')):

                # # for k,v in self.tabdict.items():
                    # # if evt.keysym in (v[0], v[0].lower()):
                        # # self.active = v[1]
                        # # self.active.focus_set()
                        
            # # # if evt was spacebar, return key, or mouse button
            # # elif evt.type in ('2', '4'):
                # # self.active.config(fg=self.formats['fg'])

            # # # remove all pages and regrid the right one
            # # for k,v in self.tabdict.items():
                # # if self.active == v[1]:
                    # # for widg in self.tabdict.values():
                        # # widg[2].grid_remove()
                    # # v[2].grid()

        # # # unhighlight all tabs
        # # for tab in self.tabdict.values():            
            # # tab[1].config(
                # # bg=self.formats['highlight_bg'])

        # # # highlight active tab
        # # self.active.config(
            # # bg=self.formats['bg'],
            # # font=self.formats['heading3'])

    # # def open_tab_alt(self, root_window):
        # # ''' Bindings for notebook tab accelerators. '''
        # # for k,v in self.tabdict.items():
            # # key_combo_upper = '<Alt-Key-{}>'.format(v[0])  
            # # root_window.bind(key_combo_upper, self.make_active)
            # # key_combo_lower = '<Alt-Key-{}>'.format(v[0].lower()) 
            # # root_window.bind(key_combo_lower, self.make_active)

            # # unkey_combo_upper = '<Alt-KeyRelease-{}>'.format(v[0])            
            # # root_window.bind_all(unkey_combo_upper, self.unhighlight_tab)
            # # unkey_combo_lower = '<Alt-KeyRelease-{}>'.format(v[0].lower()) 
            # # root_window.bind_all(unkey_combo_lower, self.unhighlight_tab)

# # ttk only below this point *********************************************

# class Notebookx(ttk.Notebook):
    # def __init__(self, master, *args, **kwargs):
        # ttk.Notebook.__init__(self, master, *args, **kwargs)

    # def winfo_subclass(self):
        # subclass = type(self).__name__
        # return subclass

# class Tabs(Notebookx):
    # def __init__(self, master, tab_names, *args, **kwargs):
        # Notebookx.__init__(self, master, *args, **kwargs)

        # self.master = master
        # self.tab_names = tab_names

        # self.store = {}

        # self.enable_traversal()

        # for tup in self.tab_names:
            # tab_frm = Frame(self, name='{}_tab'.format(tup[0]))
            # self.add(tab_frm)
            # self.tab(tab_frm, text=tup[0].title(), underline=tup[1], padding='16')
            # self.store[tup[0]] = tab_frm

# class Comboboxx(ttk.Combobox):
    # '''
        # Provides a way of changing colors in the combobox listbox
        # dropdown/popdown as well as the ability to detect subclass.
    # '''

    # def __init__(self, master, *args, **kwargs):
        # ttk.Combobox.__init__(self, master, *args, **kwargs)

    # def winfo_subclass(self):
        # subclass = type(self).__name__
        # return subclass

    # def config_popdown(self, **kwargs):
        # self.tk.eval(
            # '[ttk::combobox::PopdownWindow {}].f.l configure {}'.format(
                # self, 
                # ' '.join(self._options(kwargs))))

# class ClickAnywhereCombo(Comboboxx):
    # ''' 
        # User can ctrl+click in entry box or arrow--not just arrow--
        # to make dropdown fly down. Not needed for readonly combobox 
        # which already does this. Problem with using plain click for
        # this: it prevents dragging in the entry to select text.
        # So ctrl+click is a compromise, so that dragging to highlight 
        # will still work normally, and the arrow works normally.
    # '''

    # def __init__(self, master, *args, **kwargs):
        # Comboboxx.__init__(self, master, *args, **kwargs)
        # self.bind('<Control-Button-1>', self.fly_down_on_click)
        # self.config(font=formats['input_font'])

    # def fly_down_on_click(self, evt):
        # if int(evt.type) == 4:
            # w = evt.widget
            # w.event_generate('<Down>', when='head')  

# class ClearableReadonlyCombobox(Comboboxx):
    # '''
        # User can clear mistaken selection by pressing Delete, 
        # Escape, or Backspace.
    # '''

    # def __init__(self, master, *args, **kwargs):
        # Comboboxx.__init__(self, master, *args, **kwargs)
        # self.state(['readonly'])
        # self.bind("<Key-Delete>", self.allow_manual_deletion)
        # self.bind("<Key-Escape>", self.allow_manual_deletion)
        # self.bind("<Key-BackSpace>", self.allow_manual_deletion)

    # def allow_manual_deletion(self, evt):
        # if self.get() != "":
            # if evt.keysym in ("Escape", "Delete", "BackSpace"):
                # self.delete_content()

    # def delete_content(self):
        # self.state(['!readonly', 'selected'])
        # self.set("")
        # self.state(['readonly'])

# class GromboReadonly(ClearableReadonlyCombobox):
    # ''' 
        # Provides grayed-out italic default text. User cannot add values
        # by typing into the entry part of the combobox.
    # '''

    # def __init__(self, master, default_text, *args, **kwargs):
        # ClearableReadonlyCombobox.__init__(self, master, *args, **kwargs)

        # self.default_text = default_text
        # var = tk.StringVar()
        # var.set(self.default_text)
        # self.config(
            # foreground=formats['head_bg'],
            # font=formats['show_font'], 
            # textvariable=var)
        # self.textvariable = var

        # self.bind('<Button-1>', self.clear_default_text, add='+')
        # self.bind('<FocusIn>', self.clear_default_text)
        # self.bind('<FocusOut>', self.clear_selection)

    # def clear_default_text(self, evt=None):
        # if 'disabled' in self.state():
            # return
        # if self.get() == self.default_text:
            # self.delete(0, 'end')
            # self.config(foreground=formats['fg'])
            # self.config(font=formats['input_font'])
            
        # else:
            # self.config(foreground=formats['fg'])
            # self.config(font=formats['input_font'])

    # def clear_selection(self, evt):
        # if len(self.get()) == 0:
            # self.insert(0, self.default_text)
            # self.config(foreground=NEUTRAL_COLOR, font=formats['show_font'])
        # self.select_clear()  

    # def show_error(self):
        # self.config(font=formats['input_font'])
        # self.config(foreground='red')

# class Grombo(ClickAnywhereCombo):
    # ''' 
        # Provides grayed-out italic default text. User can add values
        # by typing into the entry part of the combobox.
    # '''

    # def __init__(self, master, default_text, *args, **kwargs):
        # ClickAnywhereCombo.__init__(self, master, *args, **kwargs)

        # self.default_text = default_text
        # var = tk.StringVar()
        # var.set(self.default_text)
        # self.config(
            # foreground=formats['head_bg'],
            # font=formats['show_font'], 
            # textvariable=var)
        # self.textvariable = var

        # self.bind('<Button-1>', self.clear_default_text, add='+')
        # self.bind('<FocusIn>', self.clear_default_text)
        # self.bind('<FocusOut>', self.clear_selection)

    # def clear_default_text(self, evt=None):
        # if 'disabled' in self.state():
            # return
        # if self.get() == self.default_text:
            # self.delete(0, 'end')
            # self.config(foreground=formats['fg'])
            # self.config(font=formats['input_font'])
            
        # else:
            # self.config(foreground=formats['fg'])
            # self.config(font=formats['input_font'])

    # def clear_selection(self, evt=None):
        # if len(self.get()) == 0:
            # self.insert(0, self.default_text)
            # self.config(foreground=NEUTRAL_COLOR, font=formats['show_font'])
        # self.select_clear()  

    # def show_error(self):
        # self.config(font=formats['input_font'])
        # self.config(foreground='red')

