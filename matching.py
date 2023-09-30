import tkinter as tk
from tkinter import scrolledtext
from tkinterdnd2 import DND_FILES, TkinterDnD

def dropedFile_path():
    outer = "" 
    def on_drop(event):
        nonlocal outer
        file_paths = event.data
        file_label.config(text="Dropped files:\n" + "\n".join(file_paths))
        outer = file_paths
        root.destroy()  

    root = TkinterDnD.Tk()

    file_label = tk.Label(root, text="Drag&Drop Your text file.")
    file_label.pack(padx=30, pady=90)

    root.drop_target_register(DND_FILES)
    root.dnd_bind('<<Drop>>', on_drop)
    root.mainloop()
    return outer

def fileRead(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    lines = lines[2:]
    return lines

def fillTheDict(lines):
    my_dict= {}
    current_value = None
    for line in lines:
        line = line.strip()  
        if line.startswith('"'):
            word = line.strip('"')  
            my_dict[word] = current_value 
        else:
            current_value = float(line.replace(',', '.'))  
    return my_dict

def keyLister(lines):
    keys_list = []
    for line in lines:
        line = line.strip()  
        if line.startswith('"'):
            word = line.strip('"')  
            keys_list.append(word)
    return keys_list

def wrongePriceFinder(keys_list, my_dict):
    output = ""
    for i in range(len(keys_list)):
        for j in range(len(keys_list)):#eğer dict key i dict key j nin içerisinde var ise ve keyi value büyükse keyj value
            if keys_list[i] in keys_list[j] and keys_list[i]!=keys_list[j]:
                output +="root:{:40} branch:({})\n".format(str(keys_list[j]), str(keys_list[i]) )
    output += "------------------------------------------------\n"
    for i in range(len(keys_list)):
        for j in range(len(keys_list)):#eğer dict key i dict key j nin içerisinde var ise ve keyi value büyükse keyj value
            if keys_list[i] in keys_list[j] and keys_list[i]!=keys_list[j] and my_dict[keys_list[i]]>my_dict[keys_list[j]]:
                output +="root:{:40}-{}          (branch:{}-{})\n".format(str(keys_list[j]), str(my_dict[keys_list[j]]), str(keys_list[i]), str(my_dict[keys_list[i]]) )            
                #print(output)
    return output

def openWindow(output_text):
    window = tk.Tk()
    window.title("Output Window")
    window.geometry("700x400")  

    
    window.configure(bg="#2E2E2E")  

    output_widget = scrolledtext.ScrolledText(window, width=120, height=30, bg="#1E1E1E", fg="white")
    output_widget.pack(padx=10, pady=10)  

    output_widget.insert(tk.END, output_text)
    output_widget.tag_configure("center", justify='center')
    output_widget.tag_add("center", "1.0", "end")
    output_widget.config(state="disabled")  

    window.mainloop()

file_path = dropedFile_path()
lines = fileRead(file_path)
my_dict = fillTheDict(lines)
keys_list = keyLister(lines)
output_text = wrongePriceFinder(keys_list,my_dict)

openWindow(output_text)

