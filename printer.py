import serial
import adafruit_thermal_printer
from art import *

clip_small= """
        ,@*\"\"\"*g
        ,,gF      ]&
    y@*[J$$\"     ,g,
    y`,gNgg \",  ,w&Z$Bg
    \ ]@@@@  @` g@@N '$*
    ^~wwe\" ]  N@@@` /
        ][ ,   `^mr^\"-
        ][ $     $F /F
        ][ $     ]L $
        ]$ $     ]F]F
        $ ]k    $F]F
        $  \"k, ,@ ]F
        ]k   `\"'  ]F
        ]k       $
            '&w, ,$\"
            '\"\"\"
"""

def printerHardcore(text, user, port):
    ThermalPrinter = adafruit_thermal_printer.get_printer_class(2.69)
    uart = serial.Serial(port, baudrate=19200, timeout=3000)
    printer = ThermalPrinter(uart, auto_warm_up=False)

    print("Connection initialized. Warming up...")

    printer.warm_up()
    printer.print(text2art("99F", font='graffiti'))
    printer.feed(1)
    printer.print(text)
    printer.feed(1)
    printer.print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    printer.print(f'OBEY, HUMAN {user.upper()}')
    printer.feed(3)
    uart.close()