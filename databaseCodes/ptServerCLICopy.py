#! /usr/intel/bin/python3.10.8
import sys
sys.path.append('/nfs/site/disks/vmisd_vclp_efficiency/rcg/server/fullServer/venvRcg/lib/python3.11/site-packages')
import typer
import typer
import readline
import optparse
import readline

# Define a dictionary to store the commands and their options
commands = {}

app = typer.Typer()

# Function to add a new command
def add_command(command_name, function, options=[]):
    commands[command_name] = {'function': function, 'options': options}

# Function to run a command
def run_command(command, option=None):
    if command in commands:
        function_info = commands[command]
        function = function_info['function']
        options = function_info['options']
        if options and option is None:
            print("Options available:", options)
            user_input = input("Enter option: ")
            if user_input in options:
                option = user_input
            else:
                print("Invalid option")
                return
        function(option)
    else:
        print("Command not found")

# Example functions
def greet(option=None):
    print("Hello", option or "there!")

def farewell(option=None):
    print("Goodbye", option or "!")



# Add example commands
add_command("hello", greet)
add_command("bye", farewell)
add_command("add", add)
add_command("sub", subtract)

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
if __name__ == "__main__":
    while True:
        user_input = input("Enter a command: ")
        if user_input.lower() == "exit":
            break
        else:
            parts = user_input.split()
            command = parts[0].lower()
            option = parts[1] if len(parts) > 1 else None
            run_command(command, option)
