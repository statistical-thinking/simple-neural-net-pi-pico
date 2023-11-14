##################################
# LINEAR SINGLE LAYER NEURAL NET #
##################################

from machine import Pin,SPI,PWM
import framebuf
import time
import os

# Farben definieren
RED = 0x00F8
GREEN = 0xE007
BLUE = 0x1F00
WHITE = 0xFFFF
BLACK = 0x0000

# Display initialisieren
class LCD_0inch96(framebuf.FrameBuffer):
    def __init__(self):
    
        self.width = 160
        self.height = 80
        
        self.cs = Pin(9,Pin.OUT)
        self.rst = Pin(12,Pin.OUT)
        self.cs(1)
        #pwm = PWM(Pin(13)) # Hintergrundbeleuchtung
        #pwm.freq(1000)        
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,10000_000,polarity=0, phase=0,sck=Pin(10),mosi=Pin(11),miso=None)
        self.dc = Pin(8,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.Init()
        self.SetWindows(0, 0, self.width-1, self.height-1)
        
    def reset(self):
        self.rst(1)
        time.sleep(0.2) 
        self.rst(0)
        time.sleep(0.2)         
        self.rst(1)
        time.sleep(0.2) 
        
    def write_cmd(self, cmd):
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))

    def write_data(self, buf):
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def backlight(self,value):
        pwm = PWM(Pin(13)) # Hintergrundbeleuchtung
        pwm.freq(1000)
        if value>=1000:
            value=1000
        data=int (value*65536/1000)       
        pwm.duty_u16(data)  
        
    def Init(self):
        self.reset() 
        self.backlight(10000)  
        
        self.write_cmd(0x11)
        time.sleep(0.12)
        self.write_cmd(0x21) 
        self.write_cmd(0x21) 

        self.write_cmd(0xB1) 
        self.write_data(0x05)
        self.write_data(0x3A)
        self.write_data(0x3A)

        self.write_cmd(0xB2)
        self.write_data(0x05)
        self.write_data(0x3A)
        self.write_data(0x3A)

        self.write_cmd(0xB3) 
        self.write_data(0x05)  
        self.write_data(0x3A)
        self.write_data(0x3A)
        self.write_data(0x05)
        self.write_data(0x3A)
        self.write_data(0x3A)

        self.write_cmd(0xB4)
        self.write_data(0x03)

        self.write_cmd(0xC0)
        self.write_data(0x62)
        self.write_data(0x02)
        self.write_data(0x04)

        self.write_cmd(0xC1)
        self.write_data(0xC0)

        self.write_cmd(0xC2)
        self.write_data(0x0D)
        self.write_data(0x00)

        self.write_cmd(0xC3)
        self.write_data(0x8D)
        self.write_data(0x6A)   

        self.write_cmd(0xC4)
        self.write_data(0x8D) 
        self.write_data(0xEE) 

        self.write_cmd(0xC5)
        self.write_data(0x0E)    

        self.write_cmd(0xE0)
        self.write_data(0x10)
        self.write_data(0x0E)
        self.write_data(0x02)
        self.write_data(0x03)
        self.write_data(0x0E)
        self.write_data(0x07)
        self.write_data(0x02)
        self.write_data(0x07)
        self.write_data(0x0A)
        self.write_data(0x12)
        self.write_data(0x27)
        self.write_data(0x37)
        self.write_data(0x00)
        self.write_data(0x0D)
        self.write_data(0x0E)
        self.write_data(0x10)

        self.write_cmd(0xE1)
        self.write_data(0x10)
        self.write_data(0x0E)
        self.write_data(0x03)
        self.write_data(0x03)
        self.write_data(0x0F)
        self.write_data(0x06)
        self.write_data(0x02)
        self.write_data(0x08)
        self.write_data(0x0A)
        self.write_data(0x13)
        self.write_data(0x26)
        self.write_data(0x36)
        self.write_data(0x00)
        self.write_data(0x0D)
        self.write_data(0x0E)
        self.write_data(0x10)

        self.write_cmd(0x3A) 
        self.write_data(0x05)

        self.write_cmd(0x36)
        self.write_data(0xA8)

        self.write_cmd(0x29) 
        
    def SetWindows(self, Xstart, Ystart, Xend, Yend): # Fenstergräße:0,0,159,79
        Xstart=Xstart+1
        Xend=Xend+1
        Ystart=Ystart+26
        Yend=Yend+26
        self.write_cmd(0x2A)
        self.write_data(0x00)              
        self.write_data(Xstart)      
        self.write_data(0x00)              
        self.write_data(Xend) 

        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(Ystart)
        self.write_data(0x00)
        self.write_data(Yend)

        self.write_cmd(0x2C) 
        
    def display(self):
    
        self.SetWindows(0,0,self.width-1,self.height-1)       
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)        

# Startbildschirm
if __name__=='__main__':

    lcd = LCD_0inch96()   
    lcd.fill(BLACK)   
    lcd.text("Single Layer",35,25,WHITE)
    lcd.text("Neural Network",25,45,WHITE)    
    lcd.display()
    
    lcd.hline(0,0,160,BLUE)
    lcd.hline(0,79,160,BLUE)
    lcd.vline(0,0,80,BLUE)
    lcd.vline(159,0,80,BLUE) 
    
    lcd.display()
    time.sleep(3)
    
    lcd.fill(BLACK)   
    lcd.text("L E A R N I N G",20,35,WHITE)
    lcd.display()
    
    lcd.hline(0,0,160,BLUE)
    lcd.hline(0,79,160,BLUE)
    lcd.vline(0,0,80,BLUE)
    lcd.vline(159,0,80,BLUE) 
    
    lcd.display()
    time.sleep(0.1)

