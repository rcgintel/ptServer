#! /usr/intel/bin/python3.10.8
import sys
sys.path.append('/nfs/site/disks/vmisd_vclp_efficiency/rcg/server/fullServer/venvRcg/lib/python3.11/site-packages')
import sqlite3
import configparser
import globalVariable
import os
from ptServerDatabasemysql import *
import argparse
from rich import print
import json
from threading import Thread
import time
import datetime

from log_config import get_server_logger

def checkLicense():
    expiry_date = datetime.datetime(2024, 6, 30)
    current_date = datetime.datetime.now()
    if current_date > expiry_date:
        print("Time expired please expect next version code for implementation")
        os.exit()
    else:
        print("Valid code")

server_logger = get_server_logger()
log_banner = """
************************************
            PT SERVER 
************************************
"""

### this script will spawn the pt server machine
def background_task(interval_sec):
    # run forever
    flag = True
    while flag:
        # block for the interval
        time.sleep(interval_sec)
        #print(globalVariable.runName)
        for t in getAllAvailbeMachine():
            server_logger.info(f" Background Task : MachineID: {t['machineId']}, Heartbeat: {t['heartBeat']}")
            if t['heartBeat'] > 10:
                server_logger.warning("Background Task : machine on machineID :"+t["machineId"]+" will be marked killed")
                setMachineKilledInMachineTrackerTable(t['machineName'],t['workWeek'],t['projectName'])
                env = config[project]["gtEnv"]
                wash = config[project]["wash"]
                target = config[project]["target"]
                Cores = config[project]["cores"]
                qslot = config[project]["qslot"]
                clas = config[project]["clas"]
                machineMemory = config[project]["machineMemory"]
                ptServerTcl = config[project]["ptServerTcl"]
                cmd = "nbjob run --target "+target+" --qslot "+qslot+" --wash  --class \'"+clas+""+machineMemory+"G&&"+Cores+"C\' xterm -T \""+t["machineName"]+"\" -e \"source setup"+t['machineName']+".csh\""
                server_logger.info(f"running {cmd}")
                os.system(cmd)

            else:
                server_logger.info("Background Task: incrementing heartbeat of MachineID {t[machineId]} by 1")
                hbeat = int(t['heartBeat']) + 1
                updateMachineHeartbeat(t['machineId'],hbeat)

def machineSpawn_task(interval_sec):
    # run forever
    while True:
        # block for the interval
        time.sleep(interval_sec)
        #print(globalVariable.runName)
        for t in getAllAvailbeMachine():
            print(t['machineId'],t['heartBeat'])
            if t['heartBeat'] > 10:
                print("machine on machineID :",t["machineId"]," will be marked killed")
                setMachineKilledInMachineTrackerTable(t['machineName'],t['workWeek'],t['projectName'])
                env = config[project]["gtEnv"]
                wash = config[project]["wash"]
                target = config[project]["target"]
                Cores = config[project]["cores"]
                qslot = config[project]["qslot"]
                clas = config[project]["clas"]
                machineMemory = config[project]["machineMemory"]
                ptServerTcl = config[project]["ptServerTcl"]
                cmd = "nbjob run --target "+target+" --qslot "+qslot+" --wash  --class \'"+clas+""+machineMemory+"G&&"+Cores+"C\' xterm -T \""+t["machineName"]+"\" -e \"source setup"+t['machineName']+".csh\""
                print ("run the command ", cmd)
                os.system(cmd)


            else:
                print("increment the heartbeat by 1")
                hbeat = int(t['heartBeat']) + 1
                updateMachineHeartbeat(t['machineId'],hbeat)
        # perform the task
        #code.interact(local=locals())
        print('SpawnBackground task!')
 
#######################

config = configparser.ConfigParser()

parser = argparse.ArgumentParser(description="User arg1")
parser.add_argument("-R", "--restore", action="store_true", help="Restore the project")
#parser.add_argument("-P", "--project", dest="project",default="nil" , help="Restore the project")
parser.add_argument("-W", "--run", dest="runName",default="nil" , help="Run name")
parser.add_argument("-N", "--name", dest="blockName",default="nil" , help="block Name ")
args = parser.parse_args()

globalVariable.project = os.environ.get("PROJ_NAME")
#if args.project == "nil":
project = globalVariable.project
#else:
#    project = args.project
checkLicense()

if args.blockName == "nil":
    blockName = globalVariable.blockName
else:
    blockName = args.blockName

if args.runName == "nil":
    runName = globalVariable.runName
else:
    runName = args.runName

globalVariable.runName = runName
config.read(globalVariable.configFile)
machineSetup = config[project]["machineSetup"]
count = 0

