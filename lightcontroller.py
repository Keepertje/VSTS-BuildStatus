from gpiozero import LED
import config as cfg

def getCode(value):
    value = value.lower()
    return cfg.gpios.get(value, cfg.gpios.get('red'))

red = LED(getCode('red'))
yellow = LED(getCode('yellow'))
green = LED(getCode('green'))

def setAllOff():
    red.off()
    yellow.off()
    green.off()
    return

def setYellowBlinking(speed):
    setAllOff()
    yellow.blink(speed)
    return

def setRedOn():
    setAllOff()
    red.on()
    return

def setGreenOn():
    setAllOff()
    green.on()
    return
