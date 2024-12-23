from tkinter import *
from tkinter.ttk import *
from tkinter import font, colorchooser,filedialog,messagebox
import networkx as nx
import tkinter as tk
import os
import sys
import tempfile
from datetime import datetime

root = Tk()
# Node class for the BST
class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

# Binary Search Tree (BST) class
class BST:
    def __init__(self):
        self.root = None

    def insert(self, data):
        if self.root is None:
            self.root = Node(data)
        else:
            self._insert(self.root, data)

    def _insert(self, node, data):
        if data < node.data:
            if node.left is None:
                node.left = Node(data)
            else:
                self._insert(node.left, data)
        else:
            if node.right is None:
                node.right = Node(data)
            else:
                self._insert(node.right, data)

    def in_order(self):
        return self._in_order(self.root)

    def _in_order(self, node):
        if node:
            return self._in_order(node.left) + [node.data] + self._in_order(node.right)
        return []
    def find(self, data):
        data = str(data)  # Ensure search data is also treated as a string
        return self._find(self.root, data)

    def _find(self, node, data):
        if node is None:
            return False
        # Check if the search term is a substring of the node's data
        if data in node.data:
            return True
        elif data < node.data:
            return self._find(node.left, data)
        else:
            return self._find(node.right, data)

def insert_into_bst(event):
    # Get the current text from the text area
    current_text = textArea.get("1.0", 'end-1c')
    
    # Split the current text into individual words
    words = current_text.split()
    
    # Insert each word into the BST
    for word in words:
        bst.insert(word)
    # print(f"Inserted words into BST: {words}")

class TextEditorGraph:
    def __init__(self):
        self.nodes = []  # List to store nodes (characters)
        self.clipboard = []  # Store copied or cut text
    
    def add_text(self, text):
        """Converts text into graph nodes."""
        self.nodes = list(text)

    def cut_text(self, start_index, end_index):
        """Cut text between start_index and end_index."""
        cut_text = ''.join(self.nodes[start_index:end_index])
        self.clipboard = cut_text  # Store cut text
        self.nodes = self.nodes[:start_index] + self.nodes[end_index:]  # Remove text from graph

    def copy_text(self, start_index, end_index):
        """Copy text between start_index and end_index."""
        self.clipboard = ''.join(self.nodes[start_index:end_index])  # Store copied text
    
    def paste_text(self, index):
        """Paste clipboard text at the given index."""
        paste_text = list(self.clipboard)
        self.nodes = self.nodes[:index] + paste_text + self.nodes[index:]  # Insert pasted text at the index

    def get_text(self):
        """Get the full text as a string."""
        return ''.join(self.nodes)

class TextEditorApp:
    def __init__(self, root, text_editor_graph):
        self.root = root
        self.text_area = tk.Text(root, wrap="word")
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.text_editor = text_editor_graph
        self.setup_ui()

    def setup_ui(self):
        """Create menu and bind cut, copy, and paste commands."""
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        # Create Edit menu
        editmenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=editmenu)

        # Add cut, copy, and paste commands to the menu
        editmenu.add_command(label='Cut', accelerator='Ctrl+X', command=self.cut_event)
        editmenu.add_command(label='Copy', accelerator='Ctrl+C', command=self.copy_event)
        editmenu.add_command(label='Paste', accelerator='Ctrl+V', command=self.paste_event)

        # Bind Cut, Copy, and Paste to key events (Ctrl + X, Ctrl + C, Ctrl + V)
        self.root.bind("<Control-x>", self.cut_event)
        self.root.bind("<Control-c>", self.copy_event)
        self.root.bind("<Control-v>", self.paste_event)

    def cut_event(self, event=None):
        """Handle the cut event."""
        try:
            start_index = int(self.text_area.index(tk.SEL_FIRST).split('.')[1])
            end_index = int(self.text_area.index(tk.SEL_LAST).split('.')[1])
            self.text_editor.add_text(self.text_area.get("1.0", tk.END))  # Load the text into the graph
            self.text_editor.cut_text(start_index, end_index)
            self.text_area.delete(tk.SEL_FIRST, tk.SEL_LAST)  # Remove the text from the widget
            self.text_area.insert(tk.END, self.text_editor.get_text())  # Update the text widget
        except tk.TclError:
            pass  # Handle if no text is selected

    def copy_event(self, event=None):
        """Handle the copy event."""
        try:
            start_index = int(self.text_area.index(tk.SEL_FIRST).split('.')[1])
            end_index = int(self.text_area.index(tk.SEL_LAST).split('.')[1])
            self.text_editor.add_text(self.text_area.get("1.0", tk.END))  # Load the text into the graph
            self.text_editor.copy_text(start_index, end_index)
        except tk.TclError:
            pass  # Handle if no text is selected

    def paste_event(self, event=None):
        """Handle the paste event."""
        try:
            index = int(self.text_area.index(tk.INSERT).split('.')[1])
            self.text_editor.add_text(self.text_area.get("1.0", tk.END))  # Load the text into the graph
            self.text_editor.paste_text(index)
            self.text_area.delete("1.0", tk.END)  # Clear the current text
            self.text_area.insert(tk.END, self.text_editor.get_text())  # Insert the updated text
        except Exception as e:
            print("Error pasting text:", e)

