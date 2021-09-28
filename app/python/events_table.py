# events_table

# previous version x7 canned because modifying the code is too hard due to the use of lists throughout the process of building a table from queried data results. I had once done this with dicts but changed to lists since the table columns are in a fixed order and the list can be in the same order, so making the table is faster from a list. But it's more important to make the code accessible so I'm going back to dictionaries which will make the code easier to read and understand. 

# During the process of building a table, the data has to be manipulated and trying to keep everything in the right order throughout this process is hard, especially when coming back to change something down the road since the index gives no clue as to what data can be found where until the list if finished and ready to be used to display a table. Instead the table will be made from a list of dicts which can be sorted as a list while the values of the table cells can be stored in a dict for each table row. If it helps, the final list of dicts can be converted to a list of lists but only if it makes the table display faster.

import tkinter as tk
import sqlite3
from files import current_file
from window_border import Border 
from widgets import (
    Frame, LabelDots, LabelButtonText, Toplevel, Label, Radiobutton,
    KinTip, LabelH3, Button, Entry, MessageHilited, EntryHilited1,
    LabelHilited)
from custom_combobox_widget import Combobox 
from autofill import EntryAuto, EntryAutoHilited
from nested_place_strings import make_all_nestings
from toykinter_widgets import Separator
from styles import make_formats_dict, config_generic
from names import (
    get_name_with_id, make_values_list_for_person_select, PersonAdd)
from roles import RolesDialog
from notes import NotesDialog
from places import place_strings, ValidatePlace, places_places
from scrolling import Scrollbar, resize_scrolled_content
from messages import open_error_message, events_msg, open_yes_no_message
from query_strings import (
    select_finding_places_nesting, select_current_person_id, 
    select_all_event_types_couple, select_all_kin_type_ids_couple,
    select_all_findings_current_person, select_findings_details_generic,
    select_findings_details_couple, select_findings_details_couple_generic,
    select_finding_id_birth, select_person_id_kin_types_birth,
    select_finding_ids_age_parents, select_person_id_birth,
    select_findings_details_offspring, select_all_findings_roles_ids_distinct, 
    select_finding_ids_offspring, select_all_findings_notes_ids,
    select_count_finding_id_sources, select_nesting_fk_finding,
    select_nestings_and_ids, select_place, update_finding_particulars,
    update_finding_age, update_current_person, select_all_place_ids,
    select_all_event_types, select_event_type_id, insert_finding_new,
    insert_finding_new_couple, insert_findings_persons_new_couple,
    select_all_kin_ids_types_couple, select_all_names_ids,
    select_kin_type_string, update_findings_persons_couple_age,
    select_event_type_couple_bool, insert_kin_type_new, update_event_types,
    update_kin_type_kin_code, select_max_finding_id, insert_place_new,
    insert_places_places_new, insert_finding_places_new_event,
    insert_event_type_new, select_max_event_type_id, delete_finding,delete_claims_findings, delete_finding_places,
    delete_findings_roles_finding, delete_findings_notes_finding, 
    delete_claims_findings, delete_findings_persons,    
    select_findings_for_person, insert_finding_places_new,
    select_event_type_after_death, select_event_type_after_death_bool,
    select_kin_types_finding, update_findings_persons_1_2,  
    select_findings_persons_parents, update_findings_persons_couple_old,
    update_findings_persons_2, update_findings_persons_1,   
    update_findings_persons_couple_new, update_finding_places_null,
    update_finding_places, select_findings_persons_age,
    update_findings_persons_mother, update_findings_persons_father,
    insert_finding_birth, update_findings_persons_parent_age,
    select_finding_event_type, delete_findings_persons_offspring,
    select_findings_roles_generic_finding, 

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

def update_particulars(input_string, finding):
    conn = sqlite3.connect(current_file)
    conn.execute('PRAGMA foreign_keys = 1')
    cur = conn.cursor()
    cur.execute(
        update_finding_particulars, 
        (input_string, finding))
    conn.commit()
    cur.close()
    conn.close()

def get_all_event_types():
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_all_event_types)
    event_types = [i[0] for i in cur.fetchall()]
    cur.close()
    conn.close()
    return event_types

def get_after_death_event_types():
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_event_type_after_death)
    after_death_event_types = [i[0] for i in cur.fetchall()]
    cur.close()
    conn.close()
    return after_death_event_types 

def get_couple_kin_types():
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()
    cur.execute(select_all_kin_type_ids_couple)
    couple_kin_type_ids = [i[0] for i in cur.fetchall()]
    cur.close()
    conn.close()
    return couple_kin_type_ids

def get_place_string(finding_id, cur):
    cur.execute(select_finding_places_nesting, finding_id)
    place = cur.fetchone()
    place_string = ", ".join([i for i in place if i])
    if place_string == "unknown": place_string = ""
    return place_string

def make_sorter(date):
    sorter = date.split(",")
    date = [int(i) for i in sorter]
    return date

def get_generic_findings(
        dkt, cur, finding_id, findings_data, 
        current_person, non_empty_roles, non_empty_notes):
    cur.execute(select_findings_details_generic, finding_id)
    generic_details = [i for i in cur.fetchone()] 
    sorter = make_sorter(generic_details[4])
    dkt["event"], dkt["particulars"], dkt["age"] = generic_details[0:3]
    dkt["date"] = [generic_details[3], sorter]
    place = get_place_string(finding_id, cur)
    dkt["place"] = place

    if finding_id[0] in non_empty_roles:
        get_role_findings(dkt, finding_id[0], cur, current_person)

    if finding_id[0] in non_empty_notes:
        get_note_findings(dkt, finding_id[0], cur, current_person)

    cur.execute(select_count_finding_id_sources, finding_id)
    source_count = cur.fetchone()[0]
    dkt["source_count"] = source_count

    findings_data[finding_id[0]] = dkt

def get_couple_findings(
        cur, current_person, rowtotype, findings_data, 
        non_empty_roles, non_empty_notes):

    couple_kin_type_ids = get_couple_kin_types()
    curr_per_kin_types = tuple([current_person] + couple_kin_type_ids)
    sql =   '''
                SELECT finding_id 
                FROM findings_persons 
                WHERE person_id1 = ?
                    AND kin_type_id1 in ({})
            '''.format(
                ','.join('?' * (len(curr_per_kin_types) - 1)))
    cur.execute(sql, curr_per_kin_types)
    couple_findings1 = [i[0] for i in cur.fetchall()]
    sql =   '''
                SELECT finding_id 
                FROM findings_persons 
                WHERE person_id2 = ?
                    AND kin_type_id2 in ({})
            '''.format(
                ','.join('?' * (len(curr_per_kin_types) - 1)))
    cur.execute(sql, curr_per_kin_types)
    couple_findings2 = [i[0] for i in cur.fetchall()]
    couple_findings = couple_findings1 + couple_findings2
    for finding_id in couple_findings:
        finding_id = (finding_id,)
        dkt = dict(rowtotype)
        cur.execute(select_findings_details_couple, finding_id)
        gotgot = cur.fetchone()
        if gotgot:
            if gotgot[0] == current_person:
                dkt["age"] = gotgot[1]
                dkt["kin_type"] = gotgot[2]
                dkt["partner_id"] = gotgot[3]
                dkt["partner_kin_type"] = gotgot[5]
                dkt["partner_name"] = get_name_with_id(gotgot[3])
            elif gotgot[3] == current_person:
                dkt["age"] = gotgot[4]
                dkt["kin_type"] = gotgot[5]
                dkt["partner_id"] = gotgot[0]
                dkt["partner_kin_type"] = gotgot[2]
                dkt["partner_name"] = get_name_with_id(gotgot[0])
      
        cur.execute(select_findings_details_couple_generic, finding_id)
        couple_generics = list(cur.fetchone())
        place = get_place_string(finding_id, cur)
        dkt["place"] = place
        sorter = make_sorter(couple_generics[2])
        couple_generic_details = [
            couple_generics[0], 
            [couple_generics[1], sorter], 
            couple_generics[3]]

        if finding_id[0] in non_empty_roles:
            get_role_findings(dkt, finding_id[0], cur, current_person)

        if finding_id[0] in non_empty_notes:
            get_note_findings(dkt, finding_id[0], cur, current_person)

        cur.execute(select_count_finding_id_sources, finding_id)
        source_count = cur.fetchone()[0]
        dkt["source_count"] = source_count

        dkt["event"], dkt["date"], dkt["particulars"] = couple_generic_details
        findings_data[finding_id[0]] = dkt

    return couple_findings

