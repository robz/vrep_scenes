import vrep, math

PORT = 6666
IPADDRESS = '192.168.1.34'

def run360():
    print "connecting to vrep with address", IPADDRESS, "on port", PORT

    clientID = vrep.simxStart(IPADDRESS, PORT, True, True, 5000, 5)
        
    print "hello vrep! ", clientID

    if clientID == -1:
        print "failed to connect to vrep server"
        return

    # get the motor joint handle
    error,jointHandle = vrep.simxGetObjectHandle(clientID, "plantStandMotor", vrep.simx_opmode_oneshot_wait)
    
    print "starting the motor..."
    
    # set the velocity of the joint
    vrep.simxSetJointTargetVelocity(clientID, jointHandle, 1.0, vrep.simx_opmode_oneshot_wait);

    print "spinning 360 degrees..."
    
    # set up to stream joint positions
    vrep.simxGetJointPosition(clientID, jointHandle, vrep.simx_opmode_streaming);
    
    passed90Degrees = False

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
            if passed90Degrees and position >= 0 and position < math.pi/2.0:
                break
            elif not passed90Degrees and position > math.pi/2.0:
                passed90Degrees = True

    print "stoppping..."
            
    vrep.simxSetJointTargetVelocity(clientID, jointHandle, 0.0, vrep.simx_opmode_oneshot_wait);

    if clientID != -1:
        vrep.simxFinish(clientID)

    print "done!"

run360();