# Create an instance of TextEditorGraph outside the Tkinter setup
text_editor_graph = TextEditorGraph()


root.title('Text Editor')
root.geometry('1200x620+10+10')
# root.resizable(False,False)

menuBar = Menu()
root.config(menu=menuBar)


#images settings 
newImage = PhotoImage(file='add-file.png')
newImage = newImage.subsample(25, 25)
openImage = PhotoImage(file='open-file.png')
openImage = openImage.subsample(25, 25)
saveImage = PhotoImage(file='data-storage.png')
saveImage = saveImage.subsample(25, 25)
saveAs_Image = PhotoImage(file='save.png')
saveAs_Image = saveAs_Image.subsample(25, 25)
exitImage = PhotoImage(file='exit.png')
exitImage = exitImage.subsample(25, 25)
copyImage = PhotoImage(file='copy.png')
copyImage = copyImage.subsample(25, 25)
pasteImage = PhotoImage(file='paste.png')
pasteImage = pasteImage.subsample(25, 25)
cutImage = PhotoImage(file='cutting.png')
cutImage = cutImage.subsample(25, 25)
selectImage = PhotoImage(file='select.png')
selectImage = selectImage.subsample(25, 25)
clearImage = PhotoImage(file='cleaning.png')
clearImage = clearImage.subsample(25, 25)
undoImage = PhotoImage(file='undo.png')
undoImage = undoImage.subsample(25, 25)
redoImage = PhotoImage(file='redo.png')
redoImage = redoImage.subsample(25, 25)
findImage = PhotoImage(file='find.png')
findImage = findImage.subsample(25, 25)
toolImage = PhotoImage(file='tool-box.png')
toolImage = toolImage.subsample(25, 25)
statusImage = PhotoImage(file='status-bar.png')
statusImage = statusImage.subsample(25, 25)
D_LightImage = PhotoImage(file='light_default.png')
P_lightImage = PhotoImage(file='light_plus.png')
monokaiImage = PhotoImage(file='monokai.png')
blueImage = PhotoImage(file='night_blue.png')
redImage = PhotoImage(file='red.png')
darkImage = PhotoImage(file='dark.png')
boldImage = PhotoImage(file='bold.png')
boldImage = boldImage.subsample(25, 25)
italicImage = PhotoImage(file='italics.png')
italicImage = italicImage.subsample(25, 25)
underlineImage = PhotoImage(file='underline-text-option.png')
underlineImage = underlineImage.subsample(25, 25)
font_colorImage = PhotoImage(file='color-wheel.png')
font_colorImage = font_colorImage.subsample(25, 25)
print_img = PhotoImage(file='icons8-print-50.png')
print_img = print_img.subsample(2, 2)
datetime_img = PhotoImage(file='icons8-schedule-50.png')
datetime_img = datetime_img.subsample(2, 2)

leftImage = PhotoImage(file='align-left.png')
leftImage = leftImage.subsample(25, 25)

rightImage = PhotoImage(file='align-right.png')
rightImage = rightImage.subsample(25, 25)

centerImage = PhotoImage(file='format.png')
centerImage = centerImage.subsample(25, 25)

#functions 

#  global declaration
fontSize = 12
fontStlye = 'Arial'
url = ''
undo_stack = []
redo_stack = []


#functions of Menu Bar --------------------------------------------------------------------->

# Function to change the font style
def font_style(event):
    global fontStlye
    fontStlye = font_family_variable.get()
    textArea.config(font=(fontStlye, fontSize))