def get_birth_findings(
        dkt, cur, current_person, findings_data, non_empty_roles, non_empty_notes):
    # dkt["offspring"] = []
    cur.execute(select_finding_id_birth, (current_person,))
    birth_id = cur.fetchone()
    parents = (None, None)
    if birth_id:
        cur.execute(select_person_id_kin_types_birth, birth_id)
        parents = cur.fetchone()
    if not parents:
        pass
    elif parents[1] == "mother":
        dkt["mother_id"] = parents[0]
        dkt["mother_name"] = get_name_with_id(parents[0])
        dkt["father_id"] = parents[2]
        dkt["father_name"] = get_name_with_id(parents[2])
    elif parents[3] == "mother":
        dkt["father_id"] = parents[0]
        dkt["father_name"] = get_name_with_id(parents[0])
        dkt["mother_id"] = parents[2]
        dkt["mother_name"] = get_name_with_id(parents[2])

    cur.execute(select_finding_ids_age_parents, (current_person,))
    children = [list(i) for i in cur.fetchall()]
    for lst in children:
        offspring_event_id = lst[0]
        cur.execute(select_person_id_birth, (offspring_event_id,))
        offspring = cur.fetchone()
        if offspring:
            lst.append(offspring[0])

    for lst in children:
        offspring_event_id, parent_age, child_id = lst
        cur.execute(select_findings_details_offspring, (child_id,))       
        offspring_details = cur.fetchone()

        child_name = get_name_with_id(child_id)

        sorter = make_sorter(offspring_details[1])
        date = [offspring_details[0], sorter]
        particulars = offspring_details[2]
        place = get_place_string((offspring_event_id,), cur)

        cur.execute(select_count_finding_id_sources, (offspring_event_id,))
        source_count = cur.fetchone()[0]
        
        findings_data[offspring_event_id] = {}
        findings_data[offspring_event_id]["event"] = "offspring"
        findings_data[offspring_event_id]["date"] = date
        findings_data[offspring_event_id]["place"] = place
        findings_data[offspring_event_id]["particulars"] = particulars
        findings_data[offspring_event_id]["age"] = parent_age
        findings_data[offspring_event_id]["source_count"] = source_count
        findings_data[offspring_event_id]["child_id"] = child_id
        findings_data[offspring_event_id]["child_name"] = child_name

        if offspring_event_id in non_empty_roles:
            get_role_findings(
                dkt, offspring_event_id, cur, current_person, 
                findings_data=findings_data)

        if offspring_event_id in non_empty_notes:
            get_note_findings(
                dkt, offspring_event_id, cur, current_person, 
                findings_data=findings_data)

def get_role_findings(
    dkt, finding_id, cur, current_person, findings_data=None):
    # dkt, finding_id, cur, current_person, offspring=False, findings_data=None):
    current_roles = []
    current_roles.append(finding_id)
    # if offspring is False:
    if findings_data is None:
        dkt["roles"] = current_roles
    else: 
        findings_data[finding_id]["roles"] = current_roles

def get_note_findings(
    dkt, finding_id, cur, current_person, findings_data=None):
    # dkt, finding_id, cur, current_person, offspring=False, findings_data=None):
    current_notes = []
    current_notes.append(finding_id)
    # if offspring is False:
    if findings_data is None:
        dkt["notes"] = current_notes
    else:
        findings_data[finding_id]["notes"] = current_notes

def get_findings():
    
    findings_data = {}
    current_person = get_current_person()
    conn = sqlite3.connect(current_file)
    cur = conn.cursor()

    rowtotype = {
        "event": "", "date": "", "place": "", "particulars": "", "age": ""}

    cur.execute(select_all_findings_current_person, (current_person,))
    generic_finding_ids = cur.fetchall()

    cur.execute(select_all_findings_roles_ids_distinct)
    non_empty_roles = [i[0] for i in cur.fetchall()]

    cur.execute(select_all_findings_notes_ids)
    non_empty_notes = [i[0] for i in cur.fetchall()]

    for finding_id in generic_finding_ids:
        dkt = dict(rowtotype)
        get_generic_findings(
            dkt, cur, finding_id, findings_data, 
            current_person, non_empty_roles, non_empty_notes)
        if dkt["event"] == "birth":
            get_birth_findings(
                dkt, cur, current_person, findings_data,
                non_empty_roles, non_empty_notes)

    couple_finding_ids = get_couple_findings(
        cur, current_person, rowtotype, findings_data, 
        non_empty_roles, non_empty_notes)

    cur.close()
    conn.close()  

    return findings_data

