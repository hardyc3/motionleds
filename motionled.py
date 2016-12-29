import RPi.GPIO as GPIO
import signal
import sys
import time
import random

class MotionLED: 

    YELLOW_LED = 33
    RED_LED = 35
    GREEN_LED = 37
    MOTION_SENSOR = 32
    NEEDS_CLEANUP = False

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(MotionLED.YELLOW_LED, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(MotionLED.RED_LED, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(MotionLED.GREEN_LED, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(MotionLED.MOTION_SENSOR, GPIO.IN)
        MotionLED.NEEDS_CLEANUP = True
        print("running init")

    def motion_callback(self, channel):
        GPIO.output(MotionLED.YELLOW_LED, GPIO.HIGH)

    def game_loop(self):
        try:
            while True:
                #set random time for green light
                print("starting loop")
                waitTime = random.randint(2, 7)
                GPIO.output(MotionLED.GREEN_LED, GPIO.HIGH)
                time.sleep(waitTime)
                #when timer ends set random time for red light, watch for motion
                waitTime = random.randint(3, 7)
                print("turning on red")
                GPIO.output(MotionLED.RED_LED, GPIO.HIGH)
                GPIO.output(MotionLED.GREEN_LED, GPIO.LOW)
                #if motion during red light, light yellow light
                #give just a little time to stop moving before we cound it against them
                time.sleep(1)
                GPIO.add_event_detect(MotionLED.MOTION_SENSOR, GPIO.RISING, callback=self.motion_callback)
                    
                time.sleep(waitTime)
                print("turning off red and yellow")
                GPIO.output(MotionLED.RED_LED, GPIO.LOW)
                GPIO.output(MotionLED.YELLOW_LED, GPIO.LOW)
                GPIO.remove_event_detect(MotionLED.MOTION_SENSOR)
        except:
            print("error", sys.exc_info()[0])
            self.shutdown()

    def shutdown(self):
        if MotionLED.NEEDS_CLEANUP:
            print("Cleaning up GPIO")
            GPIO.cleanup()
            MotionLED.NEEDS_CLEANUP = False

app = None

def signal_handler(signal, frame):
    print("Shutting down game")
    if(app != None):
        app.shutdown()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    print("Press Ctrl+C to stop game.")
    app = MotionLED()
    app.game_loop()
