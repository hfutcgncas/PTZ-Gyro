import serial
import Controler


class cSerialPort:
    comPort = 0
    baudRate = 0
    
    com = 0
    Statue = 'busy'
    
    
    def __init__(self, comPort,baudRate):
        self.com = comPort
        self.baudRate = baudRate
        self.com = serial.Serial(comPort,baudRate)
        Statue = 'free' 
        print('Seral Ok')
         
    def __del__(self):
        self.com.close()
        


class cMotor:
    serCom = 0
    addr = 0
    mode = 'stop'
    position = 0
    
    positionMax = 0
    positionMin = 0
    
    vSet = 0
    
    controler = 0
    #------------------------#
    def com2Motor(self,cmd):
      #  while 1:
      #     if self.serCom.Statue == 'free':
                self.serCom.Statue = 'busy'
                self.serCom.com.write(cmd)
                str = ''
                while 1:
                    ch = self.serCom.com.read(1)
                    if ch == '\r':
                        break
                    else:
                        str = str + ch
                self.serCom.Statue = 'free'
                return str
     #      else:
     #           print('W')
     #           continue
    #------------------------#
    def __init__(self,addr,serCom, CtrlP):
        self.addr = addr
        self.serCom = serCom
        self.controler = Controler.cControler(CtrlP) #Vmax = 180deg/s
        print ('motor ' + str(addr) + ' InitOK')
        
    #------------------------#

    def Disable(self): 
        self.mode = 'stop'
        cmd = str(self.addr) + ' s r0x24 0\r'
        response = self.com2Motor(cmd)
        print ('motor ' + str(self.addr) + ' Disable: '+ response)
        
    def getPosition(self):
        cmd = str(self.addr) + ' g r0x32\r'
        response = self.com2Motor(cmd)
        if response[0]=='v':
            result = str(response[2:])
            return float(result)/1600.0
        else:
            print ('getPosition error')
            return 0
    
    def getVelocity(self):
        cmd = str(self.addr) + ' g r0x18\r'
        response = self.com2Motor(cmd)
        if response[0]=='v':
            result = str(response[2:])
            return float(result)/16000.0
        else:
            print ('getVelocity error')
            return 0
        
    def getStatue(self):
        cmd = str(self.addr) + ' g r0xa0\r'
        response = self.com2Motor(cmd)
        print ('statue '+ response)
        return response
        
    def posLoop(self, SetPos):
        self.controler.Input = SetPos - self.getPosition() 
        self.vSet = self.controler.pollContrl()
        if self.vSet!=0:
            self.changeSpeed(self.vSet)
        
        
    #------- V-mode ---------#
    def sw2_Vmode(self,al,dl):
        cmd = str(self.addr) + ' s r0x36 ' + str(int(al)) + '\r'
        response = self.com2Motor(cmd)
        print ('motor ' + str(self.addr) + ' acelerationLimit setting: ' + response)
        cmd = str(self.addr) + ' s r0x37 ' + str(int(dl)) + '\r'
        response = self.com2Motor(cmd)
        print ('motor ' + str(self.addr) + ' decelerationLimit setting: ' + response)

        
    def Enable_V(self): 
        self.mode = 'Velocity'
        cmd = str(self.addr) + ' s r0x24 11\r'
        response = self.com2Motor(cmd)
    def changeSpeed(self,speed):
        speed = int(speed*16000)
        cmd = str(self.addr) + ' s r0x2f ' + str(speed) + '\r'
        response = self.com2Motor(cmd)
        if self.mode != 'Velocity':
            self.Enable_V()
    #------------------------#                 
    def sw2_Pmode(self,vMax,aMax,dMax):
        cmd = str(self.addr) + ' s r0xc8 0\r'
        response = self.com2Motor(cmd)
        print('motor ' + str(self.addr) + ' trajectory generator setting: ' + response) 
        cmd = str(self.addr) + ' s r0xcb '+str(vMax)+'\r' #Set maximum velocity to 7000 counts/second. 
        response = self.com2Motor(cmd)
        print ('motor ' + str(self.addr) + ' maximum velocity setting: ' + response)
        cmd = str(self.addr) + ' s r0xcc '+str(aMax)+'\r' #Set maximum acceleration to 7000 counts/second. 
        response = self.com2Motor(cmd)
        print ('motor ' + str(self.addr) + ' maximum acceleration setting: ' + response)
        cmd = str(self.addr) + ' s r0xcd '+str(dMax)+'\r' #Set maximum deceleration to 7000 counts/second. 
        response = self.com2Motor(cmd)
        print ('motor ' + str(self.addr) + ' maximum deceleration setting: ' + response)
    
    def Enable_P(self):
        self.mode = 'Position'
        cmd = str(self.addr) + ' s r0x24 21\r'
        response = self.com2Motor(cmd)
        
    def setPosition(self,position):
        cmd = str(self.addr) + ' s r0xca ' + str(position) + '\r'
        response = self.com2Motor(cmd)
        
    def motorGo_P(self):
        if self.mode != 'Position':
            self.Enable_P()
        cmd = str(self.addr) + ' t 1\r'
        response = self.com2Motor(cmd)
        
    def motorStop_P(self):
        cmd = str(self.addr) + ' t 0\r'
        response = self.com2Motor(cmd)
    

    
