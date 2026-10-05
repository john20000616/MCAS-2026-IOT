#!/usr/bin/env python3

import sys
from pathlib import Path
from time import sleep, localtime

# 找到 Lab3/7segment_display/raspberrypi-tm1637
LIB_PATH = (
    Path(__file__).resolve().parent.parent
    / "7segment_display"
    / "raspberrypi-tm1637"
)

sys.path.insert(0, str(LIB_PATH))

from tm1637 import TM1637

CLK = 23
DIO = 24

tm = TM1637(clk=CLK, dio=DIO)
tm.brightness(7)

show_colon = False

try:
    while True:
        t = localtime()

        show_colon = not show_colon

        tm.numbers(
            t.tm_hour,
            t.tm_min,
            show_colon
        )

        sleep(1)

except KeyboardInterrupt:
    tm.write([0, 0, 0, 0])