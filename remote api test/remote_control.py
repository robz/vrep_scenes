import vrep

PORT=6666
IPADDRESS='127.0.0.1'

print "connecting to vrep with address ", IPADDRESS, " on port ", PORT

clientID = vrep.simxStart('127.0.0.1',6666,True,True,5000,5)
    
print "hello vrep! ", clientID

error,jointHandle = vrep.simxGetObjectHandle(clientID, "plantStandMotor", vrep.simx_opmode_oneshot_wait)
vrep.simxGetJointPosition(clientID, jointHandle, vrep.simx_opmode_streaming);

# The control loop:
while vrep.simxGetConnectionId(clientID)!=-1 : # while we are connected to the server..
    (error,position) = vrep.simxGetJointPosition(
        clientID,
        jointHandle,
        vrep.simx_opmode_buffer
        )

    # Fetch the newest joint value from the inbox (func. returns immediately (non-blocking)):
    if error==vrep.simx_error_noerror : 
        # here we have the newest joint position in variable jointPosition! 
        print position

if clientID != -1:
    vrep.simxFinish(clientID)
