import serial
import adafruit_thermal_printer

# class Printer:
# 	def __init__(self, port):
# 		# ThermalPrinter = adafruit_thermal_printer.get_printer_class(2.69)
# 		# uart = serial.Serial(port, baudrate=19200, timeout=3000)
# 		# self.printer = ThermalPrinter(self.uart, auto_warm_up=False)

# 		# print("Connection initialized. Warming up...")
		

# 		# self.printer.warm_up()

# 	def print(self, text, port):
# 		# It's possible that this needs to be encoded as UTF-8, but so far... so good!
#         ThermalPrinter = adafruit_thermal_printer.get_printer_class(2.69)
# 		self.uart = serial.Serial(port, baudrate=19200, timeout=3000)
# 		self.printer = ThermalPrinter(self.uart, auto_warm_up=False)

# 		print("Connection initialized. Warming up...")
		

# 		self.printer.warm_up()
# 		self.printer.print(text)
# 		self.uart.close()

# 	def close(self):
# 		self.uart.close()

# The original code not as a class:
# ThermalPrinter = adafruit_thermal_printer.get_printer_class(2.69)
# uart = serial.Serial("/dev/tty.usbserial-AC01YBML", baudrate=19200, timeout=3000)
# printer = ThermalPrinter(uart, auto_warm_up=False)

# print("Connection initialized. Warming up...")

# printer.warm_up()

# printer.print("From FTDI: PLEASEEEEE")
# uart.close()


def printerHardcore(text, port):
    ThermalPrinter = adafruit_thermal_printer.get_printer_class(2.69)
    uart = serial.Serial(port, baudrate=19200, timeout=3000)
    printer = ThermalPrinter(uart, auto_warm_up=False)

    print("Connection initialized. Warming up...")

    printer.warm_up()
    printer.print(text)
    uart.close()