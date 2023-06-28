 # ORIGINAL

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
errorCode, LPhandle = sim.simxGetObjectHandle(clientID, 'left_prism', sim.simx_opmode_blocking)
errorCode, RPhandle = sim.simxGetObjectHandle(clientID, 'right_prism', sim.simx_opmode_blocking)

# Initiating and getting the Object Handles for the sensors

errorCode, sensor1 = sim.simxGetObjectHandle(clientID, 'Ultrasonic_Right', sim.simx_opmode_blocking)
errorCode, sensor2 = sim.simxGetObjectHandle(clientID, 'Ultrasonic_Mid', sim.simx_opmode_blocking)
errorCode, sensor3 = sim.simxGetObjectHandle(clientID, 'Ultrasonic_Left', sim.simx_opmode_blocking)
errorCode, sensor4 = sim.simxGetObjectHandle(clientID, 'RayRight', sim.simx_opmode_blocking)
errorCode, sensor5 = sim.simxGetObjectHandle(clientID, 'RayMid', sim.simx_opmode_blocking)
errorCode, sensor6 = sim.simxGetObjectHandle(clientID, 'RayLeft', sim.simx_opmode_blocking)

sensor_h=[sensor1, sensor2, sensor3, sensor4, sensor5, sensor6] #list for handles
sensor_val=np.array([]) #empty array for sensor measurements
sensor_detState=[]  #empty list for detectionState

# Orientation of all the sensors: 
sensor_loc=np.array([0.11,1,-0.11,0.11,1,-0.11]) 

# Reading the sensors

for x in range(1,6+1):
        errorCode,detectionState,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector=sim.simxReadProximitySensor(clientID,sensor_h[x-1],sim.simx_opmode_streaming)                
        sensor_val=np.append(sensor_val,np.linalg.norm(detectedPoint)) #get list of values
        sensor_detState.append(detectionState)

t = time.time()


# =============================================================================
# noDetectionDist=0.5
# maxDetectionDist=0.2
# detect=[0,0,0]
# braitenbergL=[-1.2,-1.6,-2.0]
# braitenbergR=[-2.0,-1.6,-1.2]
# v0=2
# =============================================================================

# Running the program

while (time.time()-t)<60:
    sensor_val=np.array([])    
    for x in range(1,6+1):
        errorCode,detectionState,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector=sim.simxReadProximitySensor(clientID,sensor_h[x-1],sim.simx_opmode_buffer)                
        sensor_val=np.append(sensor_val,np.linalg.norm(detectedPoint)) #get list of values
        sensor_detState.append(detectionState)
    
    print('sensor_detState: ' + str(sensor_detState))
    print('sensor_val: ' + str(sensor_val))
    #controller specific
    sensor_sq=sensor_val[0:3]*sensor_val[0:3] #square the values of front-facing sensors
    print('sensor_sq: ' + str(sensor_sq)) 
    
#    errorCode,positionL = sim.simxGetJointPosition(clientID,LPhandle,sim.simx_opmode_streaming)
#    errorCode,positionR = sim.simxGetJointPosition(clientID,RPhandle,sim.simx_opmode_streaming)
#    print(positionL)
#    print(positionR)    

    pla,pra = 0,0   # Linear Actuator positions
    
    if sensor_detState[3]==True:
        print('sensor_detState[0]: ' + str(sensor_detState[0]))
        print('sensor_sq[0]: ' + str(sensor_sq[0]))
        pra=-0.1
   
    if sensor_detState[5]==True:
        print('sensor_detState[2]: ' + str(sensor_detState[2]))
        print('sensor_sq[2]: ' + str(sensor_sq[2]))
        pla=0.1
    

#    min_ind=np.where(sensor_sq==np.min(sensor_sq))
#    min_ind=min_ind[0][0]
    
    if sensor_detState[4]==True:
        if sensor_sq[1]<0.02:
            print('sensor_detState[1]: ' + str(sensor_detState[1]))
            print('sensor_sq[1]: ' + str(sensor_sq[1]))
            steer=-1/sensor_loc[1]
        else:
            steer=0
    else:
        steer=0

    v=1	#forward velocity
    kp=0.5	#steering gain
    vl=v+kp*steer
    vr=v-kp*steer
    print("V_l =",vl)
    print("V_r =",vr)
    
# =============================================================================
#     for i in range(3):
#         if sensor_detState[i]==True  and sensor_val[i]<noDetectionDist:
#             if sensor_val[i]<maxDetectionDist:
#                 dist=maxDetectionDist
#             detect[i]=1-((dist-maxDetectionDist)/(noDetectionDist-maxDetectionDist))
#         else:
#             detect[i]=0
#     
#     vLeft=v0
#     vRight=v0
#     
#     for i in range(3):
#         vLeft=vLeft+braitenbergL[i]*detect[i]
#         vRight=vRight+braitenbergR[i]*detect[i]
# =============================================================================
    
    errorCode=sim.simxSetJointTargetVelocity(clientID,FRhandle,vr, sim.simx_opmode_streaming)
    errorCode=sim.simxSetJointTargetVelocity(clientID,BRhandle,vr, sim.simx_opmode_streaming)
    errorCode=sim.simxSetJointTargetVelocity(clientID,FLhandle,vl, sim.simx_opmode_streaming)
    errorCode=sim.simxSetJointTargetVelocity(clientID,BLhandle,vl, sim.simx_opmode_streaming)
# Linear actuator
    errorCode=sim.simxSetJointTargetPosition(clientID,LPhandle,pla, sim.simx_opmode_streaming)
    errorCode=sim.simxSetJointTargetPosition(clientID,RPhandle,pra, sim.simx_opmode_streaming)
    
    sensor_detState.clear()
    
    time.sleep(0.2) #loop executes once every 0.2 seconds (= 5 Hz)

#Post ALlocation
errorCode=sim.simxSetJointTargetVelocity(clientID,FRhandle,0, sim.simx_opmode_streaming)
errorCode=sim.simxSetJointTargetVelocity(clientID,BRhandle,0, sim.simx_opmode_streaming)
errorCode=sim.simxSetJointTargetVelocity(clientID,FLhandle,0, sim.simx_opmode_streaming)
errorCode=sim.simxSetJointTargetVelocity(clientID,BLhandle,0, sim.simx_opmode_streaming)


# Setting joint motor velocities

#errorCode = sim.simxSetJointTargetVelocity(clientID, FRhandle, 0.2, sim.simx_opmode_oneshot)
#errorCode = sim.simxSetJointTargetVelocity(clientID, BRhandle, 0.2, sim.simx_opmode_oneshot)
#errorCode = sim.simxSetJointTargetVelocity(clientID, FLhandle, 0.2, sim.simx_opmode_oneshot)
#errorCode = sim.simxSetJointTargetVelocity(clientID, BLhandle, 0.2, sim.simx_opmode_oneshot)
#errorCode = sim.simxSetJointTargetVelocity(clientID, LPhandle, 0.2, sim.simx_opmode_oneshot)
#errorCode = sim.simxSetJointTargetVelocity(clientID, RPhandle, 0.2, sim.simx_opmode_oneshot)

# Reading the sensors
#errorCode, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = sim.simxReadProximitySensor(clientID, sensor1, sim.simx_opmode_buffer)
#errorCode, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = sim.simxReadProximitySensor(clientID, sensor2, sim.simx_opmode_buffer)
#errorCode, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = sim.simxReadProximitySensor(clientID, sensor3, sim.simx_opmode_buffer)
