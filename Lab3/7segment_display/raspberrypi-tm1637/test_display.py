import tm1637
import time

tm = tm1637.TM1637(clk=4, dio=5)

tm.brightness(7)
tm.numbers(12, 59, True)

time.sleep(10)