# Neuronales Netzwerk
def add(x, y):
    if len(x) != len(y):
        print("Unpassendes Format")
        exit()
    else:
        z = [x[i] + y[i] for i in range(len(x))]
    return z

def sub(x, y):
    if len(x) != len(y):
        print("Unpassendes Format")
        exit()
    else:
        z = [x[i] - y[i] for i in range(len(x))]
    return z

def mul(x, y):
    z = [x[i] * y[i] for i in range(len(x))]
    return z

def div(x, y):
    if len(x) != len(y):
        print("Unpassendes Format")
        exit()
    else:
        z = [x[i] / y[i] for i in range(len(x))]
    return z

def pypow(x, y):
    z = [x[i] ** y for i in range(len(x))]
    return z

def ones1d(n):
    z = []
    for i in range(n):
        z.append(1)
    return z

def expand(val, n):
    z = []
    for i in range(n):
        z.append(val)
    return z

def random1d(strt, end, n):
    z = []
    import random
    for i in range(n):
        val = random.randint(strt, end)
        z.append(val)
    return z

def linear_regression(x, y, lr, niter):
    N = len(x)
    import random
    W = expand(random.randint(1, 6), N)
    b = []
    for i in range(N):
        b.append(0)

    for i in range(niter):
        ypred = add(mul(W, x), b)
        L = mul(div(ones1d(N), expand(N, N)), expand(sum(pypow(sub(y, ypred), 2)), N))
        dL_dW = mul(div(expand(-2, N), expand(N, N)), expand(sum(mul(sub(y, ypred), x)), N))
        dL_db = mul(div(expand(-2, N), expand(N, N)), expand(sum(sub(y, ypred)), N))
        W = sub(W, mul(expand(lr, N), dL_dW))
        b = sub(b, mul(expand(lr, N), dL_db))
        print("MSE - Verlustfunktion:" + str(L[0]))
        print("Epochen:" + str(i))

    global weight, intercept, mse
    mse = L[0]
    weight = W[0]
    intercept = b[0]
    return ypred

def linear_pred(x):
    y = add(mul(expand(weight, len(x)), x), expand(bias, len(x)))
    return y

# Training
x = [10,9,7,6,4,2]
y = [1,2,3,4,5,6]
predictions = linear_regression(x,y,0.0175,1001)
print("Intercept:" + str(intercept))
print("Regressionsgewicht:" + str(weight))
print("Geschätzte Werte:" + str(predictions))
grades = [ '%.0f' % elem for elem in predictions ]
print("Gerundete Werte:" + str(grades))
print("Tatsächliche Werte:" + str(y))

lcd.fill(BLACK)
lcd.text("Model Summary:",5,0,BLUE)
lcd.text("1K EPOs @ 0.0175 LR",5,10,WHITE)
lcd.text("MSE: " + str(mse),5,20,WHITE)
lcd.text("Intercept: " +  str(intercept),5,30,WHITE)
lcd.text("Weight: " +  str(weight),5,40,WHITE)
lcd.text("[A]:",5,60,BLUE)
lcd.text("Pred.",40,60,WHITE)
lcd.text("[B]:",85,60,BLUE)
lcd.text("Var.",120,60,WHITE)
lcd.display()
time.sleep(0.1)

KEY_CTRL=Pin(3,Pin.IN,Pin.PULL_UP)
KEY_LEFT= Pin(16,Pin.IN,Pin.PULL_UP)
KEY_A=Pin(15,Pin.IN,Pin.PULL_UP)
KEY_B=Pin(17,Pin.IN,Pin.PULL_UP)

while True:
    if (KEY_A.value() == 0):
        lcd.fill(BLACK)
        lcd.text("Predictions:",5,0,BLUE)
        lcd.text("for 10: " +  str(predictions[0]),5,10,WHITE)
        lcd.text("for 09: " +  str(predictions[1]),5,20,WHITE)
        lcd.text("for 07: " +  str(predictions[2]),5,30,WHITE)
        lcd.text("for 06: " +  str(predictions[3]),5,40,WHITE)
        lcd.text("for 04: " +  str(predictions[4]),5,50,WHITE)
        lcd.text("for 02: " +  str(predictions[5]),5,60,WHITE)
        lcd.display()
        time.sleep(0.1)
        
    if (KEY_B.value() == 0):
        lcd.fill(BLACK)
        lcd.text("Variables:",5,0,BLUE)
        lcd.text("[10] ~ [1.00]",5,10,WHITE)
        lcd.text("[09] ~ [2.00]",5,20,WHITE)
        lcd.text("[07] ~ [3.00]",5,30,WHITE)
        lcd.text("[06] ~ [4.00]",5,40,WHITE)
        lcd.text("[04] ~ [5.00]",5,50,WHITE)
        lcd.text("[02] ~ [6.00]",5,60,WHITE)
        lcd.display()
        time.sleep(0.1)
        
    if (KEY_CTRL.value() == 0):
        lcd.fill(BLACK)
        lcd.text("Model Summary:",5,0,BLUE)
        lcd.text("1K EPOs @ 0.0175 LR",5,10,WHITE)
        lcd.text("MSE: " + str(mse),5,20,WHITE)
        lcd.text("Intercept: " +  str(intercept),5,30,WHITE)
        lcd.text("Weight: " +  str(weight),5,40,WHITE)
        lcd.text("[A]:",5,60,BLUE)
        lcd.text("Pred.",40,60,WHITE)
        lcd.text("[B]:",85,60,BLUE)
        lcd.text("Var.",120,60,WHITE)
        lcd.display()
        time.sleep(0.1)
  
    if (KEY_LEFT.value() == 0):
        machine.reset()
