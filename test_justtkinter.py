import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename, Menu
from tkinter import ttk
import threading
from pygame_win_class import pygameWin ######new
import numpy as np
import random
from calculator import priority, add, multiply, divide, subtract, power
#import numpy
###work through linear algebra - 3d vectors

def open_file():
    ###### setting the current data to a Null value
    global linkedList
    linkedList = []
    faces = []
    ######
    """Open a file for editing."""
    filepath = askopenfilename(
        filetypes=[("obj code", "*.obj"),
                   ("All Files", "*.*")]
    )###can include other file types
    if not filepath:
        return
    ###deleting the current displayed data
    txt_edit.delete(1.0, tk.END)
    ###opening the file from the filepath
    with open(filepath, "r") as input_file:
        text = input_file.read()
        txt_edit.insert(tk.END, text)
    ###converting the data to a usable format
    load(text)
    ###letting the title be the new filepath
    window.title(f"Welcome to Donut_3D - {filepath}")

def save_file():
    """Save the current file as a new file."""
    filepath = asksaveasfilename(
        defaultextension="obj",
        filetypes=[("obj code", "*.obj"), ("All Files", "*.*")],
    )
    if not filepath:
        return
    with open(filepath, "w") as output_file:
        text = txt_edit.get(1.0, tk.END)
        output_file.write(text) ##outputs what is inside of the text box
    ###letting the title be the new filepath
    window.title(f"Welcome to Donut_3D - {filepath}")


def _export_(): ###the same code used for saving just saving the points data set
    """Save the current file as a new file."""
    filepath = asksaveasfilename(
        defaultextension="obj",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
    )
    if not filepath:
        return
    with open(filepath, "w") as output_file:
        text = linkedList
        output_file.write(text)
    window.title(f"Welcome to Donut_3D - {filepath}")
    
def _import_():
    ###### globalising the variables used
    global linkedList
    linkedList = []
    ######
    """Open a file for editing."""
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.obj"),
                   ("All Files", "*.*")]
    )
    if not filepath:
        return
    txt_edit.delete(1.0, tk.END)  ##deletes whats already displayed
    with open(filepath, "r") as input_file:
        linkedList = input_file.read()  ##saves the linked list
        txt_edit.insert(tk.END, linkedList)
        window.title(f"Welcome to Donut_3D - {filepath}")
    ###consider if the file isnt in obj format

def run(): ###running terminal commands
    "runs the code in the terminal"
    global program_counter ###globalises the program counter - which line of code to run- because it is incrimented
    text = txt_terminal.get(program_counter, tk.END) ###gets the text from the terminal
    text.strip("\n")  ###input sanitisation
    ###input handling -- needs to be in the format [instruction, (executable info)] where executable info is everything past instruction
    check_comm = text.split(" ")
    ###came across an error with single line could use Null value identifiers
    if text == "clear\n":
        instruction_set["clear"]()
    else:
        ##reference to the instruction set dictionary
        instruction_set[check_comm[0].strip("\n")](check_comm[1:]) 
    ###increments the program counter
    program_counter += 1

###command line - improves usability of the menu to edit 3D files
def link(executable: int) -> int:##in the form [index -> connected index]
##    try:
    if executable[0] == "all\n": ##connects every point to every other point runs in O(n^2) but could be O(n!)
        for i in range(len(linkedList)):
            for x in range(i,len(linkedList)):
               linkedList[i][3].append(x)
    elif executable[0] == "snake\n":
        for i in range(1, len(linkedList)):
            linkedList[i-1][3].append(i)
        
    else:
        temp = linkedList[int(executable[0])] ##links executable[0] to executable[1]
        linkedList[int(executable[0])][3].append(int(executable[1]))


##sets the zoom variable
def zoom_in(executable):
    global zoom
    zoom = int(executable[0])

def func(executable): ##runs from 0 -> executable[0]
    global linkedList
##    for i in range(-int(executable[0]),int(executable[0]),0.2):
##        xP, zP = 0,0
##        if "x" in execute:
##            execute = execute.replace("x",str(i))
####                zP = 0
##            xP = i
##        if "z" in execute:
##            execute = execute.replace("z",str(i))
##            zP = i
##        func = execute.strip("\n")
##        linkedList.append([xP,float(priority(func)),zP,[],[]])

        
    for i in range(int(executable[0])): ##always assumes y = executable as a function of x and z
        for x in range(10): ##runs from 0 - 1
            execute = executable[1]
##            xP,zP = (x/10)+i,(x/10)+i
            xP, zP = 0,0
            if "x" in execute:
                execute = execute.replace("x",str(i+(x/10)))
##                zP = 0
                xP = (x/10)+i
            if "z" in execute:
                execute = execute.replace("z",str(i+(x/10)))
                zP = (x/10)+i
            func = execute.strip("\n")
            linkedList.append([xP,float(priority(func)),zP,[],[]])

    update()

            
