# IMPORTS

from tkinter import *
import pickle
import pyperclip
import numpy as np


class Biblio:

    def __init__(self, window):
        self.p = "C:\\Users\\tigerault\\PycharmProjects\\Multitag\\Storage"
        self.blocs = self.import_dict(self.p, 'blocs')
        self.tag_list = self.build_tag_list(self.blocs)
        self.plan = self.import_dict(self.p, 'plan')
        self.tagging = 0
        self.window = window

        self.var = IntVar()

        self.merge_var = IntVar()

        self.save_var = IntVar()

        self.merge_tick = Checkbutton(
            window,
            text='Merge ?',
            variable=self.merge_var)
        self.merge_tick.place(x=1300, y=500)

        self.input_but = Button(
            window,
            text='Input',
            height=1,
            width=10,
            command=self.add_to_blocs)
        self.input_but.place(x=420, y=500)

        self.tag_but = Button(
            window,
            text='Tagging',
            height=1,
            width=10,
            command=self.tag_blocs)
        self.tag_but.place(x=1100, y=500)

        self.add_tag_but = Button(
            window,
            text='Add',
            height=1,
            width=10,
            command=self.add_plan)
        self.add_tag_but.place(x=70, y=500)

        self.take_note_but = Button(
            window,
            text='Take notes',
            height=1,
            width=10,
            command=self.edit_notes_from_plan)
        self.take_note_but.place(x=1300, y=650)

        self.save_note_but = Button(
            window,
            text='Save',
            height=1,
            width=10,
            command=lambda: self.save_var.set(1))
        self.save_note_but.place(x=1300, y=700)

        self.del_tag_but = Button(
            window,
            text='Delete',
            height=1,
            width=10,
            command=self.delete_plan)
        self.del_tag_but.place(x=160, y=500)

        self.edit_tag_but = Button(
            window,
            text='Edit',
            height=1,
            width=10,
            command=self.edit_plan)
        self.edit_tag_but.place(x=250, y=500)

        self.tag_next_but = Button(
            window,
            text='Next',
            height=1,
            width=10,
            command=lambda: self.var.set(1))
        self.tag_next_but.place(x=1200, y=500)

        self.search_but = Button(
            window,
            text='Search all',
            height=1,
            width=10,
            command=self.blocs_filter_search)
        self.search_but.place(x=810, y=500)

        self.plan_listbox = Listbox(
            window,
            height=30,
            width=50,
            selectmode=EXTENDED)
        self.plan_listbox.place(x=50, y=10)
        new = self.build_plan()
        for k in range(len(self.plan["position"])):
            self.plan_listbox.insert(self.plan["position"][k], new[k])
        self.plan_listbox.bind('<<ListboxSelect>>', self.blocs_filter_plan)

        self.source_listbox = Listbox(
            window,
            height=30,
            width=20,
            selectmode=EXTENDED)
        self.source_listbox.place(x=400, y=10)
        for k in np.unique(self.blocs["source"]):
            self.source_listbox.insert(END, k)
        self.source_listbox.bind('<<ListboxSelect>>', self.blocs_filter_sources)

        self.blocs_listbox = Listbox(
            window,
            height=30,
            width=60,
            selectmode=EXTENDED)
        self.blocs_listbox.place(x=550, y=10)
        self.blocs_listbox.bind('<<ListboxSelect>>', self.read_blocs)

        self.search_text = Text(
            window,
            height=1,
            width=30)
        self.search_text.place(x=550, y=500)

        self.shell_text = Text(
            window,
            height=30,
            width=60)
        self.shell_text.place(x=1000, y=10)

        self.notes_text = Text(
            window,
            height=17,
            width=150)
        self.notes_text.place(x=50, y=550)

    def import_dict(self, path, name):
        with open(path + '\\' + name + '.pkl', 'rb') as f:
            return pickle.load(f)

    def save_dict(self, path, name, d):
        with open(path + '\\' + name + '.pkl', 'wb') as f:
            pickle.dump(d, f)

    def build_tag_list(self, blocs):
        tl = []
        for i in blocs["tag"]:
            for j in i:
                if len(j) > 0:
                    if j[0] not in tl:
                        tl += [j]
        return tl

    def build_plan(self):
        built_plan = []
        for k in range(len(self.plan["position"])):
            for l in self.tag_list:
                if self.plan["ID"][k] == l[1]:
                    built_plan += ['___' * self.plan["order"][k] + l[0]]
                    break
        return built_plan

    def add_to_blocs(self):
        # to edit existing tags on a bloc, recall this function for just 1 bloc
        sep = input("Extracts separator : ")
        if sep in self.blocs["source"]:
            print('Already added')
            return None
        else:
            input('Paste?')
            article = pyperclip.paste().replace('\r', '')

            if sep not in article or len(sep) == 0:
                print("Veuillez reessayer, separateur introuvable")
                return None

            bloc_s = 0

            for k in range(article.count(sep)):
                bloc_e = article.index(sep)
                self.blocs['text'] += [article[bloc_s:bloc_e].replace('\n', '').replace('\t', '')]
                self.blocs['source'] += [sep]
                self.blocs['tag'] += [[]]
                # shorten the string for the index function to find the next occurrence
                article = article[bloc_e + len(sep):]

            self.save_dict(self.p, 'blocs', self.blocs)
            self.blocs = self.import_dict(self.p, 'blocs')

            self.source_listbox.delete(0, END)
            for k in np.unique(self.blocs["source"]):
                self.source_listbox.insert(END, k)

    def tag_blocs(self):
        self.tagging = 1
        self.tag_list = self.build_tag_list(self.blocs)
        sep = self.source_listbox.get(self.source_listbox.curselection())
        # create a selectable list of these tags, an ok button and an add button
        selected = []
        for k in range(len(self.blocs["text"])):
            if self.blocs["source"][k] == sep:
                selected += [self.blocs["text"][k]]

        deleted = 0
        for l in range(len(selected)):
            k = l - deleted
            # Color current focus bloc
            self.blocs_listbox.itemconfig(l, bg='green')
            # Show text in shell
            self.shell_text.delete('1.0', "end-1c")

            if self.merge_var.get() == 0:
                add_tag = self.blocs["text"].index(selected[k])
            if l < len(selected) - 1:
                next = self.blocs["text"].index(selected[k + 1])
                self.shell_text.insert(END, self.blocs["text"][add_tag] + '\n\nNext : \n\n' + self.blocs["text"][next])
            else:
                self.shell_text.insert(END, self.blocs["text"][add_tag])
            self.merge_var.set(0)

            # Show existing tags
            # Reset colors
            for k in self.plan["position"]:
                self.plan_listbox.itemconfig(k, bg='white')
            # Color existing tags
            for j in range(len(self.blocs["text"])):
                if self.blocs["text"][j] == self.blocs["text"][add_tag]:
                    for i in self.blocs["tag"][j]:
                        for m in range(len(self.plan["ID"])):
                            if i[1] == self.plan["ID"][m]:
                                self.plan_listbox.itemconfig(self.plan["position"][m], bg='green')
            # Wait for button press
            self.tag_next_but.wait_variable(self.var)
            if self.merge_var.get() == 1:
                deleted += 1
                # Merge text
                self.blocs["text"][add_tag] += self.blocs["text"][next]
                # Merge existing tags
                self.blocs["tag"][add_tag] += self.blocs["tag"][next]

                del selected[k + 1]
                del self.blocs["text"][next]
                del self.blocs["source"][next]
                del self.blocs["tag"][next]

                self.save_dict(self.p, 'blocs', self.blocs)
                self.blocs = self.import_dict(self.p, 'blocs')

            add = []
            focus = self.plan_listbox.curselection()
            # if a tag selection has been made
            if len(focus) > 0 :
                tag = [focus[0]]
                # To associate bloc to selected tag but also his parents.
                for k in range(self.plan["order"][self.plan["position"].index(tag[0])]):
                    tag += [self.get_parent(tag[-1])]
                for i in tag:
                    id = self.plan["ID"][self.plan["position"].index(i)]
                    for j in self.tag_list:
                        if j[1] == id:
                            add += [j]

                self.blocs["tag"][add_tag] += add
                unique_tags = []
                for n in self.blocs["tag"][add_tag]:
                    if n not in unique_tags:
                        unique_tags += [n]
                self.blocs["tag"][add_tag] = unique_tags

        self.save_dict(self.p, 'blocs', self.blocs)
        self.blocs = self.import_dict(self.p, 'blocs')
        self.tag_list = self.build_tag_list(self.blocs)
        self.save_dict(self.p, 'plan', self.plan)
        self.plan = self.import_dict(self.p, 'plan')

        self.tagging = 0

    def get_parent(self, position):
        parent = []
        for k in range(len(self.plan["position"])):
            if self.plan["position"][k] < position and self.plan["order"][k] == self.plan["order"][self.plan["position"].index(position)] - 1:
                parent += [self.plan["position"][k]]
        return max(parent)

    def access_from_plan(self):
        # to be called as soon as pressed
        # get selected from list
        position_selected = 0
        blocs_selected = []
        for k in range(len(self.blocs["tag"])):
            for l in range(len(self.blocs["tag"][k])):
                if self.plan["ID"][position_selected] == self.blocs["tag"][k][l]:
                    blocs_selected += [self.blocs["text"][k]]

    def add_plan(self):
        # to be called on edit button press
        new_tag = input('New category? : ')
        if new_tag not in [j[0] for j in self.tag_list]:
            if len(self.plan["ID"]) == 0:
                new_ID = 1
            else:
                new_ID = max(self.plan["ID"]) + 1
            self.plan["ID"] += [new_ID]
            position = int(input('position : '))
            if position in self.plan["position"]:
                for k in range(len(self.plan["position"])):
                    if position <= self.plan["position"][k]:
                        self.plan["position"][k] += 1
            self.plan["position"] += [position]
            self.plan["order"] += [int(input('order : '))]
            self.plan["note"] += ['']
            self.blocs["tag"][0] += [[new_tag, new_ID]]

            self.save_dict(self.p, 'blocs', self.blocs)
            self.blocs = self.import_dict(self.p, 'blocs')
            self.tag_list = self.build_tag_list(self.blocs)
            self.save_dict(self.p, 'plan', self.plan)
            self.plan = self.import_dict(self.p, 'plan')

            self.plan_listbox.delete(0, END)
            for k in range(len(self.plan["position"])):
                new = self.build_plan()
                self.plan_listbox.insert(self.plan["position"][k], new[k])

    def delete_plan(self):
        pos = self.plan_listbox.curselection()[0]
        deleted = 0
        for i in range(len(self.plan["position"])):
            k = i - deleted
            if pos < self.plan["position"][k]:
                self.plan["position"][k] -= 1
            elif pos == self.plan["position"][k]:
                deleted = 1
                deleted_id = self.plan["ID"][k]
                del self.plan["position"][k]
                del self.plan["ID"][k]
                del self.plan["order"][k]
                del self.plan["note"][k]

        for k in range(len(self.blocs["tag"])):
            deleted = 0
            for i in range(len(self.blocs["tag"][k])):
                j = i - deleted
                if self.blocs["tag"][k][j][1] == deleted_id:
                    deleted += 1
                    del self.blocs["tag"][k][j]

        self.save_dict(self.p, 'blocs', self.blocs)
        self.blocs = self.import_dict(self.p, 'blocs')
        self.tag_list = self.build_tag_list(self.blocs)
        self.save_dict(self.p, 'plan', self.plan)
        self.plan = self.import_dict(self.p, 'plan')

        self.plan_listbox.delete(0, END)
        for k in range(len(self.plan["position"])):
            new = self.build_plan()
            self.plan_listbox.insert(self.plan["position"][k], new[k])

    def edit_plan(self):
        pos = self.plan_listbox.curselection()[0]
        new_name = input("Change name to : ")
        for k in range(len(self.plan["position"])):
            if pos == self.plan["position"][k]:
                id = self.plan["ID"][k]

        for k in range(len(self.blocs["tag"])):
            for j in range(len(self.blocs["tag"][k])):
                if self.blocs["tag"][k][j][1] == id:
                    self.blocs["tag"][k][j][0] = new_name
        print(self.blocs["tag"])

        self.tag_list = self.build_tag_list(self.blocs)
        self.plan_listbox.delete(0, END)
        for k in range(len(self.plan["position"])):
            new = self.build_plan()
            self.plan_listbox.insert(self.plan["position"][k], new[k])

    def edit_notes_from_plan(self):
        # Get corresponding notes
        pos = self.plan["position"].index(self.plan_listbox.curselection()[0])
        self.notes_text.delete('1.0', "end-1c")
        self.notes_text.insert("1.0", self.plan["note"][pos])
        # Wait for save button press
        self.save_note_but.wait_variable(self.save_var)
        note = self.notes_text.get("1.0", "end-1c")
        self.plan["note"][pos] = note

        self.save_dict(self.p, 'plan', self.plan)
        self.plan = self.import_dict(self.p, 'plan')

    def blocs_filter_plan(self, event):
        if self.tagging == 0:
            cursor = self.plan_listbox.curselection()
            for i in cursor:
                pos = self.plan["position"].index(i)
                selected = []
                sources = []
                for k in range(len(self.blocs["text"])):
                    for l in range(len(self.blocs["tag"][k])):
                        if len(self.blocs["tag"][k][l]) > 0:
                            if self.blocs["tag"][k][l][1] == self.plan["ID"][pos]:
                                selected += [self.blocs["text"][k]]
                                sources += [self.blocs["source"]]
                sources = list(np.unique(sources))
                self.blocs_listbox.delete(0, END)
                for k in selected:
                    self.blocs_listbox.insert(END, k)
                self.source_listbox.delete(0, END)
                for k in sources:
                    self.source_listbox.insert(END, k)
                # Get corresponding notes
                #self.notes_text.delete('1.0', "end-1c")
                #self.notes_text.insert("1.0", self.plan["note"][pos])

    def blocs_filter_sources(self, event):
        pos = self.source_listbox.curselection()[0]
        selected = []
        for k in range(len(self.blocs["text"])):
            if self.blocs["source"][k] == self.source_listbox.get(pos):
                selected += [self.blocs["text"][k]]

        self.blocs_listbox.delete(0, END)
        for k in selected:
            self.blocs_listbox.insert(END, k)

    def blocs_filter_search(self):
        self.blocs_listbox.delete(0, END)
        request = self.search_text.get("1.0", "end-1c")
        for k in self.blocs["text"]:
            if request in k:
                self.blocs_listbox.insert(END, k)


    def read_blocs(self, event):
        # Reset widgets
        self.shell_text.delete('1.0', "end-1c")
        for k in [list(np.unique(self.blocs["source"])).index(l) for l in self.blocs["source"]]:
            self.source_listbox.itemconfig(k, bg="white")
        for k in self.plan["position"]:
            self.plan_listbox.itemconfig(k, bg='white')

        for i in self.blocs_listbox.curselection():
            # Display in shell
            self.shell_text.insert(END, self.blocs_listbox.get(i) + '\n----\n')

            # Show corresponding tags and sources
            for j in range(len(self.blocs["text"])):
                if self.blocs["text"][j] == self.blocs_listbox.get(i):
                    source = self.blocs["source"][j]
                    self.source_listbox.itemconfig(list(np.unique(self.blocs["source"])).index(source), bg='green')

                    for k in self.blocs["tag"][j]:
                        for m in range(len(self.plan["ID"])):
                            if k[1] == self.plan["ID"][m]:
                                self.plan_listbox.itemconfig(self.plan["position"][m], bg='green')


win = Tk()
win.title('Add to plan')
win.attributes("-fullscreen", True)
mt = Biblio(win)
win.mainloop()
