import board
import digitalio
import pwmio
from adafruit_motor import servo
from adafruit_debouncer import Debouncer
import time
import busio
import displayio
import adafruit_st7789
import terminalio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label

# Variables
carsParked = 0
maxCarsParked = 5

displayio.release_displays()

# Setup of SPI-bus and pins
spi = busio.SPI(clock=board.GP18, MOSI=board.GP19)
tft_cs = board.GP17  # Chip select
tft_dc = board.GP21  # Data/Command
tft_reset = board.GP20  # Reset

# Setup of ST7789 Display
display_bus = displayio.FourWire(
    spi, command=tft_dc, chip_select=tft_cs, reset=tft_reset
)
display = adafruit_st7789.ST7789(
    display_bus,
    width=240,
    height=240,
    rotation=90,  # Change rotation to your needs
    rowstart=80,   # Specific for 240x240 displays
)

splash = displayio.Group()
display.root_group = splash

font = bitmap_font.load_font("/fonts/Junction-regular-24.bdf")  # Path to your font file

# Create a text label
text_area = label.Label(
    font,
    text=f"Welcome!\nThere are\n{maxCarsParked} spots left",
    color=0xFFFFFF
)
text_area.x = (240 - text_area.bounding_box[2]) // 2  # Center horizontally
text_area.y = (240 - text_area.bounding_box[3]) // 2  # Center vertically

# Add the text label to the display group
splash.append(text_area)

# Buttons
buttonGatePin_1 = digitalio.DigitalInOut(board.GP2)
buttonGatePin_1.direction = digitalio.Direction.INPUT
buttonGatePin_1.pull = digitalio.Pull.UP
buttonGate_1 = Debouncer(buttonGatePin_1)

buttonGatePin_2 = digitalio.DigitalInOut(board.GP7)
buttonGatePin_2.direction = digitalio.Direction.INPUT
buttonGatePin_2.pull = digitalio.Pull.UP
buttonGate_2 = Debouncer(buttonGatePin_2)

buttonExitGatePin = digitalio.DigitalInOut(board.GP12)
buttonExitGatePin.direction = digitalio.Direction.INPUT
buttonExitGatePin.pull = digitalio.Pull.UP
buttonExitGate = Debouncer(buttonExitGatePin)
# Servo's
servoGatePin_1 = pwmio.PWMOut(board.GP3, duty_cycle=0, frequency=50)
servoGate_1 = servo.Servo(servoGatePin_1)
servoGate_1.angle = 90

servoGatePin_2 = pwmio.PWMOut(board.GP8, duty_cycle=0, frequency=50)
servoGate_2 = servo.Servo(servoGatePin_2)
servoGate_2.angle = 90
# LED's
greenLED_1 = digitalio.DigitalInOut(board.GP4)
greenLED_1.direction = digitalio.Direction.OUTPUT
greenLED_1.value = False

greenLED_2 = digitalio.DigitalInOut(board.GP9)
greenLED_2.direction = digitalio.Direction.OUTPUT
greenLED_2.value = False

redLED_1 = digitalio.DigitalInOut(board.GP5)
redLED_1.direction = digitalio.Direction.OUTPUT
redLED_1.value = True

redLED_2 = digitalio.DigitalInOut(board.GP10)
redLED_2.direction = digitalio.Direction.OUTPUT
redLED_2.value = True

exitLED = digitalio.DigitalInOut(board.GP13)
exitLED.direction = digitalio.Direction.OUTPUT
exitLED.value = False
# LED Strips
ledStrip_1 = digitalio.DigitalInOut(board.GP6)
ledStrip_1.direction = digitalio.Direction.OUTPUT
ledStrip_1.value = False

ledStrip_2 = digitalio.DigitalInOut(board.GP11)
ledStrip_2.direction = digitalio.Direction.OUTPUT
ledStrip_2.value = False

def openGate_1():
    global carsParked
    carsParked += 1
    checkSpots()
    print(f"Car parked. Total cars: {carsParked}")
    greenLED_1.value = True
    redLED_1.value = False
    servoGate_1.angle = 0
    ledStrip_1.value = True
    time.sleep(2)
    greenLED_1.value = False
    redLED_1.value = True
    servoGate_1.angle = 90
    ledStrip_1.value = False

def openGate_2():
    global carsParked
    carsParked += 1
    checkSpots()
    print(f"Car parked. Total cars: {carsParked}")
    greenLED_2.value = True
    redLED_2.value = False
    servoGate_2.angle = 0
    ledStrip_2.value = True
    time.sleep(2)
    greenLED_2.value = False
    redLED_2.value = True
    servoGate_2.angle = 90
    ledStrip_2.value = False

def checkSpots():
    emptySpots = maxCarsParked - carsParked
    if emptySpots > 0:
        updateText(f"Welcome!\nThere are\n{emptySpots} spot(s) left")
    else:
        updateText(f"Sorry!\nThere are\nno spots left")

def updateText(new_text):
    text_area.text = new_text  # Update the text on the screen
    text_area.x = (240 - text_area.bounding_box[2]) // 2  # Center horizontally
    text_area.y = (240 - text_area.bounding_box[3]) // 2  # Center vertically

while True:
    # Debounce the button
    buttonGate_1.update()
    buttonGate_2.update()
    buttonExitGate.update()

    if buttonGate_1.rose:
        if carsParked < maxCarsParked:
            openGate_1()
        else:
            redLED_1.value = False
            time.sleep(0.25)
            redLED_1.value = True
            time.sleep(0.25)
            redLED_1.value = False
            time.sleep(0.25)
            redLED_1.value = True
    elif buttonGate_2.rose:
        if carsParked < maxCarsParked:
            openGate_2()
        else:
            redLED_2.value = False
            time.sleep(0.25)
            redLED_2.value = True
            time.sleep(0.25)
            redLED_2.value = False
            time.sleep(0.25)
            redLED_2.value = True
    elif buttonExitGate.rose:
        if carsParked > 0:
            carsParked -= 1
            checkSpots()
            print(f"Car exited. Total cars: {carsParked}")
            exitLED.value = True
            time.sleep(0.5)
            exitLED.value = False

    time.sleep(0.01)  # Small delay