##executable 0 1 2 will be either coordinate points or vertex indexes
##None -> command line  1 -> vertex  2 -> face
def make(executable, type_of = None) -> int:                                                                                                                            ##maybe use argument functions for unpacking command lines
    if type_of == None and executable[0] == "box":
        length = float(executable[1])
        ###make the box
        linkedList.append([0,0,0,[],[]])
        linkedList.append([length,0,0,[],[]])
        linkedList.append([0,length,0,[],[]])
        linkedList.append([0,0,length,[],[]])
        linkedList.append([length,length,0,[],[]])
        linkedList.append([0,length,length,[],[]])
        linkedList.append([length,0,length,[],[]])
        linkedList.append([length,length,length,[],[]])
        update()
                                                                                                                                                                                ##    elif type_of == None and executable[0] == "plane": ###make a polyglon plane
                                                                                                                                                                                ##        make([0,0,0])
                                                                                                                                                                                ##        make([executable[1],0,0])                                                                                                                                                   ##        make([0,0,executable[1                                                                                                                                                                        ##        make([executable[1],0,executable[1]])
                                                                                                                                                                                ##        faces.append()
                
    elif type_of == None: ##incase the make command line is used in the terminal
        x,y,z = float(executable[0]),float(executable[1]),float(executable[2])
        linkedList.append([x,y,z,[],[]])
        update() ##adds to the linked list and updates what is displayed
    elif type_of == 1: ##displays a vertex on the text box
        x,y,z = executable
        insert = f"v {x} {y} {z}\n" 
        txt_edit.insert(tk.END, insert)         
    elif type_of == 2: ##if a face needs to be displayed
        v1,v2,v3 = executable
        insert = f"f {v1}// {v2}// {v3}//\n"
        txt_edit.insert(tk.END, insert)        

##clears all data points
def clear():
    global linkedList
    ##resetting all the data types
    linkedList = []
    faces = []
    update()
    
def load(executable): ###called after the open file to ensure correct upload of data
    ##consider os path, vertices, normals connections etc
    ##takes file data and splits it with \n
    global faces
    target_lis = executable.split("\n")
    for i in range(len(target_lis)):
        a = target_lis[i].split(" ")                                                                                                                                    ##consider error handling because this is not very robust
        if a[0] == "v":
            linkedList.append([float(a[1]),float(a[2]),float(a[3]),[]])                                                                                                 ##the easiest way is to make it int()
            ###if keyword v is found then add a new vertex to the linkedList                                                                                                        ##        elif a[0] == "vn":
            ###shoule be in float format to be inclusive of precise points                                                                                                        ##            print("not done") #####find out what to do
        elif a[0] == "f":                                                                                                                                               ##i should use private indexing because of how line 1 is 1 now 0 like in python
            ###appending the correct relational key to each vertex found in a face of assumed 3 vertices                                                                                                    ##going to have to make this face interpretation
            ###also appends to a test face variable                                                                                                                         ##assumes no normals ###needs to consider faces with more than 3 vertices
            linkedList[int(a[1].split("/")[0])-1][3].append(int(a[2].split("/")[0])-1)
            linkedList[int(a[1].split("/")[0])-1][3].append(int(a[3].split("/")[0])-1)
            linkedList[int(a[2].split("/")[0])-1][3].append(int(a[3].split("/")[0])-1)
            faces.append([int(a[1].split("/")[0])-1,int(a[2].split("/")[0])-1,int(a[3].split("/")[0])-1])

def lda_win():  ###function called to load the 3D visualiser
    global winOn ###using the variables that need to be parsed into the visualiser
    global visualiser_instance
    global linkedList                                                                                                                                                               #####temp storage variable of the points made with the graph
    global zoom
    global faces
    global is_axis_on
    global axis_faces
    ###making an instance of the 3D visualiser
    pygameWin_zero = pygameWin(linkedList, zoom, faces,is_axis_on,axis_faces)                                                                                                       ####add the zoom_factor varible and make self.zoom_factor - saves a lot of storage space
    if winOn == False:  ###if the window is not already running
        visualiser_instance = threading.Thread(target=pygameWin_zero.runalgo()) ###defining the thread
        visualiser_instance.run() ###running the thread
        winOn == True ##letting the menu know that the 3D visualiser code is running
        if pygameWin_zero.changes == True: ###if any changes are detected in te 3D visualiser
            linkedList = pygameWin_zero.points ###let the linked list vertices == the vertices data in the visualiser
            faces = pygameWin_zero.faces  ###let the faces list be equal to the faces list in the visualiser
            zoom = pygameWin_zero.zoom_factor ###keep the zoom scale constant
            update() ###update the displayed OBJ file
    else:
        terminal.insert(tk.END, "already open")   ##error handling


