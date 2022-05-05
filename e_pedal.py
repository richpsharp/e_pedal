"""Read a key and send it to keyboard."""
import argparse
import sys

import keyboard
import serial


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    ports = ['COM%s' % (i + 1) for i in range(256)]
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Listen for serial and send to keyboard.')
    parser.add_argument('--com_port', default=None, help='com port to listen on')
    args = parser.parse_args()

    if args.com_port is None:
        active_serial_ports = serial_ports()
        print(
            f'Error: specify a --com_port, these are active: '
            f'{active_serial_ports}')
        sys.exit(-1)

    ser = serial.Serial(args.com_port, 9600)
    while True:
        key = ser.readline().decode().rstrip()
        keyboard.write(key)
