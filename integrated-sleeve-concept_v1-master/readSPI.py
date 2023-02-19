import time
import os
import numpy as np

class mcp:

    def __init__(self,IP,port,device):

        os.environ["GPIOZERO_PIN_FACTORY"] = "pigpio"
        os.environ["PIGPIO_ADDR"]=IP
        from gpiozero import MCP3008
        self.channels = {}
        for i in range(0,8):
            self.channels[i] = MCP3008(channel=i, device = device, port = port)

    def output(self):
        #import gpiozero
        #self.led=gpiozero.LED(17)
        #self.led.on()
        data = np.zeros((8,))
        for i in range(len(self.channels)):
            data[i]=self.channels[i].value
        #self.led.off()
        #self.led.close()
        return data



if __name__ == "__main__":
    mcp0 = mcp('10.201.15.178',0,0)
    while True:
        print(mcp0.output())

 