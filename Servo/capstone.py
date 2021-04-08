import serial

ser = serial.Serial('/dev/ttyACM0',9600)
string = "fuck you!\n"
string_encode = string.encode()
ser.write(string_encode)
