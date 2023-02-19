import numpy as np

class converter:

    def __init__(self,Vin,R2):
        self.Vin = Vin
        self.R2 = R2

    def convert(self,values):
        #buffer = np.multiply(values,self.Vin)
        #Vout = buffer #np.divide(buffer,1024.0)
        #buffer = np.divide(self.Vin,Vout) - 1
        #values = np.multiply(self.resist,buffer)
        #return values
         
        VR1 = self.Vin - np.multiply(values, self.Vin)
        VR2 = self.Vin - VR1
        resistances = np.multiply(VR1,self.R2)/VR2
        return resistances

if __name__ == "__main__":
    convert = converter(3.3,47)
    print(convert.convert([.004,.5]))