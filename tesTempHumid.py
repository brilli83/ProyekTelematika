import time
import board
import adafruit_ahtx0
import digitalio
import RPi.GPIO as GPIO
import tespub2
import json
from smbus2 import SMBus
from mlx90614 import MLX90614
from heartrate_monitor import HeartRateMonitor 
from baby_cry_detector import Baby_Cry_Detection


#relay initialization
relay_pin = 17   
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin, GPIO.OUT)

relay_pin2 = 27   
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin2, GPIO.OUT)

# Start the sensor
hr_monitor = HeartRateMonitor()
hr_monitor.start_sensor()

# Create instances of the first AHT10 sensor and MAX30102 sensor
i2c_aht10_1 = board.I2C()
aht10_sensor_1 = adafruit_ahtx0.AHTx0(i2c_aht10_1)
#max30102_sensor = adafruit_max30102.MAX30102(i2c_aht10_1)

# Create an instance of the second AHT10 sensor on a different I2C bus
i2c_aht10_2 = board.I2C()  # Use the default I2C bus for the second AHT10 sensor
aht10_sensor_2 = adafruit_ahtx0.AHTx0(i2c_aht10_2)

# Create an instance of the second AHT10 sensor on a different I2C bus
i2c_aht10_3 = board.I2C()  # Use the default I2C bus for the second AHT10 sensor
aht10_sensor_3 = adafruit_ahtx0.AHTx0(i2c_aht10_3)

# mlx90613 instance
bus = SMBus(1)
sensor = MLX90614(bus, address=0x5A)

try:
    while True:
        # Read temperature and humidity from the first AHT10 sensor
        temperature_1 = aht10_sensor_1.temperature
        humidity_1 = aht10_sensor_1.relative_humidity

        # read ambient temparature and object temperature from MLX90614
        ambient_temperature = sensor.get_amb_temp()
        object_temperature = sensor.get_obj_temp()
        
        # Read temperature and humidity from the second AHT10 sensor
        temperature_2 = aht10_sensor_2.temperature
        humidity_2 = aht10_sensor_2.relative_humidity

        # Read temperature and humidity from the second AHT10 sensor
        temperature_3 = aht10_sensor_3.temperature
        humidity_3 = aht10_sensor_3.relative_humidity
        
        avg_temperature = (temperature_1 + temperature_2 + temperature_3 + ambient_temperature) / 4
        avg_humidity = (humidity_1 + humidity_2 + humidity_3) / 3

        # Call Baby_Cry_Detection and get the result
        emotion_id = Baby_Cry_Detection()
        
        # Display the measurements
        print("Sensor 1:")
        print(f"Temperature: {temperature_1:.2f}°C")
        print(f"Humidity: {humidity_1:.2f}%")
        #print(f"SpO2: {spo2}%")
        #print(f"Heart Rate: {heart_rate} BPM")

        print("Sensor 2:")
        print(f"Temperature: {temperature_2:.2f}°C")
        print(f"Humidity: {humidity_2:.2f}%")
        
        print("Sensor 3:")
        print(f"Temperature: {temperature_3:.2f}°C")
        print(f"Humidity: {humidity_3:.2f}%")

        print("Sensor MLX90614:")
        print(f"Ambient Temperature: {ambient_temperature:.2f}°C")
        
        print("BPM:", hr_monitor.bpm)
        print("SpO2:", hr_monitor.spo2)


        print(f"Avg Temperature: {avg_temperature:.2f}°C")
        print(f"Avg Humidity: {avg_humidity:.2f}%")
        print(f"Object Temperature: {object_temperature:.2f}°C")
       
        string = { "temperature_incubator": avg_temperature, "temperature_baby": object_temperature , "humidity": avg_humidity, "heart_rate": hr_monitor.bpm, "spo2": hr_monitor.spo2, "emotion_id" : emotion_id} 
        
        data = json.dumps(string)

        tespub2.publish_data(data)
        
        #relay to control lamp
        if avg_temperature < 25:
            # Turn on the relay
            GPIO.output(relay_pin, GPIO.HIGH)
            print("HEATER LAMP ON")
        else:
            # Turn off the relay
            GPIO.output(relay_pin, GPIO.LOW)
            print("HEATER LAMP OFF")
            
        # relay to control humidifier
        if avg_humidity < 60:
            # Turn on the relay
            GPIO.output(relay_pin2, GPIO.HIGH)
            print("HUMIDIFIER ON")
        else:
            # Turn off the relay_id"
            GPIO.output(relay_pin2, GPIO.LOW)
            print("HUMIDIFIER OFF")    
            
        # Wait for a while before taking the next reading
        time.sleep(6)

except KeyboardInterrupt:
    GPIO.cleanup()  # Clean up GPIO on keyboard interrupt