server_logger.info(log_banner)
server_logger.info(f"Current Project: {globalVariable.project}")
server_logger.info(f"Current Block: {blockName}")
server_logger.info(f"Current run name: {runName}")
server_logger.info(f"Machine setup: {machineSetup}")

setupDatabase()
## removed the fork task
server_logger.info("Starting background tasks thread")
daemon = Thread(target=background_task, args=(60,), daemon=True, name='Background')
daemon.start()
#daemon = Thread(target=machineSpawn_task, args=(60,), daemon=True, name='SpawnBackground')
#daemon.start()

if not args.restore:
    server_logger.info("NOT A RESTORE SESSION. STARTING NEW PT SHELLS")
    server_logger.info("Invoking PT Shells")
    for cornerMachine in machineSetup.split("\n"):
        server_logger.info("the number of machines that we need for corner "+cornerMachine.split(":")[0]+" is "+cornerMachine.split(":")[1])
        for cornerName in range(int(cornerMachine.split(":")[1])):
            corner = cornerMachine.split(":")[0]
            env = config[project]["gtEnv"]
            wash = config[project]["wash"]
            target = config[project]["target"]
            Cores = config[project]["cores"]
            qslot = config[project]["qslot"]
            clas = config[project]["clas"]
            machineMemory = config[project]["machineMemory"]
            ptServerTcl = config[project]["ptServerTcl"]


            
            #print("corner ",corner," spanning machine ", cornerName, " env ", env)
            ex_file = open("./setup"+corner+"_"+str(cornerName)+".csh","w")
            ex_file2 = open("./ptRun"+corner+"_"+str(cornerName)+".tcl","w")
            ex_file.write(env)
            data = "\n\npt_shell -file ./ptRun"+corner+"_"+str(cornerName)+".tcl -output_log_file ptServer_"+corner+"_"+str(cornerName)+".log"
            ex_file.write(data)
            data = "set database \""+config[project]["database"]+"\"\n"
            ex_file2.write(data)
            data = "set cornerName \""+corner+"_"+str(cornerName)+"\"\n"
            ex_file2.write(data)
            data = "set workWeek \""+runName+"\"\n"
            ex_file2.write(data)
            data = "set project \""+project+"\"\n"
            ex_file2.write(data)

            data = "\nsource "+ptServerTcl+"\n"
            ex_file2.write(data)

            ### need to insert the machines to machine tracker table
            cmd = "nbjob run --target "+target+" --qslot "+qslot+" --wash  --class \'"+clas+""+machineMemory+"G&&"+Cores+"C\' xterm -T \""+corner+"_"+str(cornerName)+"\" -e \"source setup"+corner+"_"+str(cornerName)+".csh\""
            ex_file.close()
            ex_file2.close()
            #code.interact(local=locals())
            if (globalVariable.noPTdebug):
                server_logger.info("no PT Debug set. All machine's status set to ready")
                status = "ready"
            else:
                status = "loading"
                server_logger.info("Running command : "+cmd)
                try:
                    os.system(cmd)
                except Exception as e:
                    server_logger.error(f"Machine not spawned. Error running njob command {cmd} : \n {e}")
                    sys.exit(0)
                    
                ######### insert to database
                #machineTrackerTable = ["machineId","machineName","corner","status","load","commandId","workWeek"]
                machineName = corner+"_"+str(cornerName)
                
                load = 0
                commandId = 0
                workWeek = runName
                projectName = project
                mySql = (machineName,corner,status,load,commandId,workWeek,projectName,blockName)
                #print(mySql,":: rcg")
                writeToMachineTrackerTable(mySql)
                
    server_logger.info("Invoked all PT Shells")


flag = 1
while (flag):
    """
    ## track the machines and jobs
    # get the database
    foreach get all the jobs not serviced (serviced = 0) 
        get the machines available for the corner
        see if the machines is free (status=ready)
        if machine free:
            assign the command to the machine
        else:
            do nothing
    """
    ## get the database
    notServiced = getAllNotServicedJobs()
    for job in notServiced:

        commandId = job['commandId']
        jobCorner = job['corner']
        machine = getAllAvailbeMachineForCorner(jobCorner)
        
        if str(machine) != "[]":
            machine = machine[0]
            machine = str(machine)
            machine = machine.replace("{", "")
            machine = machine.replace("}", "")
            machine = machine.replace("'", "")
            if len(machine) > 0:
                machineName = machine.split(",")[1].split(":")[1].lstrip()
                updateMachineNameInCommandInputTable(machineName,commandId)
            else:
                server_logger.info(f"Waiting for machines")
            
        else:
            server_logger.info("PT shell is not yet available for servicing commands")
    time.sleep(5)