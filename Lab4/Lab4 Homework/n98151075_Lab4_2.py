# import RPi.GPIO as GPIO
# import time

# # 設定使用 BCM 編號系統
# GPIO.setmode(GPIO.BCM)

# # 超聲波模組的 TRIG_y 與 ECHO_r 引腳設定
# TRIG_y =     # GPIO XX
# ECHO_r =     # GPIO XX


# # 設定引腳輸出入模式
# GPIO.setup(TRIG_y, GPIO.OUT)
# GPIO.setup(ECHO_r, GPIO.IN)


# def measure_distance():
#     # 確保發射端是關閉的，並稍作延遲讓感測器穩定
#     GPIO.output(TRIG_y, False)
#     time.sleep(0.5)

#     # 發送 10微秒 的高電位脈衝來觸發超聲波
#     GPIO.output(TRIG_y, True)
#     time.sleep(0.00001)
#     GPIO.output(TRIG_y, False)

#     # 等待 ECHO_r 高電位（1），並記錄起始時間
#     while GPIO.input(ECHO_r) == 0:
#         pulse_start = time.time()

#     # 等待 ECHO_r 變回低電位（0），並記錄結束時間
#     while GPIO.input(ECHO_r) == 1:
#         pulse_end = time.time()

#     # 計算脈衝持續時間，並根據音速轉換為距離（公分）
#     # 距離 = (時間 * 聲速 34300 cm/s) / 2
#     pulse_duration = pulse_end - pulse_start
#     distance = pulse_duration * 17150
#     distance = round(distance, 2)

#     return distance


# try:
#     print("程式啟動，按 Ctrl+C 可以停止測試...")

#     while True:

#         # LAB4-2
#         #
#         # 請在這裡加上判斷距離程式碼，並且輸出訊息
#         #
#         #


#         time.sleep(0.1)  # 稍微停一下，避免畫面跳太快

# except KeyboardInterrupt:
#     # 當你按下 Ctrl+C 時，會執行這裡
#     print("\n停止測量中...")

# finally:
#     # 清除 GPIO 設定，這步很重要，不然下次執行會噴錯誤
#     GPIO.cleanup()
#     print("GPIO 已清理，程式結束。")



import RPi.GPIO as GPIO
import time

# 設定使用 BCM 編號系統
GPIO.setmode(GPIO.BCM)

# 超音波模組的 TRIG 與 ECHO 引腳
TRIG_y = 23  # GPIO23，實體 Pin 16
ECHO_r = 24  # GPIO24，實體 Pin 18

# 設定引腳輸出入模式
GPIO.setup(TRIG_y, GPIO.OUT)
GPIO.setup(ECHO_r, GPIO.IN)


def measure_distance():
    # 確保發射端關閉
    GPIO.output(TRIG_y, False)
    time.sleep(0.5)

    # 發送 10 微秒的高電位脈衝
    GPIO.output(TRIG_y, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_y, False)

    timeout = time.monotonic() + 0.04

    # 等待 ECHO 變成高電位
    while GPIO.input(ECHO_r) == 0:
        if time.monotonic() > timeout:
            return None

    pulse_start = time.monotonic()
    timeout = pulse_start + 0.04

    # 等待 ECHO 變回低電位
    while GPIO.input(ECHO_r) == 1:
        if time.monotonic() > timeout:
            return None

    pulse_end = time.monotonic()

    # 計算距離（cm）
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150

    return round(distance, 2)


try:
    print("程式啟動，按 Ctrl+C 可以停止測試...")

    while True:
        # Lab 4-2：倒車雷達
        distance = measure_distance()

        if distance is None:
            print("測量失敗，請檢查感測器")
        elif distance < 20:
            print(f"距離: {distance:.2f} cm | 狀態: 注意！！！")
        else:
            print(f"距離: {distance:.2f} cm | 狀態: 沒事")

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n停止測量中...")

finally:
    GPIO.cleanup()
    print("GPIO 已清理，程式結束。")
