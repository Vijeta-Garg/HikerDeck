import time
from machine import I2C, Pin, Timer
import Pico_ePaper_2_7_V2
import gc 
import bmp280

# ==========================================
# 1. INITIALIZE HARDWARE CONFIGURATION
# ==========================================
epd = Pico_ePaper_2_7_V2.EPD_2in7_V2()

CHARS_PER_LINE = 21         
LINES_PER_PAGE = 19         
current_page = 0 
page_needs_update = False  
sensor_needs_read = False    
total_pages = 0              # Stores the pre-calculated page count

i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=100000)
bmp = bmp280.BMP280(i2c)
bmp.oversample(bmp280.BMP280_OS_HIGH)
bmp.use_case(bmp280.BMP280_CASE_WEATHER)

gc.collect()

cs_small = Pin(21, Pin.OUT)
cs_small.value(1)

# ==========================================
# 2. ULTRA-LOW RAM TEXT STREAMING ENGINE
# ==========================================
def stream_words_from_file(filename="longDistanceTrails.txt"):
    """Reads a file chunk-by-chunk and yields one single word at a time."""
    try:
        with open(filename, "r") as f:
            buffer = ""
            while True:
                chunk = f.read(64) # Read tiny 64-byte chunks
                if not chunk:
                    if buffer:
                        yield buffer
                    break
                
                buffer += chunk
                words = buffer.split()
                
                # If the chunk ended mid-word, save the last part for the next read
                if not chunk.endswith((" ", "\n", "\r", "\t")):
                    buffer = words.pop() if words else ""
                else:
                    buffer = ""
                    
                for word in words:
                    yield word
    except OSError:
        print("File not found!")

def get_page_content(target_page_num):
    """Processes the text stream and returns ONLY the text for the requested page number."""
    current_line = ""
    current_page_lines = []
    page_counter = 0
    
    gc.collect()
    
    for word in stream_words_from_file():
        if len(current_line) + len(word) + (1 if current_line else 0) <= CHARS_PER_LINE:
            current_line += (" " if current_line else "") + word
        else:
            if current_line:
                current_page_lines.append(current_line)
            current_line = word
            
            if len(current_page_lines) == LINES_PER_PAGE:
                if page_counter == target_page_num:
                    return "\n".join(current_page_lines)
                page_counter += 1
                current_page_lines = []
                gc.collect()

    if current_line:
        current_page_lines.append(current_line)
        
    if current_page_lines and page_counter == target_page_num:
        return "\n".join(current_page_lines)
        
    return "--- End of Document ---"

def precalculate_total_pages():
    """Counts total layout pages on boot without saving data to lists."""
    global total_pages
    current_line = ""
    line_count = 0
    page_count = 0
    has_words = False
    
    for word in stream_words_from_file():
        has_words = True
        if len(current_line) + len(word) + (1 if current_line else 0) <= CHARS_PER_LINE:
            current_line += (" " if current_line else "") + word
        else:
            line_count += 1
            current_line = word
            if line_count == LINES_PER_PAGE:
                page_count += 1
                line_count = 0
                
    if current_line:
        line_count += 1
    if line_count > 0 or (page_count == 0 and not has_words):
        page_count += 1
        
    total_pages = page_count
    print(f"File scanned! Total Pages: {total_pages}")

# Pre-calculate the total count on bootup
precalculate_total_pages()

# ==========================================
# 3. INTERRUPT HANDLERS (Safe, no memory allocation)
# ==========================================
def next_page_handler(pin):
    global current_page, page_needs_update
    if not page_needs_update:
        if current_page + 1 < total_pages:
            current_page += 1
            page_needs_update = True

def prev_page_handler(pin):
    global current_page, page_needs_update
    if not page_needs_update:
        if current_page > 0:
            current_page -= 1
            page_needs_update = True

key_next = Pin(7, Pin.IN, Pin.PULL_UP)
key_next.irq(trigger=Pin.IRQ_FALLING, handler=next_page_handler)

key_prev = Pin(6, Pin.IN, Pin.PULL_UP)
key_prev.irq(trigger=Pin.IRQ_FALLING, handler=prev_page_handler)

def timer_sensor_cb(t):
    global sensor_needs_read
    sensor_needs_read = True

timer_b = Timer(period=1000, mode=Timer.PERIODIC, callback=timer_sensor_cb)

# ==========================================
# 4. EXECUTION FUNCTIONS
# ==========================================
def senseAlt():
    print("pressure: {}Pa".format(bmp.pressure))
    print("altitude: {}".format(bmp.altitude))

def render_page(page_num):
    print(f"Streaming Page {page_num + 1} onto SPI lines...")
    epd.image1Gray_Portrait.fill(0xff) 
    epd.image1Gray_Portrait.text(f"PAGE {page_num + 1} of {total_pages}", 5, 5, epd.black)
    epd.image1Gray_Portrait.hline(5, 15, 166, epd.black)
    
    # Extract only the current page's text from the file stream directly
    text_to_draw = get_page_content(page_num)
    lines = text_to_draw.split("\n")
    
    current_y = 22
    for line in lines:
        epd.image1Gray_Portrait.text(line, 5, current_y, epd.black)
        current_y += 12 
    
    epd.clear() 
    time.sleep(0.3) 
    epd.display(epd.buffer_1Gray_Portrait) 
    gc.collect()

# ==========================================
# 5. EXECUTION RUNTIME ROUTINE
# ==========================================
render_page(current_page)

while True:
    if page_needs_update:
        render_page(current_page)
        time.sleep(1.0) # Hardware debouncing window
        print("Free RAM:", gc.mem_free())
        page_needs_update = False  

    if sensor_needs_read:
        senseAlt()
        sensor_needs_read = False

    time.sleep(0.05)