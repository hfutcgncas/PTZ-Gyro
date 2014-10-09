import motor
dT = 0.01

vMax = 90
vMin = 0
dz = 0

Kp = 5
Ki = 0
Kd = 0.2

aMax = 400

ctrlP_Pitch = [vMax, vMin, dz, Kp, Ki, Kd]
ctrlP_Row  = [vMax, vMin, dz, Kp, Ki, Kd]

class cPTZ:
    motorPitch     = 0
    motorYaw      = 0
    serCom  = 0
    
    def __init__(self):
        self.serCom  = motor.cSerialPort('com12',9600)
        self.motorPitch = motor.cMotor(0,self.serCom , ctrlP_Pitch)
        self.motorPitch.sw2_Vmode(aMax,aMax) 
        self.motorYaw  = motor.cMotor(1,self.serCom , ctrlP_Row)
        self.motorYaw.sw2_Vmode(aMax,aMax)
        
    def PollMoveEuler(self, Pitch,Yaw ):
        self.motorPitch.posLoop(Pitch)
        self.motorYaw.posLoop(Yaw)
    
    def EulerPos(self):
        Pitch = self.motorPitch.getPosition()
        Yaw  = self.motorYaw.getPosition()
        rlt = [Pitch, Yaw]
        return rlt
        
    def Stop(self):
        self.motorPitch.Disable()
        self.motorYaw.Disable()
        
