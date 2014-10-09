import PTZ
import time
import Gyro

dT = 0.01
SetPicth = 0
SetYaw = 0

ptz = PTZ.cPTZ()
gyro = Gyro.cGyro()
gyro.Home()

print('Begin: ')
raw_input()

while 1:
    
    while 1:
        gyro.GetEuler()
        SetPicth = gyro.Pitch
        SetYaw  = gyro.Yaw
        
        if SetPicth > 45:
            SetPicth = 45
        elif SetPicth < -45:
            SetPicth = -45
        
        if SetYaw > 45:
            SetYaw = 45
        elif SetYaw < -45:
            SetYaw = -45
            
        ptz.PollMoveEuler(SetPicth, SetYaw)
        Pos =  ptz.EulerPos()
#        if abs(Pos[0] - SetPicth) < 1 and abs(Pos[1] - SetYaw) < 1:
#            ptz.Stop() 
#            break
#        print(str(Pos))
        time.sleep(dT)
     
    ptz.Stop()    
    print('continue?: Y/N')
    IN = raw_input()
    if IN =='N':
        break



