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

### this script will spawn the pt server machine
def background_task(interval_sec):
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
        print('Background task!')
 
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

setupDatabase()
daemon = Thread(target=background_task, args=(60,), daemon=True, name='Background')
daemon.start()
#background_task(60)

if not args.restore:
    for cornerMachine in machineSetup.split("\n"):
        print("the number of machines that we need for corner ",cornerMachine.split(":")[0]," is ",cornerMachine.split(":")[1])
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
            data = "\n\npt_shell -file ./ptRun"+corner+"_"+str(cornerName)+".tcl"
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
                status = "ready"
            else:
                status = "loading"
                print("Running command : ",cmd)
                os.system(cmd)
                ######### insert to database
                #machineTrackerTable = ["machineId","machineName","corner","status","load","commandId","workWeek"]
                machineName = corner+"_"+str(cornerName)
                
                load = ""
                commandId = ""
                workWeek = runName
                projectName = project
                mySql = (machineName,corner,status,load,commandId,workWeek,projectName,blockName)
                print(mySql,":: rcg")
                writeToMachineTrackerTable(mySql)



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
    #database = config[project]["database"]
    #code.interact(local=locals())
    
    notServiced = getAllNotServicedJobs()
    #code.interact(local=locals())
    for job in notServiced:
        #code.interact(local=locals())
        #job = str(job)
        #job = job.replace("{", "")
        #job = job.replace("}", "")
        #job = job.replace("'", "")
        #commandId = job.split(",")[0].split(":")[1].lstrip()
        commandId = job['commandId']
        jobCorner = job['corner']
        #print("jobs not serviced ", job)
        #jobCorner = job.split(",")[1].split(":")[1].lstrip()
        machine = getAllAvailbeMachineForCorner(jobCorner)
        #code.interact(local=locals())
        if str(machine) != "[]":
            machine = machine[0]
            machine = str(machine)
            machine = machine.replace("{", "")
            machine = machine.replace("}", "")
            machine = machine.replace("'", "")
            #machine = str(machine[0]).replace("{", "")
            #machine = machine.replace("}", "")
            #machine = machine.replace("'", "")
            if len(machine) > 0:
                machineName = machine.split(",")[1].split(":")[1].lstrip()
                updateMachineNameInCommandInputTable(machineName,commandId)
            else:
                print("waiting for machines")
            #code.interact(local=locals())
        else:
            print("PT shell is not yet available for servicing commands")
    time.sleep(5)
    #flag = 0