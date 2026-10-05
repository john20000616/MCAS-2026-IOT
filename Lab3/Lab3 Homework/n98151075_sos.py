import RPi.GPIO as GPIO
import time

LED_PIN = 11
BUZZER_PIN = 13
FREQ = 523

SHORT = 0.3
LONG = 0.9
GAP = 0.3

GPIO.setmode(GPIO.BOARD)

GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

buzzer = GPIO.PWM(BUZZER_PIN, FREQ)
buzzer.start(0)


def signal(duration):
    # LED 和蜂鳴器同時開
    GPIO.output(LED_PIN, GPIO.HIGH)
    buzzer.ChangeDutyCycle(50)

    time.sleep(duration)

    # LED 和蜂鳴器同時關
    GPIO.output(LED_PIN, GPIO.LOW)
    buzzer.ChangeDutyCycle(0)

    time.sleep(GAP)


try:
    print("S")
    for i in range(3):
        signal(SHORT)

    print("O")
    for i in range(3):
        signal(LONG)

    print("S")
    for i in range(3):
        signal(SHORT)

finally:
    buzzer.stop()
    GPIO.output(LED_PIN, GPIO.LOW)
    GPIO.cleanup()
