# treebard_root_022.py

import tkinter as tk
from PIL import Image, ImageTk
import tkinter as tk
from files import project_path, current_file
from window_border import Border
from scrolling import MousewheelScrolling
from styles import config_generic, make_formats_dict
from main import Main
from widgets import Toplevel
import dev_tools as dt
from dev_tools import looky, seeline



'''
IMPORTS STRUCTURE:

               window_border 
               |  |    |   |
               |  |    |   places
               |  |    |       |
               |  |  events_table                              
               |  |  |   |         
               |  main   |                                  
               |         |                           
               treebard_root_020                                            
                                                       
                    
'''         

class Treebard():

    def __init__(self, root):
        self.root = root
        self.make_main_canvas_and_border()
        self.configure_mousewheel_scrolling()

    def make_main_canvas_and_border(self):
        self.canvas = Border(
            self.root, 
            size=4, # use 3, 4, 7, or 11
            menubar=True, 
            ribbon_menu=True)
        self.canvas.title_1.config(text="Treebard GPS")
        self.canvas.title_2.config(text=current_file)
        self.main = Main(self.canvas, self.root, self)
        self.canvas.create_window(0, 0, anchor='nw', window=self.main)

    def configure_mousewheel_scrolling(self):
        self.scroll_mouse = MousewheelScrolling(self.root, self.canvas)
        self.scroll_mouse.append_to_list([self.canvas, self.main])
        self.scroll_mouse.configure_mousewheel_scrolling(in_root=True)

def main():

    root = tk.Tk()

    root.geometry('+100+50')
    root.overrideredirect(1)
    root.iconbitmap(default='{}favicon.ico'.format(project_path)) 
    Treebard(root)

    config_generic(root)

    root.mainloop()

if __name__ == '__main__':
    main()