# Function to change the font size
def font_size(event):
    global fontSize
    fontSize = int(size_variable.get())
    textArea.config(font=(fontStlye, fontSize))

#Function for boldeness
def bold_text():
    current_font = font.Font(font=textArea['font'])
    # Get current font attributes
    family = current_font.actual()['family']
    size = current_font.actual()['size']
    slant = current_font.actual()['slant']
    underline = current_font.actual()['underline']
    # Toggle weight
    weight = 'bold' if current_font.actual()['weight'] == 'normal' else 'normal'
    # Apply updated font
    textArea.config(font=(family, size, weight, slant))
    textArea['font'] = font.Font(family=family, size=size, weight=weight, slant=slant, underline=underline)

# Function for italic
def italic_text():
    current_font = font.Font(font=textArea['font'])
    # Get current font attributes
    family = current_font.actual()['family']
    size = current_font.actual()['size']
    weight = current_font.actual()['weight']
    underline = current_font.actual()['underline']
    # Toggle slant
    slant = 'italic' if current_font.actual()['slant'] == 'roman' else 'roman'
    # Apply updated font
    textArea.config(font=(family, size, weight, slant))
    textArea['font'] = font.Font(family=family, size=size, weight=weight, slant=slant, underline=underline)

#function to Underline
def underline_text():
    current_font = font.Font(font=textArea['font'])
    # Get current font attributes
    family = current_font.actual()['family']
    size = current_font.actual()['size']
    weight = current_font.actual()['weight']
    slant = current_font.actual()['slant']  
    # Toggle underline
    underline = 1 if current_font.actual()['underline'] == 0 else 0
    # Apply updated font
    textArea.config(font=(family, size, weight, slant))
    textArea['font'] = font.Font(family=family, size=size, weight=weight, slant=slant, underline=underline)

# function to change the text color
def color_text():
    colorChose = colorchooser.askcolor()
    textArea.config(fg=colorChose[1])

#funtions for Alignment
def text_right():
    area = textArea.get("0.0", END)  # Correct start and end positions
    textArea.tag_config('right', justify=RIGHT)
    textArea.delete("0.0", END)  # Correct delete positions
    textArea.insert("0.0", area, 'right')  # Correct insert position
def align_left():
    area = textArea.get("0.0", END)  # Correct start and end positions
    textArea.tag_config('left', justify=LEFT)
    textArea.delete("0.0", END)  # Correct delete positions
    textArea.insert("0.0", area, 'left')  # Correct insert position
def align_center():
    area = textArea.get("0.0", END)  # Correct start and end positions
    textArea.tag_config('center', justify=CENTER)
    textArea.delete("0.0", END)  # Correct delete positions
    textArea.insert("0.0", area, 'center')  # Correct insert position

#functions of main bar ------------------------------------------------------------------------>
def open_file():
    global url
    url = filedialog.askopenfile(
        initialdir=os.getcwd(),
        title='Select File',
        filetypes=(('Text File', '*.txt'), ('All Files', '*.*'))
    )
    if url: 
        textArea.insert(0.0, url.read()) 
        root.title(os.path.basename(url.name))  # Use url.name for the file path
        url.close()

def new_file():
    textArea.delete(0.0,END)

def save_file():
    global url
    if not url:  # If no file is selected yet
        save_as_file()
    else:
        try:
            content = textArea.get("1.0", END)
            with open(url, 'w') as file:
                file.write(content)
            messagebox.showinfo("Save Successful", f"File saved successfully at {url}")
        except Exception as e:
            messagebox.showerror("Save Error", f"Error saving file: {e}")

def save_as_file():
    global url
    content = textArea.get("1.0", END)  # Get all content from text area
    lines = content.splitlines()  # Split content into individual lines
    
    

    # Insert each line into the BST
    for line in lines:
        bst.insert(line)

    # Get the sorted lines from the BST using in-order traversal
    sorted_lines = bst.in_order()

    # Open Save As dialog and choose new file location
    save_as_url = filedialog.asksaveasfile(mode='w', defaultextension='.txt', filetypes=(('Text File', '*.txt'), ('All Files', '*.*')))
    
    if save_as_url:  # Ensure the user selected a file
        try:
            # Write the sorted lines to the new file
            with open(save_as_url.name, 'w') as file:
                for line in sorted_lines:
                    file.write(line + "\n")
            # Update the title of the window to the new file's name
            root.title(f"Text Editor - {os.path.basename(save_as_url.name)}")
            messagebox.showinfo("Save Successful", f"File saved successfully at {save_as_url.name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save the file: {e}")
    else:
        messagebox.showwarning("No file selected", "No file selected for saving.")

