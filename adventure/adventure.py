########################
# HELL - THE ADVENTURE #
########################

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
        
    def SetWindows(self, Xstart, Ystart, Xend, Yend):
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

# Steuerung
# KEY_CTRL=Pin(3,Pin.IN,Pin.PULL_UP)
KEY_LEFT= Pin(16,Pin.IN,Pin.PULL_UP)
KEY_RIGHT= Pin(20,Pin.IN,Pin.PULL_UP)
# KEY_UP = Pin(2,Pin.IN,Pin.PULL_UP)
# KEY_DOWN = Pin(18,Pin.IN,Pin.PULL_UP)
KEY_A=Pin(15,Pin.IN,Pin.PULL_UP)
KEY_B=Pin(17,Pin.IN,Pin.PULL_UP)

# GamePlay
def choose_character():
     while True:
         if (KEY_A.value() == 0):
             lcd.fill(BLACK)
             lcd.text("Good choice.",10,10,WHITE)
             lcd.text("The Slayer is",10,25,WHITE)
             lcd.text("strong.",10,40,WHITE)
             lcd.hline(0,0,160,BLUE)
             lcd.hline(0,79,160,BLUE)
             lcd.vline(0,0,80,BLUE)
             lcd.vline(159,0,80,BLUE)
             lcd.display()
             time.sleep(3)
             
             hell_entrance()
        
         elif (KEY_B.value() == 0):
             lcd.fill(BLACK)
             lcd.text("BOB IS WEAK.",10,10,RED)
             lcd.text("YOU ARE DEAD!",10,25,RED)
             lcd.hline(0,0,160,RED)
             lcd.hline(0,79,160,RED)
             lcd.vline(0,0,80,RED)
             lcd.vline(159,0,80,RED)
             lcd.display()
             time.sleep(3)
             
             machine.reset()

def hell_entrance():
    lcd.fill(BLACK)
    lcd.text("You approach HELL.",10,10,WHITE)
    lcd.text("Do you enter?",10,25,WHITE)
    lcd.text("[A]:",5,60,BLUE)
    lcd.text("Yes",40,60,WHITE)
    lcd.text("[B]:",75,60,BLUE)
    lcd.text("No",110,60,WHITE)
    lcd.hline(0,0,160,BLUE)
    lcd.hline(0,79,160,BLUE)
    lcd.vline(0,0,80,BLUE)
    lcd.vline(159,0,80,BLUE)
    lcd.display()
    time.sleep(0.1)
    
    while True:
        if (KEY_A.value() == 0):
            inside_hell()
        
        elif (KEY_B.value() == 0):
            lcd.fill(BLACK)
            lcd.text("YOU ARE A COWARD.",10,10,RED)
            lcd.text("YOU WILL DIE",10,25,RED)
            lcd.text("OF OLD AGE!",10,40,RED)
            lcd.hline(0,0,160,RED)
            lcd.hline(0,79,160,RED)
            lcd.vline(0,0,80,RED)
            lcd.vline(159,0,80,RED)
            lcd.display()
            time.sleep(3)
            
            machine.reset()

def inside_hell():
    lcd.fill(BLACK)
    lcd.text("You are in HELL.",10,10,WHITE)
    lcd.text("Where do you go?",10,25,WHITE)
    lcd.text("[L]:",5,60,BLUE)
    lcd.text("Left",40,60,WHITE)
    lcd.text("[R]:",77,60,BLUE)
    lcd.text("Right",112,60,WHITE)
    lcd.hline(0,0,160,BLUE)
    lcd.hline(0,79,160,BLUE)
    lcd.vline(0,0,80,BLUE)
    lcd.vline(159,0,80,BLUE)
    lcd.display()
    time.sleep(0.1)
    
    while True:
        if (KEY_RIGHT.value() == 0):
            lcd.fill(BLACK)
            lcd.text("IT'S A TRAP.",10,10,RED)
            lcd.text("YOU ARE DEAD!",10,25,RED)
            lcd.hline(0,0,160,RED)
            lcd.hline(0,79,160,RED)
            lcd.vline(0,0,80,RED)
            lcd.vline(159,0,80,RED)
            lcd.display()
            time.sleep(3)
            
            machine.reset()
        
        elif (KEY_LEFT.value() == 0):
            boss_fight()
        
