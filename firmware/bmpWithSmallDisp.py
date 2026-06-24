import time
import framebuf 
from machine import Pin
from chineseNum import CHINESE_NUM_FONTS

PIN_CS   = 21 
PIN_DC   = 22  
PIN_RST  = 26 
PIN_BUSY = 27  

class EPD_1Inch54_3Color:
    # Accept  shared spi object from the main file constructor
    def __init__(self, shared_SPI_bus):
        self.cs   = Pin(PIN_CS, Pin.OUT, value=1)
        self.dc   = Pin(PIN_DC, Pin.OUT, value=0)
        self.rst  = Pin(PIN_RST, Pin.OUT, value=1)
        self.busy = Pin(PIN_BUSY, Pin.IN, Pin.PULL_DOWN)
        self.spi  = shared_SPI_bus

#all just lib stuff 
    def write_cmd(self, cmd):
        self.dc.value(0)
        self.cs.value(0)
        self.spi.write(bytes([cmd]))
        self.cs.value(1)
        
    def write_data(self, value):
        self.dc.value(1)
        self.cs.value(0)
        self.spi.write(bytes([value]))
        self.cs.value(1)
        
    def chkstatus(self):
        while self.busy.value() == 1:
            time.sleep_ms(50)
        
    def reset(self):
        self.rst.value(0)
        time.sleep_ms(200)
        self.rst.value(1)
        time.sleep_ms(200)
        
    def hw_init(self):
        self.reset()
        self.chkstatus()
        self.write_cmd(0x12) 
        self.chkstatus()
        
        self.write_cmd(0x01) 
        self.write_data(0xC7)
        self.write_data(0x00)
        self.write_data(0x00)
#make SURE this is 0x11 otherwise gibberish
        self.write_cmd(0x03) 
        self.write_data(0x11) 
        
        self.write_cmd(0x44) 
        self.write_data(0x00)
        self.write_data(0x18) 
        
        self.write_cmd(0x45) 
        self.write_data(0xC7)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        
        self.write_cmd(0x3C) 
        self.write_data(0x05)
        
        self.write_cmd(0x18) 
        self.write_data(0x80)
        
        self.write_cmd(0x4E) 
        self.write_data(0x00)
        self.write_cmd(0x4F) 
        self.write_data(0xC7)
        self.write_data(0x00)
        self.chkstatus()
        
    def update(self):
        self.write_cmd(0x22)
        self.write_data(0xF7)
        self.write_cmd(0x20)
        time.sleep(5) 
        self.chkstatus()

    def display_frame(self, black_buffer, red_buffer=None):
        self.write_cmd(0x24)
        for i in range(5000):
            self.write_data(black_buffer[i])
            
        self.write_cmd(0x26)
        for i in range(5000):
            if red_buffer is not None:
                self.write_data(red_buffer[i])
            else:
                self.write_data(0x00) 
        self.update()

    def sleep(self):
        self.write_cmd(0x10)
        self.write_data(0x01)
        time.sleep_ms(10)
        self.cs.value(1)


def num_to_chinese_digits(num_str):
    mapping = {
        '0': '〇', '1': '一', '2': '二', '3': '三', '4': '四',
        '5': '五', '6': '六', '7': '七', '8': '八', '9': '九',
    }
    converted = ""
    for char in num_str:
        if char in mapping:
            converted += mapping[char]
        else:
            converted += char
    return converted

def draw_hybrid_text(fb, text, start_x, start_y, color, scale=1):
 
    current_x = start_x
    
    for char in text:
        if char in CHINESE_NUM_FONTS:
            bitmap = CHINESE_NUM_FONTS[char]
            
            for row in range(16):
                byte_left = bitmap[row * 2]       # Left segment block byte
                byte_right = bitmap[row * 2 + 1]   # Right segment block byte
                
                for col in range(8):
                    if (byte_left & (0x01 << col)):
                        px = current_x + (col * scale)
                        py = start_y + (row * scale)
                        fb.fill_rect(px, py, scale, scale, color)
                
                for col in range(8):
                    if (byte_right & (0x01 << col)):
                        px = current_x + ((col + 8) * scale)
                        py = start_y + (row * scale)
                        fb.fill_rect(px, py, scale, scale, color)
                                
            current_x += 16 * scale
        else:
            current_x += 16 * scale