def exit():
    if textArea.edit_modified():  # Check if the content has changed
        response = messagebox.askyesnocancel("Unsaved Changes", "You have unsaved changes. Do you want to save them?")
        if response == True:  # Yes, save the file
            save_file()
        elif response == False:  # No, discard changes
            root.quit()
    else:
        root.quit()

#_______________________________________________>

def statusBarFunction(event):
        if textArea.edit_modified():
            current_text = textArea.get("1.0", 'end-1c')  # Current content of the text area

            # Push only if the undo stack is empty or the last state differs from current
            if not undo_stack or undo_stack[-1] != current_text:
                undo_stack.append(current_text)
            
            # Clear redo stack when a new action happens
            # redo_stack.clear()

            # Update status bar
            word_count = len(current_text.split())
            character_count = len(current_text.replace(' ', ''))
            statusBar.config(text=f"Characters: {character_count} Words: {word_count}")

            # Reset modification tracker
            textArea.edit_modified(False)

def undo_action(event=None):
    """Perform undo operation."""
    if undo_stack:
        redo_stack.append(undo_stack.pop())
        if undo_stack:
            textArea.delete("1.0", END)
            textArea.insert("1.0", undo_stack[-1])
            # status_label.config(text="Undone last action.")
        else:
            textArea.delete("1.0", END)
            # status_label.config(text="Undo stack empty.")
    # else:
        # status_label.conf/ig(text="Nothing to undo.")

def redo_action(event=None):
    """Perform redo operation."""
    # print (redo_stack)
    if redo_stack:
        # Print current redo stack for debugging
        # print("[DEBUG] Redo stack before pop:", redo_stack)
        
        # Perform redo operation
        state = redo_stack.pop()
        undo_stack.append(state)
        textArea.delete("1.0", END)
        textArea.insert("1.0", state)
        
        # Print the state after redo
        # print("[DEBUG] Redo stack after pop:", redo_stack)
        # print("[DEBUG] Undo stack after push:", undo_stack)
    # else:
    #     print("nothing")
        # Update status label
    #     status_label.config(text="Redone last action.")
    # else:
    #     status_label.config(text="Nothing to redo.")

def find_text(bst, text_widget):
    def search():
        find_data = find_entry_field.get()

        # Debugging: Check the value entered
        print(f"Searching for: {find_data}")

        # Ensure input is not empty
        if not find_data:
            messagebox.showerror("Error", "Please enter a valid search term.")
            return

        # Search for the term in the BST using the correct method
        found = bst.find(find_data)
        print(f"Found in BST: {found}")

        if found:
            # Highlight occurrences in the text widget
            text_widget.tag_remove("highlight", "1.0", END)
            start = "1.0"
            while True:
                start = text_widget.search(find_data, start, stopindex=END)
                if not start:
                    break
                end = f"{start}+{len(find_data)}c"
                text_widget.tag_add("highlight", start, end)
                text_widget.tag_config("highlight", background="yellow")
                start = end
            messagebox.showinfo("Result", f"'{find_data}' found and highlighted.")
        else:
            text_widget.tag_remove("highlight", "1.0", END)
            messagebox.showinfo("Result", f"'{find_data}' not found in the text.")

    # Create the search window
    root2 = Toplevel()
    root2.geometry('400x150+500+200')
    root2.resizable(0, 0)
    label_frame = LabelFrame(root2, text='Find')
    label_frame.pack(pady=20)

    # find_label = Label(label_frame, text='Find')
    # find_label.grid(row=0, column=0, padx=5, pady=5)
    find_entry_field = Entry(label_frame)  # Ensure this is properly defined
    find_entry_field.grid(row=0, column=1, padx=5, pady=5)

    # Add button for "Search"
    search_button = Button(label_frame, text="Search", command=search)
    search_button.grid(row=0, column=2, padx=10)

    # Set focus to the entry field for better UX
    find_entry_field.focus()

