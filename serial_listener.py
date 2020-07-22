import serial, time
from datetime import datetime

serialport = serial.Serial("/dev/ttyUSB0", 9600)

while True:    
    command = serialport.readline().rstrip()
    t = datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')
    print(t+" :: "+str(command))
    if(command.startswith('{uid')):
        file='output.txt' 
        with open(file, 'w') as f:
            f.write(command)
