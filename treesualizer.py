#!/usr/bin/python

import tkinter as tk
import tkinter.ttk as ttk
import sys
import re


def selectItem(event):
    curItem = tree.focus()
    search_node = curItem
    for path, item in tree_nodes.items(): 
        if item == search_node:
            label.delete(0,tk.END)
            label.insert(0,path)


def show_results():
    search_term = entry_search.get()
    listview.delete(0,tk.END)
    for key in tree_nodes.keys():
        if search_term.lower() in key.lower():
            listview.insert(tk.END, key)


def show_all(list_of_paths):
    first_line = list_of_paths.pop(0)
    tree_nodes[first_line] = tree.insert('', tk.END, text=first_line)
    for line in list_of_paths:
        items = line.strip().split('/')
        parent = '/'.join(items[:-1])
        child = items[-1:]
        new_key = (parent+"/"+child[0] if parent else child[0])
        try:
            tree_nodes[new_key] = tree.insert(tree_nodes[parent], tk.END, text=child)
        except:
            pass

    for key in tree_nodes.keys():
        listview.insert(tk.END, key)

    window.mainloop()


def usage():
    print ("""This script parse output of linux 'tree' command and shows it in a treeview and listview for easier search.\n
    Usage:
    \t{} <path_to_filename>
    """)
    exit(0)


def get_tree(filename):
    paths = []
    indent = 1
    with open(filename, 'r') as f:
        for line in f.readlines():
            nice_line = line.strip()
            first_char = re.search('[a-zA-Z0-9\.]',nice_line)
            if first_char:
                first_char_idx = nice_line.find(first_char.group(0),0)
                if indent == 1 and first_char_idx > 1:
                    indent = first_char_idx
                entry_text = nice_line[first_char_idx:]
                count = first_char_idx // indent
                last_entry_path_items = (paths[-1][:count] if len(paths)>0 else [])
                new_entry = last_entry_path_items[:]
                new_entry.append(entry_text)
                paths.append(new_entry)
    list_of_paths = []
    for path in paths:
        o = '/'.join(path)
        list_of_paths.append(o)
    return list_of_paths[:]


def main():
    if len(sys.argv) < 2:
        usage()
    filename = sys.argv[1]
    list_of_paths = get_tree(filename) # converts tree-like view into linux-filesyste-like paths
    show_all(list_of_paths)


window = tk.Tk()
window.geometry("700x500")
window.rowconfigure(1, weight=3)
window.rowconfigure(4, weight=3)
window.columnconfigure(1, weight=3)
tree = ttk.Treeview(window)

label = tk.Entry(master=window)
label.grid(columnspan=3, sticky=tk.E+tk.W)

tree.grid(columnspan=3, sticky=tk.E+tk.W+tk.N+tk.S)
tree.bind('<ButtonRelease-1>', selectItem)

label_search = tk.Label(master=window, text="Search: ")
label_search.grid(row=3, sticky=tk.W)
entry_search = tk.Entry(master=window)
entry_search.grid(row=3,column=1, sticky=tk.W+tk.E)
button_search = tk.Button(master=window, text="Search", command=show_results)
button_search.grid(row=3,column=2, sticky=tk.E)

listview = tk.Listbox(master=window)
listview.grid(columnspan=3, sticky=tk.E+tk.W+tk.N+tk.S)

tree_nodes = {}

if __name__ == "__main__":
    main()