class EventsTable(Frame):
    def __init__(self, master, root, treebard, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.root = root
        self.treebard = treebard

        self.current_person = get_current_person()

        self.inwidg = None
        self.headers = []
        self.widths = [[], [], [], [], []]
        self.kintips = []
        self.kin_buttons = []

        self.screen_height = self.winfo_screenheight()
        self.column_width_indecrement = 0
        self.new_row = 0

        event_types = get_all_event_types()
        self.event_autofill_values = EntryAuto.create_lists(event_types)

        self.root.bind(
            "<Control-S>", 
            lambda evt, curr_per=self.current_person: self.go_to(
                evt, current_person=curr_per))
        self.root.bind(
            "<Control-s>", 
            lambda evt, curr_per=self.current_person: self.go_to(
                evt, current_person=curr_per))

        self.make_header()
        self.make_table_cells()

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
            # so an empty table can open if the current person is null
            if len(lst) > 0:
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

    def delete_event(self, finding_id, widg, initial):

        def ok_delete_event():
            msg[0].destroy()
            self.focus_set()
            proceed(initial_value)

        def cancel_delete_event():
            msg[0].destroy()
            widg.insert(0, initial)
            widg.focus_set()

        def proceed(initial_value):

            def delete_generic_finding():
                cur.execute(delete_finding_places, (finding_id,))
                conn.commit()
                cur.execute(delete_findings_roles_finding, (finding_id,))
                conn.commit()
                cur.execute(delete_findings_notes_finding, (finding_id,))
                conn.commit()
                cur.execute(delete_claims_findings, (finding_id,))
                conn.commit()
                cur.execute(delete_finding, (finding_id,))
                conn.commit()

            def delete_couple_finding():
                cur.execute(delete_findings_persons, (finding_id,))
                conn.commit()
                delete_generic_finding()

            def delete_offspring_finding():
                cur.execute(select_findings_persons_parents, (finding_id,))
                parents = cur.fetchone()
                for person in parents:
                    cur.execute(delete_findings_persons_offspring, 
                        (finding_id, person))
                conn.commit()       
                delete_generic_finding()

            current_person = self.current_person
            conn = sqlite3.connect(current_file)
            conn.execute('PRAGMA foreign_keys = 1')
            cur = conn.cursor()
            cur.execute(select_event_type_id, (initial_value,))
            result = cur.fetchone()
            if result:
                old_event_type_id, couple_event_old = result 
            if couple_event_old == 0:
                cur.execute(select_finding_event_type, (finding_id,))
                event_type = cur.fetchone()[0]
                if event_type == 1:
                    delete_offspring_finding()
                else:
                    delete_generic_finding()
            elif couple_event_old == 1:
                delete_couple_finding()
            self.go_to(current_person=current_person)
            cur.close()
            conn.close()

        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()

        msg = open_yes_no_message(
            self, 
            events_msg[5], 
            "Delete Event Confirmation", 
            "OK", "CANCEL")
        msg[0].grab_set()
        msg[1].config(aspect=400)
        msg[2].config(command=ok_delete_event)
        msg[3].config(command=cancel_delete_event)

        initial_value = self.initial
        cur.close()
        conn.close()

    def update_db(self, widg, col_num):

        def update_event_type():

            def err_done4():
                msg[0].destroy()
                self.focus_set()
                widg.delete(0, 'end')
                widg.insert(0, 'offspring')

            def make_new_event_type():
                cur.execute(select_event_type_couple_bool, (self.initial,))
                couple = cur.fetchone()[0]

                cur.execute(
                    select_event_type_after_death_bool, (self.initial,))
                after_death = cur.fetchone()[0] 
                cur.execute(
                    insert_event_type_new, (
                        None, 
                        self.final, couple, after_death))
                conn.commit() 

                event_types = get_all_event_types()
                self.event_autofill_values = EntryAuto.create_lists(event_types)
                self.event_input.values = self.event_autofill_values

            def update_to_existing_type():

                def err_done5():
                    msg4[0].destroy()
                    self.focus_set()
                    widg.delete(0, 'end')
                    widg.insert(0, initial_value)

                initial_value = self.initial
                cur.execute(select_event_type_id, (initial_value,))
                result = cur.fetchone()
                if result:
                    old_event_type_id, couple_event_old = result 
                event_type_id = None
                couple_event_new = None
                cur.execute(select_event_type_id, (self.final,))
                result = cur.fetchone()
                if result:
                    event_type_id, couple_event_new = result 
                if couple_event_old != couple_event_new:
                    msg4 = open_error_message(
                        self, 
                        events_msg[4], 
                        "Incompatible Event Type Error", 
                        "OK")
                    msg4[0].grab_set()
                    msg4[1].config(aspect=400)
                    msg4[2].config(command=err_done5)
                    return

                if couple_event_new in (0, 1):
                    cur.execute(update_event_types, (event_type_id, self.finding))
                    conn.commit() 
                else:
                    print("line", looky(seeline()).lineno, "case not handled:")

            event_types = get_all_event_types()
            self.final = self.final.strip().lower()
            if ((self.initial == 'offspring' or self.final == 'offspring') and
                    len(self.final) != 0):
                msg = open_error_message(
                    self, 
                    events_msg[3], 
                    "Offspring Event Edit Error", 
                    "OK")
                msg[0].grab_set()
                msg[1].config(aspect=400)
                msg[2].config(command=err_done4)
                
            if self.final in event_types:
                update_to_existing_type()
            elif len(self.final) == 0:
                initial = self.initial
                self.delete_event(self.finding, widg, initial)
            else:
                make_new_event_type()
                update_to_existing_type()

        def update_place():
            cur.execute(select_nesting_fk_finding, (self.finding,))
            nested_place = cur.fetchone()[0]
            self.final = ValidatePlace(
                self.root, 
                self.treebard,
                self.inwidg,
                self.initial,
                self.final,
                self.finding)

        def update_age(offspring_event, row):
            if row[0][1] == "birth" and self.final not in (0, "0", "0d 0m 0y"):
                return
            if couple is False and offspring_event is False:
                cur.execute(update_finding_age, (self.final, self.finding))
                conn.commit() 
            elif offspring_event is True:
                cur.execute(
                    update_findings_persons_parent_age, 
                    (self.final, self.finding, self.current_person))
                conn.commit()
            else:
                cur.execute(
                update_findings_persons_couple_age, 
                (self.final, self.finding, self.current_person))
                conn.commit()

        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()

        if col_num == 0:
            update_event_type()
        elif col_num == 1:
            pass
        elif col_num == 2:
            update_place()
        elif col_num == 3:
            update_particulars(self.final, self.finding)
        elif col_num == 4:
            couple = False
            offspring_event = False
            for row in self.findings:
                if row[9] == self.finding: 
                    event_string = row[0][1]
                    cur.execute(select_event_type_couple_bool, (event_string,))
                    couple_or_not = cur.fetchone()[0]
                    if couple_or_not == 1:
                        couple = True
                    else: couple = False
                    if event_string == "offspring":
                        offspring_event = True
                        row = row
                    break
            update_age(offspring_event, row)            

        cur.close()
        conn.close()

    def make_table_cells(self, qty=1998):
        '''
            EntryAuto was used for all the text columns to keep the code 
            symmetrical for all the text columns, with autofill defaulting to 
            False except for the places column.
        '''
        self.place_autofill_values = EntryAuto.create_lists(place_strings)
        self.table_cells = []
        for i in range(int(qty/9)): # 222
            row = []
            for j in range(9):
                if j < 5:
                    if j == 0:
                        cell = EntryAuto(
                            self, 
                            autofill=True, 
                            values=self.event_autofill_values)
                    elif j == 2:
                        cell = EntryAuto(
                            self, 
                            autofill=True, 
                            values=self.place_autofill_values)
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
        self.event_input = EntryAutoHilited(
            self, 
            width=32, 
            autofill=True, 
            values=self.event_autofill_values)
        self.add_event_button = Button(
            self, text="NEW EVENT", command=self.make_new_event)
        self.set_cell_content()

    def set_cell_content(self):

        self.findings_data = get_findings()
        print("line", looky(seeline()).lineno, "self.findings_data:", self.findings_data)
        finding_ids = list(self.findings_data.keys())
        # print("line", looky(seeline()).lineno, "finding_ids:", finding_ids)
        table_size = len(self.findings_data)
        # for k,v in self.findings_data.items():
            # if v["event"] == "birth" and v["offspring"]:
                # for dickt in v["offspring"]:
                    # finding_ids.append(list(dickt.keys())[0])
                # table_size += len(v['offspring'])
                # break
        print("line", looky(seeline()).lineno, "finding_ids:", finding_ids)

        self.cell_pool = []

        i = 0
        for row in self.table_cells[0:table_size]:
            self.cell_pool.append([finding_ids[i], row])
            i += 1
            
        self.show_table_cells()

        return # GET RID OF THIS LINE************************************************

        generic_findings = findings_data[0]
        couple_findings = findings_data[1]
        parents = findings_data[2]
        children = findings_data[3]
        finding_ids = findings_data[4]
        current_roles = findings_data[5]
        non_empty_notes = findings_data[6]
        source_count = findings_data[7]

        self.cell_pool = []

        i = 0
        for row in self.table_cells[0:len(finding_ids)]:
            self.cell_pool.append([finding_ids[i], row])
            i += 1

# **********************************************************************************
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


        print("line", looky(seeline()).lineno, "self.findings:", self.findings)
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
            if row[9] in current_roles:
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
        after_death_events = get_after_death_event_types()
        after_death = []
        a_d = 0
        for row in self.findings:
            event_type = row[0][1]
            if event_type == 'birth':
                row[1][1][1] = '-10000,0,0'
            elif event_type == 'death':
                row[1][1][1] = '10000,0,0'
            elif event_type in after_death_events:
                after_death.append([row[9], row[1][1][1]])

        t = 0
        for event in after_death:
            sorter = event[1].split(',')
            sorter = [int(i) for i in sorter]
            event = sorter
            after_death[t][1] = event
            t += 1   

        after_death = sorted(after_death, key=lambda i: i[1])
        d = 0
        for event in after_death:
            for row in self.findings:
                if event[0] == row[9]:
                    after_death[d][1] = [20000 + d, 0, 0]
                    break
            d += 1

        for event in after_death:
            n = 0
            for num in event[1]:
                num = str(num)
                event[1][n] = num
                n += 1
        
        for event in after_death:
            event[1] = ",".join(event[1])

        for event in after_death:
            for row in self.findings:
                if event[0] == row[9]:
                    row[1][1][1] = event[1]
                    break

        for row in self.findings:
            sorter = row[1][1][1]
            sorter = sorter.split(',')
            sorter = [int(i) for i in sorter]
            row[1][1][1] = sorter
           
        self.findings = sorted(self.findings, key=lambda i: i[1][1][1])

        self.show_table_cells()

    def show_table_cells(self):
        r = 2
        for row in self.cell_pool:
            finding_id = row[0]
            print("line", looky(seeline()).lineno, "row:", row)
            c = 0
            for col in row[1][0:9]:
                if c == 0:
                    text = self.findings_data[finding_id]["event"]
                    print("line", looky(seeline()).lineno, "text:", text)

    def show_table_cellsx(self):
        r = 2
        for row in self.findings:
            event_type = row[0][1]
            c = 0
            for col in row[0:9]:
                cellval = col[1]
                widg = col[0]
                if c == 1:
                    text = cellval[0]
                elif c in (0, 2, 3, 4):
                    text = cellval
                elif c == 5: # kin
                    kinframe = row[c][0]
                    finding = row[9]
                    self.make_kin_button(
                        event_type, cellval, kinframe, row)
                elif c == 6: # roles
                    widg.config(text=col[1])
                elif c == 7: # notes
                    widg.config(text=col[1])
                elif c == 8: # sources
                    widg.config(text=row[8][1][1], width=8)
                if c in (6, 7, 8):
                    widg.grid(
                        column=c, row=r, sticky='w', pady=(3,0), padx=(2,0))
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
        self.new_row = row_num + 1
        
        self.size_columns_to_content()

        self.event_input.grid(
            column=0, 
            row=self.new_row,
            pady=6, columnspan=2, 
            sticky='w')
        self.add_event_button.grid(
            column=2, 
            row=self.new_row, 
            pady=6, sticky='w')

    def make_kin_button(self, event_type, cellval, kinframe, finding):
        couple_kin_type_ids = get_couple_kin_types()# not being used?
        ma_pa = False
        if event_type == 'birth':
            ma_pa = True
        if len(cellval) == 0:
            text = ""
        else:
            kin = cellval
            kin.append(finding)
            self.kinless = "Click to edit event details. Right-click to edit kin type."
            if kin:
                if ma_pa is False:
                    text = kin[2]
                else:
                    text = 'parents'
            if kin[1] is None:             
                kin[1] = self.kinless
            elif ma_pa is True:
                parentlist = list(kin[0:2])                
                
                for lst in parentlist:
                    if lst[1] is None:
                        lst[1] = self.kinless
                kin[0:2] = parentlist
            
            kinlab = LabelButtonText(
                kinframe,
                text=text,
                anchor='w',
                font=formats['heading3'])
            kinlab.grid(column=0, row=0)
            kinlab.bind(
                '<Button-1>', 
                lambda evt, kin=kin, ma_pa=ma_pa: self.open_kin_tip(
                    evt, kin, ma_pa))
            self.kin_buttons.append(kinlab)
            kinframe.grid()

    def open_kin_tip(self, evt, kin, ma_pa):

        def make_kin_tip(lst):
            if lst[1] == self.kinless:
                self.instrux = KinTip(
                    self.kin_tip, 
                    text=lst[1],
                    empty=True)
                self.instrux.grid(sticky="news")
                self.instrux.instrux2.bind('<Button-1>', self.go_to)
                if ma_pa is False:
                    self.instrux.finding = kin[3]
                else:
                    self.instrux.finding = kin[2]
            else:
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
        if len(kin) == 4:
            make_kin_tip(kin)
        # parents
        else:
            for lst in kin[0:2]:
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

    def add_kin(self, ma_pa):
        event_type = self.instrux.finding[0][1]
        self.edit_event_dialog = NewEventDialog(
            self.root, 
            self.treebard,
            self,
            event_type,
            self.current_person,
            self.place_autofill_values,   
            self.go_to,
            finding=self.instrux.finding,
            ma_pa=ma_pa)         

    def go_to(self, evt=None, current_person=None):
        if evt and evt.type == "4": 
            text = evt.widget.cget("text")
            if text == self.kinless:
                if self.instrux.finding[0][1] == "birth":
                    ma_pa = True
                self.add_kin(ma_pa)
                return
            else:
                person_id = text.split("#")[1]
                id_string = person_id.rstrip(")")
                self.instrux.person_id = int(id_string)
                self.current_person = self.instrux.person_id
        else:
            self.current_person = current_person
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(update_current_person, (self.current_person,))
        conn.commit()
        cur.close()
        conn.close()
        self.forget_cells()
        self.new_row = 0 
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
        self.event_input.grid_forget()
        self.add_event_button.grid_forget()

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

    def count_birth_death_events(self, new_event):
        too_many = False
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        cur.execute(select_findings_for_person, (self.current_person,))
        all_events = [i[0] for i in cur.fetchall()]
        if new_event in all_events:
            too_many = True
        cur.close()
        conn.close()
        return too_many

    def make_new_event(self):
        '''
            Disallow creation of second birth or death event, and
            otherwise proceed.
        '''

        def err_done6():
            self.event_input.delete(0, 'end')
            msg[0].destroy()
            self.focus_set()

        too_many = False
        new_event = self.event_input.get().strip().lower()
        if new_event in ("birth", "death"):
            too_many = self.count_birth_death_events(new_event)
        if too_many is True: 
            msg = open_error_message(
                self, 
                events_msg[6], 
                "Multiple Birth or Death Events", 
                "OK")
            msg[0].grab_set()
            msg[1].config(aspect=400)
            msg[2].config(command=err_done6)
            return
        self.new_event_dialog = NewEventDialog(
            self.root, 
            self.treebard,
            self,
            new_event,
            self.current_person,
            self.place_autofill_values,   
            self.go_to)
        self.event_input.delete(0, 'end')

class NewEventDialog(Toplevel):
    def __init__(
            self, master, treebard, events_table,
            new_event, 
            current_person, place_autofill_values, 
            go_to, finding=None, ma_pa=False, *args, **kwargs):
        Toplevel.__init__(self, master, *args, **kwargs)

        self.root = master
        self.treebard = treebard
        self.events_table = events_table
        self.new_event = new_event
        self.current_person = current_person
        self.place_autofill_values = place_autofill_values
        self.go_to = go_to
        self.finding = finding
        self.ma_pa = ma_pa
        if self.finding:
            self.edit_event = True
        else:
            self.edit_event = False

        self.place_dicts = None
        self.new_event_type = False
        self.never_mind = False

        self.new_kin_type_codes = [None, None]

        self.current_name = get_name_with_id(self.current_person)
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()

        people = make_values_list_for_person_select()        
        self.all_birth_names = EntryAuto.create_lists(people)

        cur.execute(select_all_kin_ids_types_couple)
        self.kintypes_and_ids = [i for i in cur.fetchall()]
        self.kintypes_and_ids = sorted(self.kintypes_and_ids, key=lambda i: i[1])
        self.kin_types = [i[1] for i in self.kintypes_and_ids]

        self.focus_new_event_dialog()
        self.get_some_info()
        if self.new_event_type is False:
            self.make_widgets()

        cur.close()
        conn.close()

    def get_some_info(self):
        conn =  sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(select_max_finding_id)
        self.new_finding = cur.fetchone()[0] + 1
        cur.execute(select_event_type_id, (self.new_event,))
        result = cur.fetchone()
        if result is not None:
            self.event_type_id, self.couple_event = result
        else:
            self.new_event_type = True
            cur.execute(select_max_event_type_id)
            self.event_type_id = cur.fetchone()[0] + 1            
            self.input_new_event_type()
        cur.close()
        conn.close()

    def ask_if_after_death(self):

        def ok_new_evt_type():
            conn = sqlite3.connect(current_file)
            conn.execute('PRAGMA foreign_keys = 1')
            cur = conn.cursor()
            evt_is_after_death = posthumousvar.get()
            cur.execute(insert_event_type_new, (
                self.event_type_id, 
                self.new_event, 
                self.couple_event, 
                evt_is_after_death))
            conn.commit()

            event_types = get_all_event_types()
            more_event_types = EntryAuto.create_lists(event_types)
            self.events_table.event_input.values = more_event_types

            self.asker.grab_release()
            self.asker.destroy()
            self.deiconify()
            self.focus_set() 
            self.lift()
            self.grab_set()
            cur.close()
            conn.close()

        def cancel_new_evt_type():
            nonlocal never_mind
            self.asker.grab_release()
            self.asker.destroy()
            never_mind = True

        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()

        never_mind = False

        text = ( 
            "Before-death event type: e.g. 'promotion', "
            "'business venture', 'graduation'.",
            "After-death event type: e.g. 'funeral', 'probate', "
            "'reading of the will', 'posthumous ______'.")
        posthumousvar = tk.IntVar(None, 0)
        self.asker = Toplevel(self)
        self.asker.title("Select Before- or After-Death Event Type")
        lab = LabelH3(
            self.asker, 
            text="Does the new event type occur after death?")
        
        for i in range(2):
            rad = Radiobutton(
                self.asker,  
                text=text[i],
                value=i,
                variable=posthumousvar,
                anchor='w')
            rad.grid(column=0, row=i+1)

        buttonframe = Frame(self.asker)
        butt1 = Button(
            buttonframe, text="OK", width=6, 
            command=ok_new_evt_type)
        butt2 = Button(
            buttonframe, text="CANCEL", width=6, 
            command=cancel_new_evt_type)

        lab.grid(column=0, row=0, pady=12)
        buttonframe.grid(column=0, row=3, sticky='e', pady=(0,12))
        butt1.grid(column=0, row=0, sticky='e', padx=12, pady=6)
        butt2.grid(column=1, row=0, sticky='e', padx=12, pady=6)
        self.asker.grab_set()
        butt1.focus_set()
        
        self.wait_window(self.asker)
        if never_mind is False:
            self.make_widgets()
        else:
            self.destroy()
        cur.close()
        conn.close()        

    def input_new_event_type(self):  

        def ask_next_question():
            self.couple_event = couplevar.get()
            id_couple_event.grab_release()
            id_couple_event.destroy()

        def input_evt_type_now():
            conn = sqlite3.connect(current_file)
            conn.execute('PRAGMA foreign_keys = 1')
            cur = conn.cursor()
            self.couple_event = couplevar.get()
            cur.execute(insert_event_type_new, (
                self.event_type_id, self.new_event, self.couple_event, 0))
            conn.commit()

            event_types = get_all_event_types()
            more_event_types = EntryAuto.create_lists(event_types)
            self.events_table.event_input.values = more_event_types

            cur.close()
            conn.close()

            self.make_widgets()
            self.deiconify()

        def cancel_new_evt_type():
            nonlocal never_mind
            id_couple_event.grab_release()
            id_couple_event.destroy()
            never_mind = True

        never_mind = False

        text = ( 
            "Generic event type: one primary participant or a parent, e.g. "
                "'birth', 'career', 'adopted a child'.",
            "Couple event type: two equal participants, e.g. 'marriage', "
                "'wedding', 'engagement'.")
        couplevar = tk.IntVar(None, 0)
        id_couple_event = Toplevel(self.root)
        id_couple_event.title("Select Couple or Generic Event Type")
        self.withdraw()
        id_couple_event.grab_set()

        lab = LabelH3(
            id_couple_event, 
            text="Is the new event type a couple event?")
        
        for i in range(2):
            rad = Radiobutton(
                id_couple_event,  
                text=text[i],
                value=i,
                variable=couplevar,
                anchor='w')
            rad.grid(column=0, row=i+1)

        buttonframe = Frame(id_couple_event)
        butt1 = Button(
            buttonframe, text="OK", width=6, 
            command=ask_next_question)
        butt2 = Button(
            buttonframe, text="CANCEL", width=6, 
            command=cancel_new_evt_type)

        lab.grid(column=0, row=0, pady=12)
        buttonframe.grid(column=0, row=3, sticky='e', pady=(0,12))
        butt1.grid(column=0, row=0, sticky='e', padx=12, pady=6)
        butt2.grid(column=1, row=0, sticky='e', padx=12, pady=6)
        butt1.focus_set()
        
        self.wait_window(id_couple_event)
        if never_mind is False:
            if self.couple_event == 0:
                self.ask_if_after_death()
            else:
                input_evt_type_now()
        else:
            self.destroy()

    def make_widgets(self):

        def show_message():
            window.columnconfigure(1, weight=1)
            window.rowconfigure(1, weight=1)
            self.new_evt_msg = MessageHilited(
                window, 
                justify='left', 
                aspect=1200)
            self.new_evt_msg.grid(column=1, row=1, sticky='news', ipady=18)

        self.columnconfigure(1, weight=1)
        self.rowconfigure(4, weight=1)
        canvas = Border(self, size=3) # don't hard-code size   
        if self.edit_event is True:
            canvas.title_1.config(text="Edit Event Dialog")
        else:
            canvas.title_1.config(text="New Event Dialog")
        canvas.title_2.config(text="Current Person: {}, id #{}".format(
            self.current_name, self.current_person))

        window = Frame(canvas)
        canvas.create_window(0, 0, anchor='nw', window=window)
        scridth = 16
        scridth_n = Frame(window, height=scridth)
        scridth_w = Frame(window, width=scridth)
        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')
        # DO NOT DELETE THESE LINES, UNCOMMENT IN REAL APP
        # self.treebard.scroll_mouse.append_to_list([canvas, window])
        # self.treebard.scroll_mouse.configure_mousewheel_scrolling()

        window.vsb = Scrollbar(
            self, 
            hideable=True, 
            command=canvas.yview,
            width=scridth)
        window.hsb = Scrollbar(
            self, 
            hideable=True, 
            width=scridth, 
            orient='horizontal',
            command=canvas.xview)
        canvas.config(
            xscrollcommand=window.hsb.set, 
            yscrollcommand=window.vsb.set)
        window.vsb.grid(column=2, row=4, sticky='ns')
        window.hsb.grid(column=1, row=5, sticky='ew')

        buttonbox = Frame(window)
        self.b1 = Button(buttonbox, text="OK", width=7)
        b2 = Button(buttonbox, text="CANCEL", width=7, command=self.cancel)

        scridth_n.grid(column=0, row=0, sticky='ew')
        scridth_w.grid(column=0, row=1, sticky='ns')
        window.columnconfigure(2, weight=1)
        window.rowconfigure(1, minsize=60)
        buttonbox.grid(column=1, row=3, sticky='se', pady=6)

        self.b1.grid(column=0, row=0)
        b2.grid(column=1, row=0, padx=(2,0))

        self.frm = Frame(window)
        self.frm.grid(column=1, row=2, sticky='news', pady=12)
        self.frm.columnconfigure(0, weight=1)
        show_message()
        self.make_inputs()

        resize_scrolled_content(self, canvas, window)

    def make_inputs(self):

        self.generic_data_inputs = Frame(self.frm)
        self.couple_data_inputs = Frame(self.frm)
        more = Label(
            self.frm, 
            text="Roles, Notes & Sources can be created and "
                "edited in the events table.")

        self.generic_data_inputs.grid(column=0, row=0, sticky="news")
        self.couple_data_inputs.grid(column=0, row=2, sticky='news')
        more.grid(column=0, row=4, columnspan=2, sticky="ew", pady=(12,0))
        
        self.lab0 = LabelH3(
            self.generic_data_inputs, text="Event Type: {}".format(
                self.new_event))
        lab1 = Label(self.generic_data_inputs, text="Date")
        self.date_input = EntryHilited1(self.generic_data_inputs)
        lab2 = Label(self.generic_data_inputs, text="Place")
        self.place_input = EntryAutoHilited(
            self.generic_data_inputs, 
            width=48, autofill=True, values=self.place_autofill_values)
        self.place_input.bind("<FocusOut>", self.validate_place)
        lab3 = Label(self.generic_data_inputs, text="Particulars")
        self.particulars_input = EntryHilited1(
            self.generic_data_inputs, width=60)

        self.lab0.grid(column=0, row=0, sticky="w", pady=6)
        lab1.grid(column=0, row=1, sticky="e", pady=(0,1))
        self.date_input.grid(column=1, row=1, sticky="w", padx=(3,0), pady=(0,1))
        lab2.grid(column=0, row=2, sticky="e", pady=(0,1))
        self.place_input.grid(
            column=1, row=2, sticky="w", padx=(3,0), pady=(0,1))
        lab3.grid(column=0, row=3, sticky="e")
        self.particulars_input.grid(column=1, row=3, sticky="w", padx=(3,0))
        if self.couple_event == 0:
            self.b1.config(command=self.add_event)
            if self.ma_pa is True:
                self.show_other_person()
            elif self.new_event == "offspring":
                self.show_other_person()            
            else:
                self.show_one_person()
            if self.edit_event is True:
                self.fill_in_for_editing()
        elif self.couple_event == 1:
            self.show_other_person()
            if self.edit_event is True:
                self.fill_in_for_editing(people=2)
                self.b1.config(command=self.validate_kin_types)
            else:
                self.b1.config(command=self.validate_kin_types)        

        self.date_input.focus_set()

    def fill_in_for_editing(self, people=1):
        conn = sqlite3.connect(current_file)
        cur = conn.cursor()
        self.finding_id = self.finding[9]
        self.date_input.insert(0, self.finding[1][1][0])
        self.place_input.insert(0, self.finding[2][1])
        self.particulars_input.insert(0, self.finding[3][1])
        if self.ma_pa is False:
            self.age1_input.insert(0, self.finding[4][1])
            if people == 1:
                cur.close() 
                conn.close()
                return
            cur.execute(select_kin_types_finding, (self.finding_id,))
            kin_types = [i[0] for i in cur.fetchall()]
            self.kin_type_input1.insert(0, kin_types[0])
            self.kin_type_input2.insert(0, kin_types[1])
        else:
            ma_id = self.finding[5][1][0][1]
            ma_name = self.finding[5][1][0][0]
            cur.execute(
                select_findings_persons_age, 
                (ma_id, self.finding_id))
            result = cur.fetchone()
            if result:
                age_ma = result[0]
            else:
                age_ma = ''
            self.parent1_input.insert(0, '{}  #{}'.format(ma_name, ma_id))
            self.age1_input.insert(0, age_ma)

            pa_id = self.finding[5][1][1][1]
            pa_name = self.finding[5][1][1][0]
            cur.execute(
                select_findings_persons_age, 
                (pa_id, self.finding_id))
            result = cur.fetchone()
            if result:
                age_pa = result[0]
            else:
                age_pa = ''
            self.other_person_input.insert(0, pa_name)
            self.age2_input.insert(0, age_pa)
            # Also used if ma_pa is True since kin_type is fixed.
            if people == 1:
                cur.close() 
                conn.close()
                self.other_person_input.focus_set()
                return
            cur.execute(select_kin_types_finding, (self.finding_id,))
            kin_types = [i[0] for i in cur.fetchall()]
            self.kin_type_input1.insert(0, kin_types[0])
            self.kin_type_input2.insert(0, kin_types[1])

        self.other_person_input.focus_set()
        cur.close() 
        conn.close()        

    def show_one_person(self):
        self.new_evt_msg.config(text="Information about the new event "
            "relating to the current person.")
        age1 = Label(self.generic_data_inputs, text="Age")
        self.age1_input = EntryHilited1(self.generic_data_inputs, width=6)

        self.generic_data_inputs.columnconfigure(0, weight=1)
        age1.grid(column=0, row=4, sticky="e", pady=(0,1))
        self.age1_input.grid(
            column=1, row=4, sticky="w", padx=(3,0), pady=(0,1))
        
        self.lab0.config(text="Event Type: {} ({})".format(
            self.new_event,
            self.current_name))
        self.lab0.grid_configure(columnspan=2)

    def show_other_person(self):

        def radio_reflex():
            parent_type = self.offspringvar.get()
            if parent_type == 1:
                self.mother_or_father.config(text="father")
            elif parent_type == 2:
                self.mother_or_father.config(text="mother")

        self.new_evt_msg.config(text="Information about the new event "
            "relating to the current person and other primary participants "
            "in the event.")
        sep1 = Separator(self.frm, width=3)
        sep2 = Separator(self.frm, width=3)
        sep1.grid(column=0, row=1, columnspan=2, sticky="ew", pady=(12,0))
        sep2.grid(column=0, row=3, columnspan=2, sticky="ew", pady=(12,0))

        name1 = Label(self.couple_data_inputs, text=self.current_name)
        parent1 = Label(self.couple_data_inputs, text="mother")
        offspring = Label(self.couple_data_inputs, text="Name of Child")
        self.parent1_input = EntryAutoHilited(
            self.couple_data_inputs, width=32, 
            autofill=True, values=self.all_birth_names)
        self.offspring_input = EntryAutoHilited(
            self.couple_data_inputs, width=32, 
            autofill=True, values=self.all_birth_names)
        age1 = Label(self.couple_data_inputs, text="Age")
        self.age1_input = EntryHilited1(self.couple_data_inputs, width=6)
        kin_type1 = Label(self.couple_data_inputs, text="Kin Type")
        self.kin_type_input1 = Combobox(
            self.couple_data_inputs, self.root, values=self.kin_types)
        mother_is_it = LabelHilited(self.couple_data_inputs, text="mother")
        self.mother_or_father = LabelHilited(
            self.couple_data_inputs, text="(current person)")

        spacer = Frame(self.couple_data_inputs)

        name2 = Label(self.couple_data_inputs, text="Partner")
        self.other_person_input = EntryAutoHilited(
            self.couple_data_inputs, width=32, autofill=True, 
            values=self.all_birth_names)
        self.other_person_input.bind(
            "<FocusOut>", self.catch_dupe_or_new_partner)

        age2 = Label(self.couple_data_inputs, text="Age")
        self.age2_input = EntryHilited1(self.couple_data_inputs, width=6)
        kintype2 = Label(self.couple_data_inputs, text="Kin Type")
        self.kin_type_input2 = Combobox(
            self.couple_data_inputs, self.root, values=self.kin_types)
        radframe = Frame(self.couple_data_inputs)
        father_is_it = LabelHilited(self.couple_data_inputs, text="father")

        if self.new_event == "offspring":
            self.lab0.config(
                text="offspring (child of {})".format(self.current_name))
            age1.config(text="Current Person Age")
            offspring.grid(column=0, row=0, sticky='e', pady=(9,1))
            self.offspring_input.grid(
                column=1, row=0, sticky='w', padx=(3,0), pady=(9,1))
            self.mother_or_father.grid(column=1, row=2, sticky="w", padx=(2,0), ipadx=1)
            radframe.grid(column=4, row=2, sticky="w", padx=(2,0))
            self.offspringvar = tk.IntVar(None, 0)
            pardlabs = ("mother", "father")
            for i in range(2):
                rad = Radiobutton(
                    radframe,  
                    text=pardlabs[i],
                    value=i+1,
                    variable=self.offspringvar,
                    anchor='w',
                    command=radio_reflex)
                rad.grid(column=i, row=0)
        elif self.ma_pa is False:
            name1.grid(column=0, row=0, sticky="w", columnspan=2, pady=(9,1))
            self.kin_type_input1.grid(column=1, row=2, sticky="w", padx=(2,0))
            self.kin_type_input2.grid(column=4, row=2, sticky="w", padx=(2,0))
        else:
            parent1.grid(column=0, row=0, sticky='e', pady=(9,1))
            self.parent1_input.grid(
                column=1, row=0, sticky='w', padx=(3,0), pady=(9,1))
            name1.config(text="mother")
            name2.config(text="father")
            mother_is_it.grid(column=1, row=2, sticky="w", padx=(2,0), ipadx=1)
            father_is_it.grid(column=4, row=2, sticky="w", padx=(2,0), ipadx=1)
        age1.grid(column=0, row=1, sticky="e", pady=(0,1))
        self.age1_input.grid(
            column=1, row=1, sticky="w", padx=(3,0), pady=(0,1))
        kin_type1.grid(column=0, row=2, sticky="e")

        self.couple_data_inputs.columnconfigure(2, weight=1)
        spacer.grid(column=2, row=0, sticky="news", rowspan=3)

        name2.grid(column=3, row=0, sticky="e", pady=(9,1))
        self.other_person_input.grid(
            column=4, row=0, sticky="w", padx=(3,0), pady=(9,1))
        age2.grid(column=3, row=1, sticky="e", pady=(0,1))
        self.age2_input.grid(column=4, row=1, sticky="w", padx=(3,0), pady=(0,1))
        kintype2.grid(column=3, row=2, sticky="e", padx=(9,0)) 

    def cancel(self):
        self.root.focus_set()
        self.root.lift()
        self.destroy()

    def add_event(self):
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()

        self.age_1 = self.age1_input.get()
        if self.couple_event == 1:
            self.age_2 = self.age2_input.get()
            self.other_person = self.other_person_input.get()

        if self.edit_event is False:
            if self.new_event == "offspring":
                self.offspring_ok()
            elif self.couple_event == 0:
                cur.execute(
                    insert_finding_new, (
                        self.new_finding, self.age_1, 
                        self.event_type_id, self.current_person))
                conn.commit()            
            else:
                cur.execute(
                    insert_finding_new_couple, 
                    (self.new_finding, self.event_type_id,))
                conn.commit()

                self.couple_ok()  
            
            if len(self.place_string) == 0:
                cur.execute(insert_finding_places_new, (self.new_finding,))
                conn.commit()
            else:
                self.update_db_place()

            update_particulars(
                self.particulars_input.get().strip(), self.new_finding)
        else:
            if self.couple_event == 0:
                if self.ma_pa is True:
                    ma_input = self.parent1_input.get()
                    ma_age = self.age1_input.get()
                    pa_input = self.other_person_input.get()
                    pa_age = self.age2_input.get()
                    self.ma_pa_ok(ma_input, pa_input, ma_age, pa_age)           

            elif self.couple_event == 1:
                self.couple_ok()
            else:
                print("line", looky(seeline()).lineno, "case not handled:")
            place_string = self.place_input.get()
            if len(place_string) == 0:
                cur.execute(update_finding_places_null, (self.finding_id,))
                conn.commit()
            else:
                self.update_db_place()

            update_particulars(
                self.particulars_input.get().strip(), self.finding_id)

        cur.close()
        conn.close()
        self.cancel()
        self.go_to(current_person=self.current_person)

    def offspring_ok(self):

        def make_new_person(new_name=None):
            if new_name is None:
                return
        other_person_id = None
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        other_person = self.other_person_input.get().split("  #")
        if len(other_person) == 0:
            pass
        elif len(other_person) == 1:
            # make_new_person()
            pass
        else:
            other_person_id = other_person[1]
        child_id = self.offspring_input.get().split("  #")
        if len(child_id) < 2:
            # make_new_person()
            pass
        else:
            child_id = child_id[1]
        age1 = self.age1_input.get()
        age2 = self.age2_input.get()
        partner_kin_type = self.offspringvar.get()
        if partner_kin_type == 1:
            kin_type1 = 2
        else:
            kin_type1 = 1
        child_kin_type = 6

        cur.execute(select_max_finding_id)
        new_finding = cur.fetchone()[0] + 1

        cur.execute(insert_finding_birth, (new_finding, child_id))
        conn.commit()
        cur.execute(insert_findings_persons_new_couple, 
            (new_finding, self.current_person, age1, kin_type1, 
                other_person_id, age2, partner_kin_type)) 
        cur.close()
        conn.close()

    def ma_pa_ok(self, ma_input, pa_input, ma_age, pa_age):
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        ma_id = None
        pa_id = None
        ma_name = ""
        pa_name = ""
        if len(ma_input) != 0:
            ma_input = ma_input.split("  #")
            ma_name = ma_input[0]
            ma_id = ma_input[1]
        if len(pa_input) != 0:
            pa_input = pa_input.split("  #")
            pa_name = pa_input[0]
            pa_id = pa_input[1]

        cur.execute(update_findings_persons_1_2, (ma_id, pa_id, self.finding_id))
        conn.commit()

        cur.execute(update_findings_persons_mother, 
            (ma_age, ma_id, self.finding_id))
        conn.commit()

        cur.execute(update_findings_persons_father, 
            (pa_age, pa_id, self.finding_id))
        conn.commit()

        cur.close()
        conn.close()

    def couple_ok(self):                
        if len(self.other_person) != 0:
            other_person_all = self.other_person.split(" #")
            other_person_id = other_person_all[1]
        else:
            other_person_id = None
        if self.edit_event is True:
            self.edit_existing_event()
        else:
            self.talk_to_db(other_person_id)

    def talk_to_db(self, other_person_id):
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()

        self.kin_type_list = list(
            zip(self.kin_type_list, self.new_kin_type_codes))
        self.kin_type_list = [list(i) for i in self.kin_type_list]

        for item in self.kin_type_list:
            if item[1] is None:
                continue
            else:
                cur.execute(
                    insert_kin_type_new, 
                    (item[0], item[1].get()))
                conn.commit()
                cur.execute("SELECT seq FROM SQLITE_SEQUENCE WHERE name = 'kin_type'")
                new_id = cur.fetchone()[0]
                item[0] = new_id

        cur.execute(
            insert_findings_persons_new_couple,
            (self.new_finding, self.current_person, self.age_1, 
                self.kin_type_list[0][0], other_person_id, self.age_2, 
                self.kin_type_list[1][0]))
        conn.commit()
        cur.close()
        conn.close()

    def edit_existing_event(self):
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        cur.execute(
            select_findings_persons_parents,
            (self.finding_id,))
        right_pair = cur.fetchone()
        idx = right_pair.index(self.current_person)
        if idx == 0:
            sql = update_findings_persons_2
        elif idx == 1:
            sql = update_findings_persons_1
        cur.execute(
            sql, (other_person_id, self.finding_id))
        conn.commit()

        # parameterize this repeated block of code
        self.kin_type_list = list(
            zip(self.kin_type_list, self.new_kin_type_codes))
        self.kin_type_list = [list(i) for i in self.kin_type_list]
        for item in self.kin_type_list:
            if item[1] is None:
                continue
            else:
                cur.execute(
                    insert_kin_type_new, 
                    (item[0], item[1].get()))
                conn.commit()
                cur.execute("SELECT seq FROM SQLITE_SEQUENCE WHERE name = 'kin_type'")
                new_id = cur.fetchone()[0]
                item[0] = new_id
        # *******************************
        cur.execute(
            update_findings_persons_couple_old, (
                self.age_1, self.kin_type_list[0][0], 
                self.finding_id, self.current_person))
        conn.commit()
        cur.execute(
            update_findings_persons_couple_new, (
                self.age_2, self.kin_type_list[1][0], 
                other_person_id, self.finding_id, self.current_person))
        conn.commit()
        cur.close()
        conn.close()

    def update_db_place(self):
        if self.place_dicts is None: return
        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()
        ids = []
        for dkt in self.place_dicts:            
            ids.append(dkt["id"])
        qty = len(self.place_dicts)
        nulls = 9 - qty
        ids = ids + [None] * nulls
        last = len(self.place_dicts) - 1
        q = 0
        for dkt in self.place_dicts:
            child = dkt["id"]
            if q < last:
                parent = self.place_dicts[q+1]["id"]
            else:
                parent = None
            if child == dkt["temp_id"]:
                cur.execute(insert_place_new, (child, dkt["input"]))
                conn.commit()
                cur.execute(insert_places_places_new, (child, parent))
                conn.commit()
            else:
                if (child, parent) not in places_places:
                    places_places.append((child, parent))
                    cur.execute(insert_places_places_new, (child, parent))
                    conn.commit()
            q += 1

        if self.edit_event is False:
            ids.append(self.new_finding)
            cur.execute(insert_finding_places_new_event, tuple(ids))
            conn.commit() 
        else:            
            ids.append(self.finding_id)
            print("line", looky(seeline()).lineno, "ids:", ids)
            cur.execute(update_finding_places, tuple(ids))
            conn.commit() 

        place_strings.insert(0, self.place_string)

        self.place_autofill_values = EntryAuto.create_lists(place_strings)
            
        cur.close()
        conn.close()

    def validate_kin_types(self):

        def err_done2(widg):
            msg[0].destroy() 
            self.grab_set()
            widg.focus_set()

        conn = sqlite3.connect(current_file)
        conn.execute('PRAGMA foreign_keys = 1')
        cur = conn.cursor()

        self.kin_type_list = [
            self.kin_type_input1.get(), self.kin_type_input2.get()]

        new_kin_types = []
        for kin_type_input in [self.kin_type_input1, self.kin_type_input2]:
            if len(kin_type_input.get()) == 0:
                msg = open_error_message(
                    self, 
                    events_msg[1], 
                    "No Kin Type Selected", 
                    "OK")
                msg[0].grab_set()
                msg[1].config(aspect=400)
                msg[2].config(
                    command=lambda widg=kin_type_input: err_done2(widg))
                return
        v = 0
        for item in self.kin_type_list:
            if item in self.kin_types:
                k = 0
                for stg in self.kin_types:
                    if stg == item:
                        idx = k
                        self.kin_type_list[v] = self.kintypes_and_ids[idx][0]
                    k += 1
                new_kin_types.append(None)
            else:
                if type(item) is not int and len(item) != 0:
                    new_kin_types.append(item)            
            v += 1
        if new_kin_types != [None, None]:
            self.new_kin_type_codes = NewKinTypeDialog(
                self.root,
                new_kin_types,
                self).show()

        cur.close()
        conn.close()
        self.add_event()

    def catch_dupe_or_new_partner(self, evt):

        def err_done(): 
            self.other_person_input.focus_set()
            self.other_person_input.delete(0, 'end')
            self.grab_set()
            msg[0].destroy()

        if self.couple_event == 0: return
        person_and_id = self.other_person_input.get().split("#")
        if len(person_and_id[0]) == 0: return
        if len(person_and_id) == 1:
            self.open_new_person_dialog(person_and_id)
        elif self.current_person == int(person_and_id[1]):
            msg = open_error_message(
                self, 
                events_msg[0], 
                "Duplicate Persons in Couple", 
                "OK")
            msg[0].grab_set()
            msg[1].config(aspect=400)
            msg[2].config(command=err_done)

    def open_new_person_dialog(self, new_name):
        new_partner_dialog = Toplevel(self)
        new_partner_dialog.title("Add New Person")
        person_add = PersonAdd(
            new_partner_dialog, self.other_person_input, self.root)
        person_add.grid()
        person_add.name_input.delete(0, 'end')
        person_add.name_input.insert(0, new_name[0])
        person_add.add_person()
        person_add.show_sort_order()
        person_add.gender_input.focus_set()

    def validate_place(self, evt):
        inwidg = evt.widget
        self.place_string = inwidg.get().strip()
        if len(self.place_string) == 0:
            return
        place_validator = ValidatePlace(
            self.root, 
            self.treebard,
            inwidg,
            '',
            self.place_string,
            self.new_finding)
        self.place_dicts = place_validator.input_new_event()
        self.place_autofill_values.insert(0, inwidg.get())
        if place_validator.new_place_dialog is not None:
            self.place_validator = place_validator.new_place_dialog.new_places_dialog
            self.place_validator.bind("<Destroy>", self.focus_new_event_dialog)
            self.place_validator.grab_set()

    def focus_new_event_dialog(self, evt=None):
        self.grab_set()
        self.lift()

class NewKinTypeDialog(Toplevel):

    def __init__(
            self, master, new_kin_types,  
            new_event_dialog, *args, **kwargs):
        Toplevel.__init__(self, master, *args, **kwargs)
        self.root = master
        self.new_event_dialog = new_event_dialog

        self.kinradvars = [None, None]

        self.title("New Kin Types Dialog")
        self.columnconfigure('all', weight=1)
        self.make_widgets()
        column = 0
        for item in new_kin_types:
            self.make_widgets_for_one(item, column)            
            column += 1
        self.grab_set()

    def make_widgets(self):
        buttons = Frame(self)
        buttons.grid(column=0, row=1, columnspan=2, sticky='e')
        ok_rads = Button(buttons, text="OK", command=self.ok_new_kin_type)
        ok_rads.grid(column=0, row=0, padx=12, pady=12)
        cancel_rads = Button(buttons, text="CANCEL", command=self.cancel_new_kin_type)
        cancel_rads.grid(column=1, row=0, padx=12, pady=12)

    def make_widgets_for_one(self, item, column): 
        if item is None:
            return
        radframe = Frame(self)
        radframe.grid(column=column, row=0, sticky="news", padx=12, pady=(6,0))
        radios = []
        radvar = tk.StringVar(None, "B")
        self.kinradvars[column] = radvar
        head = LabelH3(radframe, text="Create new kin type: {}".format(item))
        head.grid(column=0, row=0, padx=12, pady=(6,0))
        instrux = Label(radframe, text="Describe this kin type's role:")
        instrux.grid(column=0, row=1, padx=12, pady=(6,0))
        kinrads = [
            ("parent", "B"), ("sibling", "C"), 
            ("partner", "D"), ("child", "E")]
        d = 2
        for tup in kinrads:
            rad = Radiobutton(
                radframe, 
                text=tup[0], 
                variable=radvar,
                value=tup[1],
                anchor="w")
            rad.grid(column=0, row=d, sticky='we', padx=12, pady=(6,0))
            radios.append(rad)  
            d += 1
        d = d
        radios[0].focus_set()

    def show(self):
        self.root.wait_window(self)
        return self.kinradvars        

    def ok_new_kin_type(self):
        self.destroy()
        self.cancel_new_kin_type()

    def cancel_new_kin_type(self):
        self.grab_release()
        self.new_event_dialog.focus_set()
        self.new_event_dialog.lift()
 
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

    strings = make_all_nestings(select_all_place_ids)
    place_autofill_values = EntryAuto.create_lists(strings)

    auto = EntryAuto(root, width=50, autofill=True, values=place_autofill_values)


    auto.focus_set()   

    move = tk.Entry(root)

    auto.grid()
    move.grid()

    root.mainloop()


# DO LIST

# BRANCH: events_table
# The offspring event is a continuous thorn in my side. At least put it in the dict same as any other event, bec it's a row in the table same as any event, so stop nesting it inside the birth event dict, this will greatly simplify the code.
# test the kintips systems thoroughly by using it to create people from scratch. Anything that can't be done, make it possible. The goal is to totally replace the way that genbox makes parents and children so the whole immediate family area becomes unnecessary, could be replaced by a non-active display like a pannable pedigree for example. Then maybe make the pannable pedigree active anyway.
# make sure it can still be done if only one parent is known, and you have to be able to add the unknown parent(s) also.
# make sure you can't add an offspring by a certain person_id if the parents already have that person as an offspring. Think of other physically impossible things that have to be disallowed.
# make sure it works if the child's and/or partner's name is a new person
# add 'unknown' to kin_types in case someone doesn't want to display e.g. 'husband' for an unknown person, might need unknown for generic kin and unknown2 for couple events but if possible make unknown a special case which can be used anywhere
# SEE # parameterize
# on right-clicking a kintip, a dlg opens to edit non-missing persons e.g.add/edit a child/name on offspring
# when couple asker closes, the afterdeath asker works and has grabset and the OK button has focus, but the titlebar doesn't change color.
# add tooltips/status bar messages
# open kintips with spacebar when kin button is in focus, not just mouse click
# bind all ok buttons to Return and cancel buttons to Escape
# finish the Border code so it only makes scridth & scrollbar if make_scrollbar is True but make it False by default, show NO Windows title bars on ANY dialog
# detect if kintips text is too long and if so change font-size to boilerplate
# get rid of ttk combobox in new person dialog 
# test notes & roles all features; esp. test roles re: `if self.role_person_edited is True:` since new_person_id is no longer real but temp at this point in names.py and get rid of ttk.Combobox
# Q: Is it possible to eliminate the immediate family area (pedigree area) above the table because of the kin column and its clickable functionalities? IE could a parent or child be added this way?

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
# get rid of nesting in styles.py by passing conn, cur

# BRANCH: sources
# IDEA for copy/pasting citations. This is still tedious and uncertain bec you never know what's in a clipboard, really. Since the assertions are shown in a table, have a thing like the fill/drag icon that comes up on a spreadsheet when you point to the SE corner of a cell. The icon turns into a different icon, maybe a C for Copy, and if you click down and drag at that point, the contents of the citation are pasted till you stop dragging. Should also work without the mouse, using arrow keys. If this idea isn't practical, it still leads to the notion of a tabular display of citations which would make copy & paste very easy instead of showing citations a click apart from each other, and seeing them all together might be useful for the sake of comparison?

# add to do list for combobox: when scrolling if the mouse strays off the scrollbar the dropdown undrops, I've seen a way to fix that but what was it?
# add to main do list re: all dialogs: run the same code when clicking X on title bar
# add to do list for new_event dialog: add person search button 




# ADD TO DEV DOCS FOR EVENTS TABLE.PY: is it possible to get rid of persons_persons table? There seems to be a one-to-one relationship between the finding_id in a couple event and the persons_persons_id in that event. So look at what persons_persons is being used for. Can the finding_id be used instead? Seems like they aren't exactly the same thing because finding_id has 2 records in findings_persons for each event where the two people are related, but 1 record in persons_persons. Try to remember why I created this table to begin with. Something to do with ??? I have no idea but it's very recent so shd have left a trail of blather in some rollback with the rationale behind this annoying data item. Look at August rollbacks for a hint. For ex on aug 28 I wrote "But let's say you want to search how many 2 people are linked to each other. This would be a very simple search if each event in which the 2 are coupled is a separate persons_persons_id.) Another question: have I put the fk in the wrong table? Now I'm putting persons_persons_id in findings_persons table. Should I instead be putting finding_id in persons_persons table? Then there's a directly discernible reason for each row in the p_P table to exist instead of just these 2 mysterious columns. But it would be a drastic redesign to move finding_id to persons_persons out of findings_persons where it is now and it seems like I'm very close to making the code work, since it already works for same-name couple (spouse/spouse), all I need is to make the code work for diff-name couples (wife/husband) and since it's already close, I shd resist the temptation to rip the building down to the foundations, change the foundations, and start over completely because that's what I'd have to do, I'd have to refactor the events_table code again and I kinda refuse." But what was the original reason to make the table? Here it is, same day: "select_findings_details_couple is inadequate since it looks for pairs of matched kin_type_id but wife & husband have different ids whereas spouse & spouse have the same. Need a better way to select partnerships eg maybe a new table called couples so that each coupling will have a separate couple_id (persons_persons_id). It should be a table called persons_persons because it is many to many, each person can have any number of links to each other person including more than one link to the same person in case the same couple gets married twice etc. Then put fk persons_persons_id in findings_persons. The persons_persons table might be useful for other relationship problems later on such as people with real parents, foster parents, and adoptive parents for example." So in short, the problem I was having was that I was doing something by searching for matching kin type to find spouses, but this didn't work eg with "wife" and "husband" because the kin types didn't match. So I had to register the relationship as a single record in a table to easily detect the relationship.









