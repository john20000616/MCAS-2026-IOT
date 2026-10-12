import serial
import time

# 設定 UART 連接埠與參數
ser = serial.Serial(
    port='/dev/serial0',       # GPIO14 (TX) 和 GPIO15 (RX)
    baudrate=9600,             # 傳輸速率
    timeout=1                  # 讀取逾時時間（秒）
)

# 傳送資料
def send_data(data):
    if ser.is_open:
        ser.write((data + "\n").encode('utf-8'))
        print(f"已傳送：{data}")

# 接收資料
def receive_data():
    if ser.is_open:
        incoming = ser.readline().decode('utf-8').strip()

        if incoming:
            print(f"收到資料：{incoming}")

            # 判斷收到的訊息並自動回覆
            if incoming == "台北順起來!":
                reply = "Future 順"
                print(f"自動回覆：{reply}")

        return incoming

# 主程式
try:
    print("UART 聊天系統啟動！")
    print("按 Ctrl+C 可以停止程式\n")

    while True:
        send_data("台北順起來!")
        time.sleep(1)

        receive_data()
        time.sleep(1)

except KeyboardInterrupt:
    print("\n程式中斷")

finally:
    if ser.is_open:
        ser.close()
        print("串列埠已關閉")
