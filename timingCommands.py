
from ptServerDatabasemysql import *
import globalVariable
from rich import print
import shutil
import datetime
import re
from rich.console import Console
from rich.table import Table

from log_config import get_client_logger

client_logger = get_client_logger()

def log_performance(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        client_logger.debug(f"{func.__name__} executed in {end_time - start_time:.4f} seconds")
        return result
    return wrapper

@log_performance
def get_cells (parser):
    print("get_cells cells ",globalVariable.corner)
    if parser == None:
        command = "get_cells "
    else:
        command = "get_cells "+ parser
    commandId = writeToCommandInputTable(command)
    client_logger.info("Please wait for command to be serviced")

    location = None
    while location == None:
        location = getCompleteFromCommandInputTable(commandId)
        client_logger.info(f"Report generated in location {location}")
        globalVariable.tempLocation = location
    show_report(location)

@log_performance
def get_pins (parser):
    print("get_pins of cells ",globalVariable.corner)
    if parser == None:
        command = "get_pins "
    else:
        command = "get_pins "+ parser
    commandId = writeToCommandInputTable(command)
    client_logger.info("Please wait for command to be serviced")
    location = None
    while location == None:
        location = getCompleteFromCommandInputTable(commandId)
        client_logger.info(f"Report generated in location {location}")
        globalVariable.tempLocation = location
    show_report(location)

@log_performance
def get_lib_cells (parser):
    print("get_lib_cells of cells ",globalVariable.corner)
    if parser == None:
        command = "get_lib_cells "
    else:
        command = "get_lib_cells "+ parser

    commandId = writeToCommandInputTable(command)
    client_logger.info("Please wait for command to be serviced")
    location = None
    while location == None:
        location = getCompleteFromCommandInputTable(commandId)
        client_logger.info(f"Report generated in location {location}")
        globalVariable.tempLocation = location
    show_report(location)

@log_performance
def get_lib_pins (parser):
    print("get_lib_pins of cells ",globalVariable.corner)
    if parser == None:
        command = "get_lib_pins "
    else:
        command = "get_lib_pins "+ parser

    commandId = writeToCommandInputTable(command)
       
    print("please wait for the command to be serviced")
    location = None
    while location == None:
        location = getCompleteFromCommandInputTable(commandId)
        client_logger.info(f"Report generated in location {location}")
        globalVariable.tempLocation = location
    show_report(location)

@log_performance
def get_object_name (parser):
    print("get_object_name -of cells ",globalVariable.corner)
    if parser == None:
        command = "get_object_name "
    else:
        command = "get_object_name "+ parser
    commandId = writeToCommandInputTable(command)
    client_logger.info("Please wait for command to be serviced")
    location = None
    while location == None:
        location = getCompleteFromCommandInputTable(commandId)
        client_logger.info(f"Report generated in location {location}")
        globalVariable.tempLocation = location
    show_report(location)

@log_performance
def get_attributes (parser):
    print("get_attributes -of ",globalVariable.corner)
    if parser == None:
        command = "get_attributes "
    else:
        command = "get_attributes "+ parser
    commandId = writeToCommandInputTable(command)
    client_logger.info("Please wait for command to be serviced")
    location = None
    while location == None:
        location = getCompleteFromCommandInputTable(commandId)
        client_logger.info(f"Report generated in location {location}")
        globalVariable.tempLocation = location
    show_report(location)

@log_performance
def report_timing(parser):
    client_logger.debug("currner corner for generating timing report "+globalVariable.corner)
    if "report_timing " in parser:
        parser = re.sub(r"report_timing "," ",parser)

    if parser == None:
        command = "report_timing "
    else:
        command = "report_timing "+ parser

    commandId = writeToCommandInputTable(command)
    client_logger.info("Please wait for command to be serviced")
    #code.interact(local=locals())
    location = None
    completCommandStart = datetime.datetime.now()
    while location == None:
        #print("time: ",datetime.datetime.now())
        location = getCompleteFromCommandInputTable(commandId)
        client_logger.debug(f"Report generated in location {location}")
        globalVariable.tempLocation = location
    show_report(location)
    return(commandId)



@log_performance
def report_delay_calculation(parser):
    print("current corner for generating timing report ",globalVariable.corner)
    if parser == None:
        print ("incorrect options")
        command = "report_delay_calculation "
    else : 
        command = "report_delay_calculation "+ parser

    commandId = writeToCommandInputTable(command)
    client_logger.info("Please wait for command to be serviced")
    location = None
    while location == None:
        location = getCompleteFromCommandInputTable(commandId)
        client_logger.info(f"Report generated in location {location}")
        globalVariable.tempLocation = location
    show_report(location)

@log_performance
def set_var(parser):
    print("set variable ",globalVariable.corner)
    command = "set "+ parser
    variableName = parser.split(" ")[0]
    user = os.environ['USER']
    variableValue = command
    commandId = writeToCommandInputTable(command)
    mySql = (variableName,user,variableValue)
    writeToUserVariablesTable(mySql)
    client_logger.info("Please wait for command to be serviced")
    location = getCompleteFromCommandInputTable(commandId)
    client_logger.info(f"Report generated in location {location}")
    show_report(location)

def man(parser):
    if parser == "--help":
        print("give the man page for any pt command")
        print("currner corner for generating timing report ",globalVariable.corner)
    command = "man "+ parser
    commandId = writeToCommandInputTable(command)
    print("please wait for the command to be serviced")
    location = None
    while location == None:
        location = getCompleteFromCommandInputTable(commandId)
        print("report generated in location ",location)
    show_report(location)

@log_performance
def load_corner(corner):
    if corner == "--help":
        print("give the corner for which you need the timing numbers")
        print("use show_corner command to see the available list of corners")
    #show_corner()
    client_logger.info("changed the corner to "+str(corner))
    globalVariable.corner = corner
    return corner

@log_performance
def show_corner(option=None):
    client_logger.debug("The available corners are ")
    config = configparser.ConfigParser()
    project = globalVariable.project
    config.read(globalVariable.configFile)
    machineSetup = config[project]["machineSetup"]
    for cor in machineSetup.split("\n"):
        print(cor.split(":")[0])

@log_performance
def current_corner(option=None):
    client_logger.debug("The current corners is: "+globalVariable.corner)
    print("The current corners is: "+globalVariable.corner)
   
@log_performance
def show_report(location):
    if globalVariable.displayResult:
        print("This command will print the entire report from", location)
        directory_path, file_name = os.path.split(location)
        if globalVariable.userLocation == "":
            globalVariable.userLocation = input("please enter a location to dump the script: ")
        if globalVariable.userLocation != "":
            print ("need to copy the files to user location ", globalVariable.userLocation, " \nresolved permission issue")
            copy_file(location, globalVariable.userLocation)
            #code.interact(local=locals())
            #permission = check_permissions_recursive(location)
            if os.access(location, os.W_OK):
                os.remove(location)
            else:
                print("please ask the pt session owner to give permission to remove the files")
            location = globalVariable.userLocation+"/"+file_name
            globalVariable.tempLocation = location

        with open(location, 'r') as file:
            # Read the file line by line and print each line
            for line in file:
                print(line, end='')
    else:
        client_logger.debug("reports are not displayed run set_app_var displayResult 1 to enable displaying the reports")

@log_performance
def set_app_var(option):
    print(option)
    appName = option.split(" ")[0]
    appValue = option.split(" ")[1]
    #code.interact(local=locals())
    if isinstance(appValue, bool):
        appValue = bool(option.split(" ")[1])
    elif isinstance(appValue, int):
        appValue = int(option.split(" ")[1])
    elif isinstance(appValue, float):
        appValue = float(option.split(" ")[1])
    elif isinstance(appValue, str):
        appValue = str(option.split(" ")[1])
    setattr(globalVariable,appName,appValue)
    print(getattr(globalVariable,appName))


def get_app_var(option):
    print(option)
    print(getattr(globalVariable,option))
    #code.interact(local=locals())
    return(getattr(globalVariable,option))

@log_performance
def list_app_var(option=None):
    visibleVar = ["displayResult","historyLimit","tempLocation","userLocation"]
    for visVar in visibleVar:
        print(visVar," : ",getattr(globalVariable,visVar))
        
@log_performance
def set_user_location(location):
    path_to_check = location
    if check_permissions(path_to_check):
        globalVariable.userLocation = location
        print("[bold green]defined the user reports location to : [/bold green]", location)
    else:
        print("[bold red]user location not set please check the permission issue[/bold red]")

def get_user_location(location):
    print("[bold green]defined the user reports location : [/bold green]", globalVariable.userLocation)
    return(globalVariable.userLocation)

def load_work_week(workweek):
    globalVariable.runName = workweek
    print("[bold green]defined the user workweek : [/bold green]", globalVariable.runName)

def show_work_week(option=None):
    print("[bold green]defined the user workweek : [/bold green]", getAllWorkWeek())

def current_work_week(option=None):
    print("[bold green]the current workweek : [/bold green]", globalVariable.runName)

def load_block(blockName):
    globalVariable.blockName = blockName
    show_work_week()
    globalVariable.runName = input("give the run name: ")
    load_work_week(globalVariable.runName)
    print("[bold green]defined the block name : [/bold green]", globalVariable.blockName)

def show_block(option=None):
    print("[bold green]defined the block name : [/bold green]", getAllblockName())

def current_block(option=None):
    print("[bold green]the current block name is : [/bold green]", globalVariable.blockName)

@log_performance
def show_info(option=None):
    print("[bold green]Project : [/bold green]", globalVariable.project)
    print("[bold green]block name : [/bold green]", globalVariable.blockName)
    print("[bold green]work week : [/bold green]", globalVariable.runName)
    print("[bold green]corner : [/bold green]", globalVariable.corner)

@log_performance
def history(option=None):
    print("[bold green] current history length [/bold green]", globalVariable.historyLimit)
    print("[bold green]Command History : [/bold green]")
    commandNumber = 0
    #code.interact(local=locals())
    for hisCommand in globalVariable.commandHistory[-globalVariable.historyLimit:]:
        print(str(commandNumber)+") "+hisCommand)
        commandNumber +=1
    print("[bold green] increase the history limit using set_app_var historyLimit <int> : [/bold green]")

@log_performance
def compare_timing(command):
    print(command)
    ### check the commands correctness before proceding
    #code.interact(local=locals())
    pattern = r"-work_week\s+(.*?)\s+-corner\s+(.*?)-command {(.*)}"

    match = re.match(pattern,command)
    if match:
        workWeeks = match.group(1)
        corners = match.group(2)
        command = match.group(3)
        if "-nosplit" not in command:
            command += " -nosplit "
        if "-input_pins" not in command:
            command += " -input_pins "
        if "-nets" not in command:
            command += " -nets "
        if "-capacitance" not in command:
            command += " -capacitance "
        if "-transition" not in command:
            command += " -transition "
        client_logger.debug("this command will compare the timing between 2 runs for command "+ command +" on work week "+ workWeeks +" and corners "+ corners)
        #print("run command ",command," on work week ",workWeeks.split(":")[0]," and corner ",corners.split(":")[0])
        #code.interact(local=locals())
        #breakpoint()
        load_work_week(workWeeks.split(":")[0])
        load_corner(corners.split(":")[0])
        command = " ".join(command.split(" ")[1:])
        commandId = report_timing(command)
        mainReport = globalVariable.tempLocation
        client_logger.debug(globalVariable.tempLocation)
        returnData = extractPathInfo(globalVariable.tempLocation)
        comparePoint = 0
        pathCount = 0
        printTable = []
        #code.interact(local=locals())
        #breakpoint()
        console = Console()
        #code.interact(local=locals())

        client_logger.info("\n\n#################################################################")
        #print("\n\n#################################################################")
        #print("\nCommand Given is : "+command+"\n\n")

        for path in returnData:
            compareInputData = (os.environ.get("USER"),commandId,path[0],comparePoint,path[1],path[2],path[3],path[4],corners.split(":")[0],workWeeks.split(":")[0],globalVariable.blockName,globalVariable.blockName,globalVariable.project)
            #print("\nStartpoint: "+path[1]+"\nEndpoint: "+path[2]+"\n")
            printTable.append(path[1])
            printTable.append(path[2])
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("ID", style="dim", width=6)
            table.add_column("Corner")
            table.add_column("Slack")
            table.add_column("reportPath")
            #print(compareInputData)
            pathCount +=1
            table.add_row(str(pathCount)+"_Main", corners.split(":")[0] , path[4], str(commandId)+"::"+mainReport)
            client_logger.debug("Path"+str(pathCount))
            client_logger.debug("\nStartpoint: "+path[1]+"\n\nEndpoint: "+path[2]+"\n\nCorner: "+corners.split(":")[0]+"\n\nSlack: "+path[4])

            writeTocompareInputTable(compareInputData)
            childData = zip(corners.split(":")[0:],workWeeks.split(":")[0:])
            client_logger.info("\n\nGenerating for compare path\n\n")
            #code.interact(local=locals())
            for cor, ww in childData:
                try:
                    load_work_week(ww)
                except Exception as e:
                    client_logger.exception("An error occurred in load_work_week while passing ", ww)
                    #code.interact(local=locals())
                try:
                    load_corner(cor)
                except Exception as e:
                    client_logger.exception("An error occurred in load_corner while passing ", cor)
                    #code.interact(local=locals())
                childCommand = " -from "+path[1]+" -to "+path[2]+" -through {"+path[3].replace(":"," ")+"} -nosplit -input_pins -capacitance -nets -transition"
                childCommandId = report_timing(childCommand)
                childReturnData = extractPathInfo(globalVariable.tempLocation)
                for childPath in childReturnData:
                    compareInputData = (os.environ.get("USER"),childCommandId,childPath[0],comparePoint,childPath[1],childPath[2],childPath[3],childPath[4],cor,ww,globalVariable.blockName,globalVariable.blockName,globalVariable.project)
                    client_logger.info("Startpoint: "+childPath[1]+"\n\nEndpoint: "+childPath[2]+"\n\nCorner: "+cor+"\n\nSlack: "+childPath[4])
                    writeTocompareInputTable(compareInputData)
                    table.add_row(str(pathCount), cor , childPath[4], globalVariable.tempLocation)
            #console.print(table)
            printTable.append(table)
            comparePoint +=1
        #code.interact(local=locals())
        print("\n\n\n######################################################\n\nprinting Report")
        for i in range(0, len(printTable), 3):
            print("Startpoint: ",printTable[i:i+3][0])
            print("Endpoint: ",printTable[i:i+3][1],"\n\n")
            console.print(printTable[i:i+3][2])
        print ("\n\n##########################################")
        #print("\nCommand used: report_timing "+command)
        #print("\nStartpoint: "+path[1])
        #print("\nEndpoint: "+path[2])
        #console.print(table)
        client_logger.info("\n\n#################################################################\n\n")
    else:
        client_logger.info("the input command format is incorrect please follow the example\ncompare_timing -work_week 17p2:17p3 -corner 85:55 -command {report_timing -from abc}")

def extractPathInfo(fileName):
    pathCount = 1
    with open(fileName,'r') as file:
        lines = file.readlines()
        sp_pattern = r"\s+Startpoint:\s+(.*?)\s+(.*)"
        ep_pattern = r"\s+Endpoint:\s+(.*?)\s+(.*)"
        slack_pattern = r"\s+slack \(.*\).*\s+([-]?\d+.\d+).*$"
        path_start_pattern = r"\s+clock network delay.*"
        pin_pattern = r"\s+(.*?)\s.*"
        icgPath = 0
        spFlag = 0
        epFlag = 0
        pathStartFlag = 0
        slackFlag = 0
        comparePointId = 0
        returnData = []
        pinsList = []
        pathName = "path"+str(pathCount)
        print("path name :",pathName)
        for line in lines:
            if slackFlag:
                slackFlag = 0
                pathCount += 1
                pathName = "path"+str(pathCount)
                #print("\n\npath name :",pathName)
            match = re.match(slack_pattern,line)
            if match:
                slackFlag = 1
                slack = match.group(1)
                #print("slack:", slack)
                #print("commandId: ",commandId,"pathName: ",pathName," comparePoint: ",comparePointId,"sp: ",startPoint," ep: ",endPoint," pins: ",pinsList," slack: ",slack)
                pinsList = ":".join(pinsList)
                #code.interact(local=locals())
                tempList = [pathName,startPoint,endPoint,pinsList,slack]
                returnData.append(tempList)
                pinsList = []
            if pathStartFlag:
                if (startPoint not in line):
                    if (endPoint in line):
                        pathStartFlag = 0
                        spFlag = 0
                        epFlag = 0
                    match = re.match(pin_pattern,line)
                    if match and pathStartFlag:
                        match2 = re.match(r"\s+----",line)
                        if match2:
                            if (icgPath % 2) == 0:
                                icgPath += 1
                            else:
                                icgPath = icgPath - 1
                        #print(match.group(1))
                        if icgPath == 0:
                            if not match2:
                                pinsList.append(match.group(1))
            match = re.match(sp_pattern,line)
            if match:
                #code.interact(local=locals())
                startPoint = match.group(1)
                spFlag = 1
                #print("startPoint:", startPoint)
            if spFlag:
                match = re.match(ep_pattern,line)
                if match:
                    endPoint = match.group(1)
                    epFlag = 1
                    #print("endPoint:", endPoint)
            if epFlag:
                match = re.match(path_start_pattern,line)
                if match:
                    pathStartFlag = 1
    return returnData



@log_performance
def copy_file(source_file, destination_file):
    try:
        shutil.copy(source_file, destination_file)
        print(f"File '{source_file}' copied to '{destination_file}' successfully.")
    except FileNotFoundError:
        print("Source file not found.")
    except PermissionError:
        print("Permission denied.")
    except Exception as e:
        print(f"An error occurred: {e}")


def check_permissions(path):
    # Check if the path exists
    if not os.path.exists(path):
        print("[bold red]The path does not exist.[/bold red]")
        return False
    if os.access(path, os.W_OK):
        print("Write permission is available successfully setting the location.")
        return True
    else:
        print("[bold red]Write permission is denied.[/bold red]")
        return False

def exit(option=None):
    print("Exit tool")


def check_permissions_recursive(path):
    permission = True
    while True:
        if os.access(path, os.W_OK):
            permission = True
        else:
            permission = False
            return permission
        # Get the parent directory
        parent_directory = os.path.dirname(path)
        # If the parent directory is the same as the current directory, break the loop
        if parent_directory == path:
            break
        # Update the path to the parent directory for the next iteration
        path = parent_directory

####
