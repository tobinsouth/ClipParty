import serial
import adafruit_thermal_printer
from art import *

def printerHardcore(text, port):
    ThermalPrinter = adafruit_thermal_printer.get_printer_class(2.69)
    uart = serial.Serial(port, baudrate=19200, timeout=3000)
    printer = ThermalPrinter(uart, auto_warm_up=False)

    print("Connection initialized. Warming up...")

    printer.warm_up()
    printer.print(text2art("99F", font='graffiti'))
    printer.feed(1)
    printer.print(text)
    printer.feed(1)
    printer.print("OBEY, HUMAN")
    printer.feed(3)
    uart.close()