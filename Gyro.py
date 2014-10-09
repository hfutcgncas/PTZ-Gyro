import serial
import time  

GyroComPort = 'com8'
GyroCombaud = 38400

class cGyro:
    convertFactor = (360.0/65536.0)
    cmd = '\x0e'
    out = [0]*20
    com = 0
    Roll = 0
    Pitch = 0
    Yaw = 0
    RollBase = 0
    PitchBase = 0
    YawBase = 0
    
    def __init__(self):
        self.com = serial.Serial(GyroComPort,GyroCombaud)
        print("Gyro Init OK")
    
    def GetEuler(self):
        self.com.write(self.cmd)  
        resp = self.com.read(11)
        i = 0
        for ch in resp:
            self.out[i] = ord(ch)
            i = i + 1
        self.Roll    = (self.out[1]*256 + self.out[2])*self.convertFactor - self.RollBase
        self.Pitch  = (self.out[3]*256 + self.out[4])*self.convertFactor - self.PitchBase
        self.Yaw   = (self.out[5]*256 + self.out[6])*self.convertFactor - self.YawBase
        
        if self.Roll > 180:
            self.Roll = self.Roll - 360
        if self.Pitch > 180:
            self.Pitch = self.Pitch - 360
        if self.Yaw > 180:
            self.Yaw = self.Yaw - 360
    
    def Home(self):
        self.RollBase = 0
        self.PitchBase = 0
        self.YawBase = 0
        self.GetEuler()
        self.RollBase = self.Roll
        self.PitchBase = self.Pitch
        self.YawBase = self.Yaw
        
        
        