def status_Bar():
    if show_status_bar.get() == False:
        statusBar.pack_forget()
    if show_status_bar.get() == True:
        # textArea.pack_forget()
        statusBar.pack()
        textArea.pack(fill=BOTH, expand=1)

def toolBar():
    if show_toolbar.get()== False:
        tool_bar.pack_forget()
    if show_toolbar.get()== True:
        textArea.pack_forget()
        tool_bar.pack(fill=X)
        textArea.pack(fill=BOTH,expand=1)

def theme_change(bg_color,fg_color):
    textArea.config(bg=bg_color,fg=fg_color)

def printOut(event=None):
    file = tempfile.mktemp('.txt')
    open(file, 'w').write(textArea.get(1.0,END))
    os.startfile(file,'print')

def select_all(event=None):
    textArea.tag_add("sel", "1.0", "end-1c")  # Select all the text
    textArea.mark_set("insert", "end-1c")  # Move the insertion point to the end
    textArea.see("insert")  # Scroll to the insertion point (optional)

def delete_all(event=None):
    textArea.delete("1.0", "end-1c")  # Delete all text from the Text widget

def insert_datetime(event=None):
    # Get the current date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Insert the date and time at the current cursor position in the text area
    textArea.insert(tk.INSERT, current_datetime)

#file Menu Adjustments 
filemenu = Menu(menuBar,tearoff=False)
menuBar.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label='New',accelerator='Ctrl+N',image=newImage,compound=LEFT,command=new_file)
filemenu.add_command(label='Open',accelerator='Ctrl+O',image=openImage,compound=LEFT,command=open_file)
filemenu.add_command(label='Save',accelerator='Ctrl+S',image=saveImage,compound=LEFT,command=save_file)
filemenu.add_command(label='Save As',accelerator='Ctrl+Alt+S',image=saveAs_Image,compound=LEFT,command=save_as_file)
filemenu.add_command(label='Print',accelerator='Ctrl+P',image=print_img,compound=LEFT,command=printOut)
filemenu.add_command(label='Date_Time',accelerator='Ctrl+D',image=datetime_img,compound=LEFT,command=insert_datetime)
filemenu.add_separator()
filemenu.add_command(label='Exit',accelerator='Ctrl+Q',image=exitImage,compound=LEFT,command=exit)

#Edit Menu Adjustments
editmenu = Menu(menuBar,tearoff=False)
menuBar.add_cascade(label='Edit',menu=editmenu)
editmenu.add_command(label='Cut',accelerator='Ctrl+X',image=cutImage,compound=LEFT)
editmenu.add_command(label='Copy',accelerator='Ctrl+C',image=copyImage,compound=LEFT)
editmenu.add_command(label='Paste',accelerator='Ctrl+P',image=pasteImage,compound=LEFT)
editmenu.add_separator()
editmenu.add_command(label='Select All',accelerator='Ctrl+A',image=selectImage,compound=LEFT,command=select_all)
editmenu.add_command(label='Clear',accelerator='Ctrl+Alt+X',image=clearImage,compound=LEFT)
editmenu.add_command(label='Find',accelerator='Ctrl+F',image=findImage,compound=LEFT, command=lambda: find_text(bst,textArea))
editmenu.add_separator()
editmenu.add_command(label='Undo',accelerator='Ctrl+Z',image=undoImage,compound=LEFT,command=undo_action)
editmenu.add_command(label='Redo',accelerator='Ctrl+Y',image=redoImage,compound=LEFT,command=redo_action)

#view menu Adjustmensts
show_toolbar = BooleanVar(value=True)
show_status_bar = BooleanVar(value=True)

view_menu = Menu(menuBar,tearoff=False)
menuBar.add_cascade(label='View',menu=view_menu)

view_menu.add_checkbutton(label='Tool Bar',variable=show_toolbar,onvalue=True,offvalue=False,image=toolImage,compound=LEFT,command=toolBar)

view_menu.add_checkbutton(label='Status Bar',variable=show_status_bar,onvalue=True,offvalue=False,image=statusImage,compound=LEFT,command=status_Bar)


#Theme Menu Adjustements
theme_Choice = StringVar()
theme_menu = Menu(menuBar,tearoff=False)
menuBar.add_cascade(label='Theme',menu=theme_menu)