def boss_fight():
    lcd.fill(BLACK)
    lcd.text("You move forward",10,10,WHITE)
    lcd.text("like a hero...",10,25,WHITE)
    lcd.hline(0,0,160,BLUE)
    lcd.hline(0,79,160,BLUE)
    lcd.vline(0,0,80,BLUE)
    lcd.vline(159,0,80,BLUE)
    lcd.display()
    time.sleep(3)
    
    lcd.fill(BLACK)
    lcd.text("It's the DEVIL!",10,10,WHITE)
    lcd.text("What do you do?",10,25,WHITE)
    lcd.text("[A]:",5,60,BLUE)
    lcd.text("Fight",40,60,WHITE)
    lcd.text("[B]:",85,60,BLUE)
    lcd.text("Run",120,60,WHITE)
    lcd.hline(0,0,160,BLUE)
    lcd.hline(0,79,160,BLUE)
    lcd.vline(0,0,80,BLUE)
    lcd.vline(159,0,80,BLUE)
    lcd.display()
    time.sleep(0.1)
    
    while True:
        if (KEY_A.value() == 0):         
            final_battle()
        
        elif (KEY_B.value() == 0):
            lcd.fill(BLACK)
            lcd.text("The DEVIL is fast.",10,10,RED)
            lcd.text("YOU ARE DEAD!",10,25,RED)
            lcd.hline(0,0,160,RED)
            lcd.hline(0,79,160,RED)
            lcd.vline(0,0,80,RED)
            lcd.vline(159,0,80,RED)
            lcd.display()
            time.sleep(3)
            
            machine.reset()           

def final_battle():
    lcd.fill(BLACK)
    lcd.text("Flames and rage",10,10,WHITE)
    lcd.text("surround you...",10,25,WHITE)
    lcd.hline(0,0,160,BLUE)
    lcd.hline(0,79,160,BLUE)
    lcd.vline(0,0,80,BLUE)
    lcd.vline(159,0,80,BLUE)
    lcd.display()
    time.sleep(3)
    
    lcd.fill(BLACK)
    lcd.text("Choose your",10,10,WHITE)
    lcd.text("weapon wisely:",10,25,WHITE)
    lcd.text("[A]:",5,60,BLUE)
    lcd.text("Bible",40,60,WHITE)
    lcd.text("[B]:",85,60,BLUE)
    lcd.text("Fist",120,60,WHITE)
    lcd.hline(0,0,160,BLUE)
    lcd.hline(0,79,160,BLUE)
    lcd.vline(0,0,80,BLUE)
    lcd.vline(159,0,80,BLUE)
    lcd.display()
    time.sleep(0.1)

    while True:
        if (KEY_B.value() == 0):     
            happy_ending()
            
        elif (KEY_A.value() == 0):
            lcd.fill(BLACK)
            lcd.text("THE HOLY BIBLE",10,10,RED)
            lcd.text("BURNS IN HELL.",10,25,RED)
            lcd.text("YOU ARE DEAD!",10,40,RED)
            lcd.hline(0,0,160,RED)
            lcd.hline(0,79,160,RED)
            lcd.vline(0,0,80,RED)
            lcd.vline(159,0,80,RED)
            lcd.display()
            time.sleep(3)
            
            machine.reset()      

def happy_ending():
    lcd.fill(BLACK)
    lcd.text("You killed the",10,10,WHITE)
    lcd.text("DEVIL and saved",10,25,WHITE)
    lcd.text("the world...",10,40,WHITE)
    lcd.hline(0,0,160,BLUE)
    lcd.hline(0,79,160,BLUE)
    lcd.vline(0,0,80,BLUE)
    lcd.vline(159,0,80,BLUE)
    lcd.display()
    time.sleep(3)
    
    lcd.fill(BLACK)
    lcd.text("THIS TIME...",10,10,RED)
    lcd.text("HARRR, HARRR...",10,25,RED)
    lcd.hline(0,0,160,RED)
    lcd.hline(0,79,160,RED)
    lcd.vline(0,0,80,RED)
    lcd.vline(159,0,80,RED)
    lcd.display()
    time.sleep(3)
    
    machine.reset()

# Startbildschirm
if __name__=='__main__':

    lcd = LCD_0inch96()
    lcd.fill(BLACK)
    lcd.text("H E L L",50,25,RED)
    lcd.text("THE ADVENTURE",25,45,RED)
    lcd.display()
    
    lcd.hline(0,0,160,RED)
    lcd.hline(0,79,160,RED)
    lcd.vline(0,0,80,RED)
    lcd.vline(159,0,80,RED) 
    
    lcd.display()
    time.sleep(2)
    
    lcd.fill(BLACK)
    lcd.text("Welcome! Choose",10,10,WHITE)
    lcd.text("your character:",10,25,WHITE)
    lcd.text("[A]:",5,60,BLUE)
    lcd.text("Slayer",40,60,WHITE)
    lcd.text("[B]:",92,60,BLUE)
    lcd.text("Bob",127,60,WHITE)
    lcd.display()
    
    lcd.hline(0,0,160,BLUE)
    lcd.hline(0,79,160,BLUE)
    lcd.vline(0,0,80,BLUE)
    lcd.vline(159,0,80,BLUE)
    
    lcd.display()
    time.sleep(0.1)
    
    choose_character()
