import time
from smbus2 import SMBus
from mlx90614 import MLX90614

def read_temperature(sensor):
    ambient_temperature = sensor.get_amb_temp()
    object_temperature = sensor.get_obj_temp()  # Assuming this is the correct method name

    return ambient_temperature, object_temperature

def main():
    bus = SMBus(1)
    sensor = MLX90614(bus, address=0x5A)

    try:
        while True:
            ambient, object_temp = read_temperature(sensor)
            print(f"Ambient Temperature: {ambient}°C")
            print(f"Object Temperature: {object_temp}°C")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program stopped by user.")
    finally:
        bus.close()

if __name__ == "__main__":
    main()
