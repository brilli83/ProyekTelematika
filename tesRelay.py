import RPi.GPIO as GPIO
import time

# Pin Setup:
relay_pin = 17  # GPIO pin the relay is connected to
GPIO.setmode(GPIO.BCM)  # Use Broadcom SOC Pin numbers
GPIO.setup(relay_pin, GPIO.OUT)  # Set the pin as an output

try:
    while True:
        GPIO.output(relay_pin, GPIO.HIGH)  # Turn relay ON
        print("relay on")
        time.sleep(3)  # Wait for 3 seconds
        

        GPIO.output(relay_pin, GPIO.LOW)  # Turn relay OFF
        print("relay off")
        time.sleep(3)  # Wait for 3 seconds

except KeyboardInterrupt:
    # Clean up GPIO on CTRL+C exit
    GPIO.cleanup()

GPIO.cleanup()  # Clean up GPIO on normal exit
