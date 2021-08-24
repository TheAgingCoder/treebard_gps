# events_table

import tkinter as tk
import sqlite3
from files import current_file
from window_border import Border 
from widgets import (
    Frame, LabelDots, LabelButtonText, Toplevel, Label, 
    KinTip, LabelH3, Button) 
from place_autofill import EntryAuto
from nested_place_strings import make_all_nestings
from toykinter_widgets import Separator
from styles import make_formats_dict, config_generic
from names import get_name_with_id
from roles import RolesDialog
from notes import NotesDialog
from places import place_strings, ValidatePlace
from query_strings import (
    select_finding_places_nesting, select_current_person_id, 
    select_all_event_types_couple, select_all_kin_types_couple,
    select_all_findings_current_person, select_findings_details_generic,
    select_findings_details_couple_age, select_findings_details_couple_generic,
    select_finding_id_birth, select_person_id_kin_types_birth,
    select_finding_ids_age_parents, select_person_id_birth,
    select_findings_details_offspring, select_all_findings_roles_ids, 
    select_finding_ids_offspring, select_all_findings_notes_ids,
    select_count_finding_id_sources, select_nesting_fk_finding,
    select_nestings_and_ids, select_place, update_finding_particulars,
    update_finding_age, update_current_person, select_all_place_ids
)
import dev_tools as dt
from dev_tools import looky, seeline





formats = make_formats_dict()

FINDING_TABLE_HEADS = (
    'Event', 'Date', 'Place', 'Particulars', 'Age', 
    'Kin', 'Roles', 'Notes', 'Sources')

def get_current_person():
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_current_person_id)
    current_person = cur.fetchone()[0]
    cur.close()
    conn.close()
    return current_person

