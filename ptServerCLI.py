#! /usr/intel/bin/python3.10.8
import sys
sys.path.append('/nfs/site/disks/vmisd_vclp_efficiency/rcg/server/fullServer/venvRcg/lib/python3.11/site-packages')
import typer
from rich.console import Console
from rich.prompt import Prompt
from timingCommands import *

from ptServerDatabasemysql import setupDatabase

import readline
import optparse
import readline
import globalVariable
import datetime
import re

# Define a dictionary to store the commands and their options
commands = {}

# Function to add a new command
def add_command(command_name, function, options=[], helpM=""):
    commands[command_name] = {'function': function, 'options': options, 'helpM': helpM}

# Function to run a command
def run_command(command, option=None):
    if command in commands:
        function_info = commands[command]
        function = function_info['function']
        options = function_info['options']

        help = function_info['helpM']
        if options and option is None:
            print("Help\n", help)
            print("Options available:", options)
            if globalVariable.guiMode == 0:
                user_input = input("Enter option: ")
                if user_input in options:
                    option = user_input
                else:
                    print("Invalid option")
                #return
        function(option)
    else:
        print("Command not found")




def start_gui(option=None):
    import tkinter as tk
    import subprocess
    import threading
    import queue

    globalVariable.guiMode = 1
    class TerminalApp:
        def change_button_color(self, event, idx, buttons):
            button = event.widget
            for buts in buttons:
                buts.configure(bg="light grey")
            button.configure(bg="green")  # Change color to green when clicked

        def destroyMaster(self):
            globalVariable.guiMode = 0
            self.master.destroy()
        
        def generateOutput(self, event):
            print(self.entry_widget.get())
            parts = self.entry_widget.get().split()
            command = parts[0].lower()
            option = ' '.join(parts[1:]) if len(parts) > 1 else None
            self.text_widget.insert(tk.END, " empty ")
            self.text_widget.delete("1.0", tk.END)
            run_command(command, option)
            #code.interact(local=locals())
            if globalVariable.tempLocation != "":
                with open(globalVariable.tempLocation, 'r') as file:
                    # Read the file line by line and print each line
                   for line in file:
                        self.text_widget.insert(tk.END, line)
            
        def __init__(self, master):
            self.master = master
            
            config = configparser.ConfigParser()
            project = globalVariable.project
            config.read(globalVariable.configFile)
            machineSetup = config[project]["machineSetup"]
            corners = []
            for cor in machineSetup.split("\n"):
                corners.append(cor.split(":")[0])


            # Add a row of buttons at the top
            workweek = getAllWorkWeek()
            self.workweek_buttons = []
            for i, day in enumerate(workweek):
                button = tk.Button(master, text=day, command=lambda day=day: load_work_week(day))
                button.grid(row=0, column=i+1, sticky="e")  # start from column 1
                button.bind("<Button-1>", lambda event, idx=i: self.change_button_color(event, idx, self.workweek_buttons))
                self.workweek_buttons.append(button)

            # Add a column of buttons on the left
            
            self.corner_buttons = []
            for i, corner in enumerate(corners):
                button = tk.Button(master, text=corner, command=lambda corner=corner: load_corner(corner))
                button.grid(row=i+1, column=0, sticky="n")  # stacked vertically
                button.bind("<Button-1>", lambda event, idx=i: self.change_button_color(event, idx, self.corner_buttons))
                self.corner_buttons.append(button)
                #self.corner_buttons = []

            button = tk.Button(master, text="exit", command=lambda corner=corner: self.destroyMaster())
            button.grid(row=i+1, column=0, ipady = 5, ipadx=50, sticky="s")  # stacked vertically

            # Text widget for displaying the output
            self.text_widget = tk.Text(self.master)
            self.text_widget.grid(row=1, column=1, rowspan=len(corners), columnspan=len(workweek), sticky='nsew')

            # Entry widget for inputting commands
            self.entry_widget = tk.Entry(self.master)

            self.entry_widget.bind("<Return>", self.generateOutput)
            self.entry_widget.grid(row=len(corners)+1, column=1, columnspan=len(workweek), sticky='ew')

            # Configure grid to expand properly when window is resized
            self.master.grid_rowconfigure(len(corners), weight=1)
            self.master.grid_columnconfigure(1, weight=1)

            # Create a queue to handle the output from the subprocess
            self.queue = queue.Queue()



        def display_output(self):
            self.entry_widget.delete(0, tk.END)
            self.text_widget.insert(tk.END, "checks")


    root = tk.Tk()
    app = TerminalApp(root)
    root.mainloop()


    print("starting the gui for ptServer")




# Add example commands
add_command("report_timing", report_timing, "-from -to -capacitance -transition " ,"use --help for options")
add_command("report_delay_calculation", report_delay_calculation, "-from -to -capacitance -transition ", "use --help for options")
add_command("man", man, "" ,"man for command")
add_command("exit", exit)
add_command("show_report", show_report, "" ,"location")

add_command("load_corner", load_corner, "corner", "")
add_command("show_corner", show_corner)
add_command("current_corner", current_corner)

add_command("set_var", set_var, "" , "set the variable")
add_command("start_gui", start_gui, "" , "start the gui")

add_command("get_cells", get_cells , "" , "get the cells")
add_command("get_pins", get_pins, "" , "get the pins")
add_command("get_lib_cells", get_lib_cells, "" , "get lib cells")
add_command("get_lib_pins", get_lib_pins, "" , "get lib pins")
add_command("get_object_name", get_object_name, "" , "get object name")

add_command("get_attributes", get_attributes, "" , "get attributes")
add_command("set_user_location", set_user_location, "" , "set the user location location to copy the data")
add_command("get_user_location", get_user_location, "", "get the user location")

add_command("load_work_week",load_work_week, "work_week","set the work week location")
add_command("show_work_week",show_work_week)
add_command("current_work_week",current_work_week)

# Define a function to handle tab completion
def completer(text, state):
    options = [cmd for cmd in commands.keys() if cmd.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None

# Set tab completion function
readline.set_completer(completer)
readline.parse_and_bind("tab: complete")

# Main loop
setupDatabase()
if __name__ == "__main__":
    console = Console()
    version = 1.0
    console.print("Welcome to ptServer\nVersion : ",version," \n\n\n", style="bold green")

    while True:
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%H:%M:%S")
        user_input = Prompt.ask("[bold cyan]"+formatted_time+" ptServer>[/bold cyan]")

        if user_input == "":
            print("enter command")
            continue
        if user_input.lower() == "exit":
            print ("exiting PTServer\nThanks for using PTServer")
            break
        if user_input.lower().startswith("source"):
            match = re.match(r"source\s*(.*)", user_input)
            fileSource = match.group(1)
            print(fileSource)
            try:
                with open(fileSource, 'r') as file:
                    for line in file:
                        print(line.strip())
                        parts = line.split()
                        command = parts[0].lower()
                        option = ' '.join(parts[1:]) if len(parts) > 1 else None
                        print("command: ",command)
                        print("option: ",option)
                        run_command(command, option)
            except FileNotFoundError:
                print("The file does not exist.")
            except Exception as e:
                print("An error occurred:", e)

        else:
            parts = user_input.split()
            command = parts[0].lower()
            option = ' '.join(parts[1:]) if len(parts) > 1 else None
            print("command: ",command)
            print("option: ",option)
            run_command(command, option)            

