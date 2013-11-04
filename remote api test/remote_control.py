import vrep

PORT=6666
IPADDRESS='127.0.0.1'

print "connecting to vrep with address ", IPADDRESS, " on port ", PORT

clientID = vrep.simxStart('127.0.0.1',6666,True,True,5000,5)
    
print "hello vrep! ", clientID

print "starting the motor..."

error,jointHandle = vrep.simxGetObjectHandle(clientID, "plantStandMotor", vrep.simx_opmode_oneshot_wait)
vrep.simxSetJointTargetVelocity(clientID, jointHandle, 1.0, vrep.simx_opmode_oneshot_wait);

print "getting joint positions..."

vrep.simxGetJointPosition(clientID, jointHandle, vrep.simx_opmode_streaming);

started = False

print "spinning 360 degrees..."

# The control loop:
while vrep.simxGetConnectionId(clientID) != -1 : # while we are connected to the server..
    (error,position) = vrep.simxGetJointPosition(
        clientID,
        jointHandle,
        vrep.simx_opmode_buffer
        )

    # Fetch the newest joint value from the inbox (func. returns immediately (non-blocking)):
    if error==vrep.simx_error_noerror : 
        # here we have the newest joint position in variable jointPosition! 
        # break when we've done a 360
        if started and position >= 0 and position < 1:
            break
        elif not started and position > 1:
            started = True

print "stoppping..."
        
vrep.simxSetJointTargetVelocity(clientID, jointHandle, 0.0, vrep.simx_opmode_oneshot_wait);

if clientID != -1:
    vrep.simxFinish(clientID)

print "done!"