def get_findings():

    current_person = get_current_person()
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()

    # get couple event types and couple kin types
    cur.execute(select_all_event_types_couple)
    couple_event_types = cur.fetchall()
    couple_event_types = [i[0] for i in couple_event_types]

    cur.execute(select_all_kin_types_couple)
    couple_kin_type_ids = cur.fetchall()
    couple_kin_type_ids = [i[0] for i in couple_kin_type_ids]

    # get generic events
    generic_findings = []
    cur.execute(select_all_findings_current_person, (current_person,))
    generic_finding_ids = cur.fetchall()
    generic_finding_ids = [i[0] for i in generic_finding_ids]

    for finding_id in generic_finding_ids: 
        cur.execute(select_findings_details_generic, (finding_id,))

        generic_finding_details = cur.fetchone()
        generic_finding_details = list(generic_finding_details) 

        cur.execute(select_finding_places_nesting, (finding_id,))
        place_string = cur.fetchone()
        place_string = [i for i in place_string if i]
        place_string = ', '.join(place_string)
        generic_finding_details.insert(3, place_string)
        generic_finding_details[1] = generic_finding_details[1:3]

        del generic_finding_details[2]
        generic_finding_details.insert(0, finding_id)
        generic_findings.extend([generic_finding_details])

    for lst in generic_findings:
        if lst[3] == 'unknown':
            lst[3] = ''

    couple_age_spouse = []
    generic_couple_findings = []    

    sql =   '''
                SELECT finding_id, kin_type_id 
                FROM findings_persons 
                WHERE person_id = (SELECT person_id FROM current WHERE current_id = 1)
                    AND kin_type_id in ({}) 
            '''.format(
                ','.join('?' * len(couple_kin_type_ids)))

    cur.execute(sql, couple_kin_type_ids)

    finding_ids_kin_type_ids = cur.fetchall()

    for event in finding_ids_kin_type_ids:
        cur.execute(select_findings_details_couple_age, event)
        got = cur.fetchall()
        finding_id = event[0]
        for tup in got:
            if len(got) == 2:
                couple_finding_details = [finding_id, got[0], got[1]]
            elif len(got) == 1:
                couple_finding_details = [finding_id, got[0], (None, '')]
        couple_age_spouse.append(couple_finding_details)
        cur.execute(select_findings_details_couple_generic, (finding_id,))
        couple_generic_details = cur.fetchall()
        couple_generic_details = [list(i) for i in couple_generic_details]
        couple_generic_details[0].insert(0, finding_id)

        cur.execute(select_finding_places_nesting, (finding_id,))
        place_string = cur.fetchone()
        place_string = [i for i in place_string if i]
        place_string = ', '.join(place_string)
        couple_generic_details[0][4] = place_string

        generic_couple_findings.extend(couple_generic_details)
    for item in generic_couple_findings:
        if item[4] == 'unknown':
            item[4] = ''

    # get birth events
    cur.execute(select_finding_id_birth, (current_person,))
    birth_id = cur.fetchone()
    parents = (None, None)
    if birth_id:
        birth_id = birth_id[0]
        cur.execute(select_person_id_kin_types_birth, (birth_id,))
        parents = cur.fetchall()
        parents.insert(0, birth_id)

    cur.execute(select_finding_ids_age_parents, (current_person,))
    children = cur.fetchall()
    children = [list(i) for i in children]
    for lst in children:
        finding_id = lst[0]

        cur.execute(select_person_id_birth, (finding_id,))
        offspring = cur.fetchone()
        if offspring:
            lst.insert(2, offspring[0])

    kids = []
    for lst in children:
        child_id = lst[2]
        
        cur.execute(select_findings_details_offspring, (child_id,))
        offspring_details = list(cur.fetchall()[0])

        cur.execute(select_finding_places_nesting, (finding_id,))
        place_string = cur.fetchone()
        place_string = [i for i in place_string if i]
        place_string = ', '.join(place_string)
        offspring_details[2] = place_string
        if offspring_details[2] == 'unknown':
            offspring_details[2] = ''

        name = get_name_with_id(child_id)
        new_list = [lst[0], lst[1], [name, child_id, 'child']] 
        new_list.insert(1, 'offspring')
        new_list.insert(2, [offspring_details[0], offspring_details[1]])
        new_list.insert(3, offspring_details[2])
        new_list.insert(4, offspring_details[3])
        kids.append(new_list) 

    finding_ids = []

    for lst in generic_findings:
        if lst[0] not in finding_ids:
            finding_ids.append(lst[0])
    for lst in generic_couple_findings:
        if lst[0] not in finding_ids:
            finding_ids.append(lst[0])
    for lst in children:
        if lst[0] not in finding_ids:
            finding_ids.append(lst[0])

    couple_findings = []
    for finding in generic_couple_findings:
        for spouse_age in couple_age_spouse:
            if finding[0] == spouse_age[0]:
                for spouse in spouse_age[1:]:
                    if spouse[0] == current_person:
                        finding.append(spouse[1])
                for spouse in spouse_age[1:]:
                    if spouse[0] != current_person:
                        spouse_id = spouse[0]
                        name = get_name_with_id(spouse_id)
                        kin_type = spouse[2]
                        finding.append([name, spouse_id, kin_type])
        finding[2] = finding[2:4]
        del finding[3]
        couple_findings.append(finding)

    couple_finding_ids = [i[0] for i in finding_ids_kin_type_ids]
    all_finding_ids = generic_finding_ids + couple_finding_ids

    cur.execute(select_all_findings_roles_ids)

    non_empty_roles = cur.fetchall()
    non_empty_roles = [i[0] for i in non_empty_roles]

    current_roles = []
    for role_id in all_finding_ids:
        if role_id in non_empty_roles:
            current_roles.append(role_id)
    cur.execute(select_finding_ids_offspring, (current_person,))
    offspring_events = cur.fetchone()

    if offspring_events:
        offspring_roles = []
        for finding_id in offspring_events:
            if finding_id in non_empty_roles:
                offspring_roles.append(finding_id)
        current_roles.extend(offspring_roles)
    non_empty_roles = current_roles

    cur.execute(select_all_findings_notes_ids)

    non_empty_notes = cur.fetchall()
    non_empty_notes = [i[0] for i in non_empty_notes]

    current_notes = []
    for note_id in all_finding_ids:
        if note_id in non_empty_notes:
            current_notes.append(note_id)
    cur.execute(select_finding_ids_offspring, (current_person,))
    offspring_events = cur.fetchone()

    if offspring_events:
        offspring_notes = []
        for finding_id in offspring_events:
            if finding_id in non_empty_notes:
                offspring_notes.append(finding_id)
        current_notes.extend(offspring_notes)
    non_empty_notes = current_notes

    source_count = []
    for finding_id in finding_ids:
        cur.execute(select_count_finding_id_sources, (finding_id,))
        src_count = cur.fetchone()
        source_count.append((finding_id, src_count[0]))

    cur.close()
    conn.close()    

    return (
        generic_findings,
        couple_findings, 
        parents, 
        kids,
        finding_ids,
        non_empty_roles,
        non_empty_notes,
        source_count)

