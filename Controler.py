class cControler:
    Input = 0
    Output = 0
    
    Kp = 0
    Ki = 0
    Kd = 0
    
    Length4SumList = 20
    dSumList = [0]*Length4SumList
    
    Vmax = 0
    Vmin = 0
    deadZoon = 1      #degree
    
    def __init__(self, ctrlP):
        self.Vmax = ctrlP[0]
        self.Vmin =  ctrlP[1]
        self.deadZoon= ctrlP[2]
        
        self.Kp = ctrlP[3]
        self.Ki = ctrlP[4]
        self.Kd = ctrlP[5]
        
        self.dSumList = [0]*self.Length4SumList
        
    
    def PIDcontroler(self, In):
        out = self.Kp*In + self.Ki*sum(self.dSumList) + self.Kd*(In-self.dSumList[-1])
        del(self.dSumList[0])
        self.dSumList.append(out);
        return out
    
    
    def pollContrl(self ):
        controlerOut = self.PIDcontroler(self.Input)
        
        if abs(self.Input) < self.deadZoon: 
            controlerOut = 0 
#        if controlerOut < Vmin and controlerOut > 0:
#            controlerOut = Vmin
#        elif controlerOut > -1*Vmin and controlerOut < 0:
#            controlerOut = -1*Vmin
            
        if abs(controlerOut) > self.Vmax:   
            if controlerOut>0:
                controlerOut = self.Vmax
            else:
                controlerOut = -1*self.Vmax
                
        return controlerOut