def update():  ##runs the make function and then adds the connecting line segments and stuff
    global linkedList                                                                                                                                           ####i need to optimise the functions
    global faces
    txt_edit.delete(1.0, tk.END) ####deletes whats already in the file
    txt_edit.insert(tk.END, "##updated with donut-3d\n")
    for i in range(len(linkedList)): ##the function has to iterate through the whole data set                                                                   ##if i use argument functions to unpack i dont need to specify the indexes
        make(linkedList[i][0:3],1)   ##displays the data in the text box                                                                                                ##make linkedList[i]
    if faces != None:                ##also displays faces
        for i in range(len(faces)):
            make(faces[i],2)         ##appends to the faces part of the list

    ###now do the same for the vertex normal as well as the links

##determines if the 3d axis should be on
def axis_on(executable):
    global is_axis_on
    if executable[0] == "True":
        is_axis_on = True
    elif executable[0] == "False":
        is_axis_on = False

##are the faces displayed or the individual vertices
def axis_faces_func(executable):
    global axis_faces
    if executable[0] == "True":
        axis_faces = True
    elif executable[0] == "False":
        axis_faces = False

def random_gen(executable): ###add a range too
    for i in range(int(executable[0])):
        make([random.randint(0,10),random.randint(0,10),random.randint(0,10)]) ##this is why make should unpack##

instruction_set = {"link": link,  
                   "make":make,
                   "clear":clear,
                   "zoom":zoom_in,
                   "axis_on": axis_on,
                   "axis_faces": axis_faces_func,
                   "random":random_gen,
                   "func":func} 


linkedList = []
faces = []

program_counter = 1.0
winOn = False
zoom = 1 ###zoom scares me now
is_axis_on = True
axis_faces = False

window = tk.Tk()
window.title("Welcome to Donut_3D")
window.rowconfigure(1, minsize=20, weight=1)
window.columnconfigure(1, minsize=20, weight=1)
##window.rowconfigure(1, minsize=800, weight=1)
##window.columnconfigure(1, minsize=800, weight=2)

# create a menubar
menubar = Menu(window)
window.config(menu=menubar)
# create the file_menu

file_menu = Menu(
    menubar,
    tearoff=0
)

# add menu items to the File menu
file_menu.add_command(label='Save', command=save_file)
file_menu.add_command(label='Open...', command=open_file)
file_menu.add_command(label='load view window', command=lda_win)
file_menu.add_command(label='import', command=_import_)
file_menu.add_command(label='export', command=_export_)
file_menu.add_command(label='Close')
file_menu.add_separator()

# add Exit menu item
file_menu.add_command(
    label='Exit',
    command=window.destroy
)

# add the File menu to the menubar
menubar.add_cascade(
    label="File",
    menu=file_menu
)

# create the Help menu
help_menu = Menu(
    menubar,
    tearoff=0
)

help_menu.add_command(label='Welcome')
help_menu.add_command(label='About...')

# add the Help menu to the menubar
menubar.add_cascade(
    label="Help",
    menu=help_menu
)

options = tk.Frame(window)
n = tk.StringVar()
format_type = ttk.Combobox(options, width = 27, textvariable = n)

# Adding combobox drop down list
format_type['values'] = ('OBJ')


options.grid(row=0, sticky="nsew")
format_type.grid(column = 0, row = 0)

##positioning the buttons
##fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
btn_run = tk.Button(options, text="run", command=run, width = 27)
btn_run.grid(row=0, column=1, sticky="ew")#, padx=5, pady=5)


textboxes = tk.Frame(window)
txt_edit = tk.Text(textboxes, height = 50, width = 120)
txt_terminal = tk.Text(textboxes, height = 30, width = 100)

textboxes.grid(row = 1,column = 0, columnspan = 2, sticky = "nsew")
txt_edit.grid(row=0, column=0, sticky="nsew")##, columnspan = 1
txt_terminal.grid(row=0, column=1, sticky="nsew")


thread_1 = threading.Thread(target=window.mainloop())
thread_1.start()


thread_1.join()
##visualiser_instance.join()###not accounted for as the program cuts itself off

###its a class that runs itself after setting the parameters
##fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
##btn_run = tk.Button(fr_buttons, text="run", command=run)
##fr_buttons.grid(row=0, column=0, sticky="ns")
##btn_run.grid(row=2, column=0, sticky="ew", padx=5, pady=5)


######everything under the buttons frame
##btn_open = tk.Button(fr_buttons, text="Open", command=open_file)
##btn_save = tk.Button(fr_buttons, text="Save As...", command=save_file)
##btn_change = tk.Button(fr_buttons, text="change", command=change)

##btn_win = tk.Button(fr_buttons, text="lda_win", command=lda_win)##pywin
##btn_win.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
##btn_change.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

##btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
##btn_save.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