class EventsTable(Frame):
    def __init__(self, master, root, treebard, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.root = root
        self.treebard = treebard

        self.inwidg = None
        self.headers = []
        self.widths = [[], [], [], [], []]
        self.nested_place_id = None
        self.kintips = []

        self.screen_height = self.winfo_screenheight()
        self.column_width_indecrement = -2
        self.row_qty = 5

        self.make_header()
        self.make_table_cells()
        self.make_new_event_row()

    def size_columns_to_content(self):
        '''
            Get length of each cell in the column and size the top row cells to 
            fit the longest content in the column. The whole column will follow
            this size. The method make_table_cells() has some influence in this
            sizing process because column 0 (Event) sets itself to Tkinter's default
            width=20 if you don't tell it not to and column 4 (Age) should be 
            smaller than the others. Any of this could be improved, especially
            if Tkinter would let us detect and set Labels and Entries to their
            required width but they use different default characters so even
            setting them to the same width doesn't work. One workaround might
            be to have a button in the Preferences > Fonts tab or someplace which
            increases or decreases the column width and redraws the table. Not
            desirable, but I'm trying to avoid manually resizable columns since
            I believe with religious fervor that they are inexcusable and I'm
            waiting to be proven wrong. Thus for future reference: 
            self.column_width_indecrement. If this works out, the button might
            want to be on the Fonts tab since the setting would most often have to
            be changed when redrawing the table in different fonts. Another thing to
            consider is making the input and output fonts the same font family to
            see if that helps.
        '''

        self.header_widths = []
        for lst in self.widths:
            self.header_widths.append(max(lst))
        for row in self.cell_pool:
            c = 0
            for ent in row[1][0:5]:
                if ent.winfo_class() == 'Entry':
                    if ent.winfo_subclass() == 'EntryAuto':
                        if len(ent.grid_info()) != 0:
                            if ent.grid_info()['row'] == 2:
                                ent.config(
                                    width=self.header_widths[c] + self.column_width_indecrement)
                                c += 1      

    def get_initial(self, evt):
        self.initial = evt.widget.get()
        self.inwidg = evt.widget

    def get_final(self, evt):
        widg = evt.widget
        final = widg.get()
        if final != self.initial:
            self.final = final
            for row in self.findings:
                c = 0
                for col in row[0:-1]:
                    if col[0] == widg:
                        self.finding = row[9]
                        col_num = c
                    c += 1
        
            self.update_db(widg, col_num)

    def update_db(self, widg, col_num):
        def update_place():
            cur.execute(select_nesting_fk_finding, (self.finding,))
            nested_place = cur.fetchone()[0]
            self.final = ValidatePlace(
                self.root, 
                self.treebard,
                self.inwidg,
                self.initial,
                self.final,
                self.finding,
                nested_place)

        def update_particulars():
            cur.execute(update_finding_particulars, (self.final, self.finding))
            conn.commit()

        def update_age():
            cur.execute(update_finding_age, (self.final, self.finding))
            conn.commit() 

        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()

        if col_num == 0:
            pass
        elif col_num == 1:
            pass
        elif col_num == 2:
            update_place()
        elif col_num == 3:
            update_particulars()
        elif col_num == 4:
            update_age()

        cur.close()
        conn.close()

    def make_table_cells(self, qty=1998):
        '''
            EntryAuto was used for all the text columns to keep the code 
            symmetrical for all the text columns, with autofill defaulting to 
            False except for the places column.
        '''

        self.table_cells = []
        for i in range(int(qty/9)): # 222
            row = []
            for j in range(9):
                if j < 5:
                    if j == 2:
                        cell = EntryAuto(self, autofill=True)
                    else:                        
                        cell = EntryAuto(self)
                    cell.initial = ''
                    cell.final = ''
                    cell.finding = None
                    cell.bind('<FocusIn>', self.get_initial, add="+")
                    cell.bind('<FocusOut>', self.get_final, add="+")
                    if j == 0:
                        cell.config(width=1)
                    elif j == 4:
                        cell.config(width=5)
                elif j == 5:
                    cell = Frame(self, bd=0, highlightthickness=0)
                elif j == 6:
                    cell = LabelDots(self, current_file, RolesDialog)
                elif j == 7:
                    cell = LabelDots(self, current_file, NotesDialog)
                elif j == 8:
                    cell = LabelButtonText(
                        self,
                        width=6,
                        anchor='w',
                        font=formats['heading3'])
                row.append(cell)
            self.table_cells.append(row)
        self.set_cell_content()

    def set_cell_content(self):

        findings_data = get_findings()

        generic_findings = findings_data[0]
        couple_findings = findings_data[1]
        parents = findings_data[2]
        children = findings_data[3]
        finding_ids = findings_data[4]
        non_empty_roles = findings_data[5]
        non_empty_notes = findings_data[6]
        source_count = findings_data[7]

        self.cell_pool = []

        i = 0
        for row in self.table_cells[0:len(finding_ids)]:
            self.cell_pool.append([finding_ids[i], row])
            i += 1
        self.findings = []
        for finding_id in finding_ids:
            c = 0
            for row in self.cell_pool:
                if row[0] == finding_id:
                    right_cells = row[1]
                    c += 1
                    for final_list in (couple_findings, generic_findings, children):
                        for lst in final_list:
                            if finding_id == lst[0]:
                                right_row = lst[1:]
                                couple_or_no = len(right_row)
                                if couple_or_no == 5:
                                    right_row.extend([[], '     ', '     ', []])
                                elif couple_or_no == 6:
                                    right_row.extend(['     ', '     ', []])
                                row_list = [list(i) for i in zip(right_cells, right_row)]
                                row_list.append(finding_id)
                                self.findings.append(row_list)

        EntryAuto.create_lists(place_strings)

        ma = None
        pa = None
        for row in self.findings:
            if row[0][1] == 'birth':
                finding_id = row[9]
                break
        for row in self.findings:
            if row[9] == finding_id:            
                for item in parents:
                    if item == finding_id:
                        for parent in parents[1:]:
                            if parent[1] == 'mother':
                                ma = parent
                            elif parent[1] == 'father':
                                pa = parent
                    continue
                if ma:
                    ma = [get_name_with_id(ma[0]), ma[0], ma[1]]
                    row[5][1].append(ma)
                if pa:
                    pa = [get_name_with_id(pa[0]), pa[0], pa[1]]
                    row[5][1].append(pa)

        for row in self.findings:
            widg = row[6][0]
            finding_id = row[9]
            widg.finding_id = finding_id
            if row[9] in non_empty_roles:
                widg.header = [row[0][1], row[1][1][0], row[2][1], row[3][1]]
                row[6][1] = ' ... '
            else:
                widg.header = [row[0][1], row[1][1][0], row[2][1], row[3][1]]

        for row in self.findings:
            widg = row[7][0]
            finding_id = row[9]
            widg.finding_id = finding_id
            if row[9] in non_empty_notes:
                widg.header = [row[0][1], row[1][1][0], row[2][1], row[3][1]]
                row[7][1] = ' ... '
            else:
                widg.header = [row[0][1], row[1][1][0], row[2][1], row[3][1]]

        for row in self.findings:
            for src in source_count:
                if row[9] == src[0]:
                    row[8][1] = src

        # sort by date
        for row in self.findings:
            event_type = row[0][1]
            if event_type == 'birth':
                row[1][1][1] = '-10000,0,0'
            elif event_type == 'death':
                row[1][1][1] = '10000,0,0'
            elif event_type == 'burial':
                row[1][1][1] = '10001,0,0'

        for row in self.findings:
            sorter = row[1][1][1]
            sorter = sorter.split(',')
            sorter = [int(i) for i in sorter]
            row[1][1][1] = sorter
           
        self.findings = sorted(self.findings, key=lambda i: i[1][1][1])

        self.show_table_cells()

    def show_table_cells(self):

        def open_kin_tip(evt, kin):

            def make_kin_tip(lst):
                self.instrux = KinTip(
                    self.kin_tip, 
                    text="{} (id #{})".format(lst[0], lst[1]))
                self.instrux.grid(sticky="news")
                self.instrux.instrux2.bind('<Button-1>', self.go_to)
    
            def highlight(event):
                event.widget.config(bg=formats["head_bg"])

            def unhighlight(event):
                event.widget.config(bg=formats["bg"])

            if evt.widget.winfo_rooty() < 96:
                y_offset = 32
            else:
                y_offset = -84

            self.kin_tip = Toplevel(self)
            x, y, cx, cy = evt.widget.bbox("insert")
            x = x + evt.widget.winfo_rootx() + y_offset
            y = y + cy + evt.widget.winfo_rooty() + y_offset
            self.kin_tip.wm_geometry('+{}+{}'.format(x, y))
            self.kin_tip.wm_overrideredirect(1)
            self.kintips.append(self.kin_tip)

            # spouse or child
            if len(kin) == 3:
                make_kin_tip(kin)
            # parents
            else:
                for lst in kin:
                    make_kin_tip(lst)

            ex = LabelButtonText(
                self.instrux, 
                text="x", 
                width=2,
                font=("arial black", 3))
            ex.place(rely=1.0, relx=1.0, x=0, y=0, anchor='se')
            ex.bind('<Button-1>', self.destroy_kintip)
            ex.bind('<Control-Button-1>', self.destroy_all_kintips)
            ex.bind('<Enter>', highlight)
            ex.bind('<Leave>', unhighlight)

        r = 2
        for row in self.findings:
            event_type = row[0][1]
            c = 0
            for col in row[0:9]:
                widg = col[0]
                if c == 1:
                    text = col[1][0]
                elif c in (0, 2, 3, 4):
                    text = col[1]
                elif c == 5: # kin
                    ma_pa = False
                    if event_type == 'birth':
                        ma_pa = True
                        self.kin_buttons = []                    
                    if len(col[1]) == 0:
                        text = ""
                    else:
                        kin = col[1]
                        if kin:
                            if ma_pa is False:
                                text = kin[2]
                            else:
                                text = 'parents'
                        kinlab = LabelButtonText(
                            row[c][0],
                            text=text,
                            anchor='w',
                            font=formats['heading3'])
                        kinlab.grid(column=0, row=0)
                        kinlab.bind(
                            '<Button-1>', 
                            lambda evt, kin=kin: open_kin_tip(evt, kin))
                        self.kin_buttons.append(kinlab)

                elif c == 6: # roles
                    widg.config(text=col[1])
                elif c == 7: # notes
                    widg.config(text=col[1])
                elif c == 8: # sources
                    widg.config(text=row[8][1][1], width=8)
                if c in (6, 7, 8):
                    widg.grid(column=c, row=r, sticky='w', pady=(3,0), padx=(2,0))
                else:
                    widg.grid(column=c, row=r, sticky='ew', pady=(3,0))
                if c < 5:
                    widg.insert(0, text)
                    self.widths[c].append(len(text))
                c += 1
            r += 1

        self.fix_tab_traversal()
        for row_num in range(self.grid_size()[1]):
            self.grid_rowconfigure(row_num, weight=0)
        self.row_qty = row_num
        
        self.size_columns_to_content()

    def destroy_kintip(self, evt=None):
        if evt:
            tip = evt.widget.master.master
            idx = self.kintips.index(tip)
            del self.kintips[idx]
            tip.destroy()
        for widg in self.kintips:
            widg.lift()

    def destroy_all_kintips(self, evt=None):
        for widg in self.kintips:
            widg.destroy()
        self.kintips = []

    def go_to(self, evt):

        text = evt.widget.cget("text")
        person_id = text.split("#")[1]
        self.instrux.person_id = int(person_id.rstrip(")"))
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(update_current_person, (self.instrux.person_id,))
        conn.commit()
        cur.close()
        conn.close()
        self.forget_cells()
        self.set_cell_content()

    def forget_cells(self):
        self.update_idletasks()
        for lst in self.cell_pool:
            for widg in lst[1]:
                if widg.winfo_subclass() == 'EntryAuto':
                    widg.delete(0, 'end')
                elif widg.winfo_subclass() == 'Frame':
                    self.destroy_all_kintips()
                    for button in self.kin_buttons:
                        button.destroy()
                elif widg.winfo_subclass() == 'LabelButtonText':
                    widg.config(text='')
                widg.grid_forget()

    def make_header(self):
        
        y = 0
        for heading in FINDING_TABLE_HEADS:
            head = LabelH3(self, text=heading, anchor='w')
            head.grid(column=y, row=0, sticky='ew')
            if y in (6, 7, 8):
                head.grid(column=y, row=0, sticky='ew')
            else:
                head.grid(column=y, row=0, sticky='ew')
            if y < 5:
                self.headers.append(head)
            y += 1

        sep = Separator(self, height=3)
        sep.grid(column=0, row=1, columnspan=9, sticky='ew')

    def make_new_event_row(self):
        pass

    def fix_tab_traversal(self):

        def third_and_second_items(pos):
            return pos[2], pos[1]

        row_fixer = []
        for lst in self.cell_pool:
            for child in lst[1]:           
                row_fixer.append((
                    child, 
                    child.grid_info()['column'], 
                    child.grid_info()['row']))
        row_fixer_2 = sorted(row_fixer, key=third_and_second_items) 

        widgets = []
        for tup in row_fixer_2:
            widgets.append(tup[0])

        for widg in widgets:
            widg.lift() 

short_values = ['red', 'white', 'blue', 'black', 'rust', 'pink', 'steelblue']

def highlight_current_title_bar(): # DON'T DELETE
    # MOVED HERE FROM window_border.py... I think currently the title bars
    #    are the right color except for the root when another dialog is in focus,
    #    anyway check it and make it right
    # for k,v in perm_dialogs.items():
        # border = v['canvas']
        # for widg in (
                # border.title_bar, border.title_frame, border.logo, 
                # border.title_1, border.title_1b, border.title_2, 
                # border.txt_frm, border.buttonbox, border.border_top, 
                # border.border_left, border.border_right, 
                # border.border_bottom):
            # widg.config(bg=NEUTRAL_COLOR)
    pass

if __name__ == '__main__':

    root = tk.Tk()
    root.geometry('+800+300')

    auto = EntryAuto(root, width=50, autofill=True)
    strings = make_all_nestings(select_all_place_ids)

    EntryAuto.create_lists(strings)
    auto.focus_set()   

    move = tk.Entry(root)

    auto.grid()
    move.grid()

    root.mainloop()


# DO LIST

# BRANCH: events_table
# # NEW EVENT ROW: Have to make one permanent edit row and ungrid it on close, this is because I learned last time since there is only ever one of them it's better to grid_remove instead of destroy it.

# BRANCH: dates
# finish refactoring dates validation

# BRANCH: front_page
# replace ttk.Notebooks
# add menubar, ribbon menu, footer
# add picture and attrib table
# add buttons to place tab for alias and edit/delete place but don't make them do anything

# BRANCH: fonts
# make fonts tab on prefs tabbook
# replace all comboboxes and all other ttk widgets

# BRANCH: sources
# IDEA for copy/pasting citations. This is still tedious and uncertain bec you never know what's in a clipboard, really. Since the assertions are shown in a table, have a thing like the fill/drag icon that comes up on a spreadsheet when you point to the SE corner of a cell. The icon turns into a different icon, maybe a C for Copy, and if you click down and drag at that point, the contents of the citation are pasted till you stop dragging. Should also work without the mouse, using arrow keys. If this idea isn't practical, it still leads to the notion of a tabular display of citations which would make copy & paste very easy instead of showing citations a click apart from each other, and seeing them all together might be useful for the sake of comparison?









