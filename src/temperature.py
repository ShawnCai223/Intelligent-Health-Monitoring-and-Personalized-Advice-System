import time
import board
import busio
import adafruit_mlx90614

def read_avg_temperature(duration_sec=5):
    i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
    mlx = adafruit_mlx90614.MLX90614(i2c)
    object_list = []

    start_time = time.time()
    while time.time() - start_time < duration_sec:
        try:
            object_temp = mlx.object_temperature
            object_list.append(object_temp)
            print(f"Temperature: {object_temp:.2f} °C", end="\r")
        except Exception:
            pass
        time.sleep(1)

    if not object_list:
        return None
    return sum(object_list) / len(object_list)