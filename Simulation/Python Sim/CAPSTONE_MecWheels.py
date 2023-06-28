# ONLY MECANUM WHEELS, NO SENSORS

import sim
import sys
import time                # Used to keep track of time
import numpy as np         # Array library
import math
import matplotlib as mpl   # Used for image plotting

# Connecting V-REP to Python

sim.simxFinish(-1)
clientID=sim.simxStart('127.0.0.1',19999,True,True,5000,5)

if clientID!=-1:
    print ('Connected to remote API server')
else:
    print ('Failed connecting to remote API server')
    sys.exit('Could not connect')
    
# Initiating and getting the Object Handles for the joint motors
    
errorCode, FRhandle = sim.simxGetObjectHandle(clientID, 'FRTypeA', sim.simx_opmode_blocking)
errorCode, BRhandle = sim.simxGetObjectHandle(clientID, 'BRTypeB', sim.simx_opmode_blocking)
errorCode, FLhandle = sim.simxGetObjectHandle(clientID, 'FLTypeB', sim.simx_opmode_blocking)
errorCode, BLhandle = sim.simxGetObjectHandle(clientID, 'BLTypeA', sim.simx_opmode_blocking)
rolling=[FRhandle,BRhandle,FLhandle,BLhandle]

slip1 = sim.simxGetObjectHandle(clientID, 'freeJoint_br', sim.simx_opmode_blocking)
slip2 = sim.simxGetObjectHandle(clientID, 'freeJoint_fr', sim.simx_opmode_blocking)
slip3 = sim.simxGetObjectHandle(clientID, 'freeJoint_bl', sim.simx_opmode_blocking)
slip4 = sim.simxGetObjectHandle(clientID, 'freeJoint_fl', sim.simx_opmode_blocking)
slipping=[slip1,slip2,slip3,slip4]

wheel1 = sim.simxGetObjectHandle(clientID, 'respondableWheel_br', sim.simx_opmode_blocking)
wheel2 = sim.simxGetObjectHandle(clientID, 'respondableWheel_fr', sim.simx_opmode_blocking)
wheel3 = sim.simxGetObjectHandle(clientID, 'respondableWheel_bl', sim.simx_opmode_blocking)
wheel4 = sim.simxGetObjectHandle(clientID, 'respondableWheel_fl', sim.simx_opmode_blocking)
wheel=[wheel1,wheel2,wheel3,wheel4]

t = time.time()

def movement(forwBackVel, leftRightVel, rotVel):
    sim.simxSetJointTargetVelocity(clientID,FLhandle,-forwBackVel-leftRightVel-rotVel, sim.simx_opmode_streaming)
    sim.simxSetJointTargetVelocity(clientID,BLhandle,-forwBackVel+leftRightVel-rotVel, sim.simx_opmode_streaming)
    sim.simxSetJointTargetVelocity(clientID,BRhandle,-forwBackVel-leftRightVel+rotVel, sim.simx_opmode_streaming)
    sim.simxSetJointTargetVelocity(clientID,FRhandle,-forwBackVel+leftRightVel+rotVel, sim.simx_opmode_streaming)
    
    for i in range(4):
        if (sim.simxGetObjectParent(clientID,rolling[i],sim.simx_opmode_blocking)!=-1):
            sim.simxSetObjectPosition(clientID,slipping[i],rolling[i],[0,0,0],sim.simx_opmode_oneshot)
            sim.simxSetObjectOrientation(clientID,slipping[i],rolling[i],[-math.pi/4,0,0],sim.simx_opmode_buffer)
            sim.simxSetObjectPosition(clientID,wheel[i],rolling[i],[0,0,0],sim.simx_opmode_oneshot)
            sim.simxSetObjectOrientation(clientID,wheel[i],rolling[i],[0,0,.0],sim.simx_opmode_buffer)
        

# Running the program

while (time.time()-t)<60:

    movement(1,0,0) 


#Post ALlocation
errorCode=sim.simxSetJointTargetVelocity(clientID,FRhandle,0, sim.simx_opmode_streaming)
errorCode=sim.simxSetJointTargetVelocity(clientID,BRhandle,0, sim.simx_opmode_streaming)
errorCode=sim.simxSetJointTargetVelocity(clientID,FLhandle,0, sim.simx_opmode_streaming)
errorCode=sim.simxSetJointTargetVelocity(clientID,BLhandle,0, sim.simx_opmode_streaming)