theme_menu.add_radiobutton(label='Default Light',image=D_LightImage,variable=theme_Choice,compound=LEFT, command=lambda:theme_change("white","black"))
theme_menu.add_radiobutton(label='Pluse Light',variable=theme_Choice,image=P_lightImage,compound=LEFT, command=lambda:theme_change("slate gray","white"))
theme_menu.add_radiobutton(label='Monokai',image=monokaiImage,compound=LEFT,variable=theme_Choice, command=lambda:theme_change("navajo white","black"))
theme_menu.add_radiobutton(label='Night Blue',image=blueImage,compound=LEFT,variable=theme_Choice, command=lambda:theme_change("cornflower blue","white"))
theme_menu.add_radiobutton(label='Red',image=redImage,compound=LEFT,variable=theme_Choice, command=lambda:theme_change("pink","blue"))
theme_menu.add_radiobutton(label='Dark',image=darkImage,compound=LEFT,variable=theme_Choice, command=lambda:theme_change("gray20","white"))

#tool bar
tool_bar = Label(root)
tool_bar.pack(side=TOP,fill=X)
#font family

font_family_variable = StringVar()
fontFamily_comboBox = Combobox(tool_bar,width=30,values=font.families(),state='readonly',textvariable=font_family_variable)
fontFamily_comboBox.current(font.families().index('Arial'))
fontFamily_comboBox.grid(row=0,column=0,padx=5)
fontFamily_comboBox.bind('<<ComboboxSelected>>',font_style)
#font size

size_variable=StringVar() 
font_size_comboBox = Combobox(tool_bar,width=14,textvariable=size_variable,state='readonly',values=tuple(range(8,80)))
font_size_comboBox.current(4)
font_size_comboBox.grid(row=0,column=1,padx=5)
font_size_comboBox.bind('<<ComboboxSelected>>',font_size)
#bold button
boldbtn = Button(tool_bar,image=boldImage,command=bold_text)
boldbtn.grid(row=0,column=2,padx=5)
#italic button
italicbtn = Button(tool_bar,image=italicImage,command=italic_text)
italicbtn.grid(row=0,column=3,padx=5)
#underline button
underlinebtn = Button(tool_bar,image=underlineImage,command=underline_text)
underlinebtn.grid(row=0,column=4,padx=5)
#font color
font_colorbtn = Button(tool_bar,image=font_colorImage,command=color_text)
font_colorbtn.grid(row=0,column=5,padx=5)
#alignments
leftbtn = Button(tool_bar,image=leftImage,command=align_left)
leftbtn.grid(row=0,column=6,padx=5) 

rightbtn = Button(tool_bar,image=rightImage,command=text_right)
rightbtn.grid(row=0,column=7,padx=5)

centerbtn = Button(tool_bar,image=centerImage,command=align_center)
centerbtn.grid(row=0,column=8,padx=5)

#scrool bar
scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT,fill=Y)

#text Area
textArea = Text(root,wrap='word', undo=True,yscrollcommand= scrollbar.set,font=('arial',12))
textArea.pack(fill=BOTH,expand=True)
scrollbar.config(command=textArea.yview)

#status bar
statusBar = Label(root,text='Status Bar')
statusBar.pack(side=BOTTOM)
textArea.bind("<KeyPress>", insert_into_bst)
textArea.bind("<<Modified>>", statusBarFunction)

# Binding accelerator keys
root.bind('<Control-n>', lambda event: new_file())   # Ctrl+N for new file
root.bind('<Control-o>', lambda event: open_file())  # Ctrl+O for open file
root.bind('<Control-s>', lambda event: save_file())  # Ctrl+S for save file
root.bind('<Control-Alt-s>', lambda event: save_as_file())  # Ctrl+Alt+S for save as file
root.bind('<Control-q>', lambda event: exit())       # Ctrl+Q for exit
root.bind('<Control-z>', lambda event: undo_action())
root.bind('<Control-y>', lambda event: redo_action())
root.bind('<Control-f>', lambda event: find_text(bst,textArea))
root.bind('<Control-p>', lambda event: printOut())
root.bind("<Control-a>", select_all)
root.bind("<Control-Alt-x>", delete_all)
root.bind("<Control-d>", insert_datetime)

if __name__ == "__main__":
    root = tk.Tk()  # This is where you start your Tkinter app (unchanged)
    app = TextEditorApp(root, text_editor_graph)  # Pass the graph object to the app
    bst = BST()
    root.mainloop()  # Main loop