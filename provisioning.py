import time
import threading
from serial import Serial
from multiprocessing import queues
import sys, getopt
from constants import (setFirmware, setPackage)

class ModemResponse:
    OK = "OK"
    ERROR = "ERROR"
    CONNECT = "CONNECT"
    NOCARRIER = "NO CARRIER"
    PROMPT = ">"
    CMGS = "+CMGS:"
    CREG = "+CREG:"

class ModemData:
    Success = False
    Data = ModemResponse.OK

# start_time = 0.0
# end_time = 0.0
device = ""
ser = None
baud = 115200
apn = ""
server = ""
port = ""
deviceid = ""
callbackFunc = None
timeout_max = 5.0
device = ""

def exit():
    sys.exit()

def usage():
    print("-d/--device - device location")
    print("-s/--script - script location")
    print("-i/--deviceid - the devices id (separated by commas)")
    print("-p/--params - the params kore file location")

def handler(cmds, fileName):
    error_count = 0
    escape_loop = False
    # check to see if serial is already open if so close
    
    fileOpened = open(fileName, 'a')
    for key in cmds["cfg"]:
        tmp_buffer = b""
        escape_loop = False
        # store the command and expected response for later use
        cmd = key[0]
        print("cmd: ", cmd)
        rsp = key[1]
        # log
        # print("cmd: ", cmd)
        print("rsp: ", rsp)
        if rsp == "COMMENT" or rsp == "BLANK":
            print("Commented or empty string")
            fileOpened.write("{0}\r\n".format(cmd))
            continue
        
        # send command to modem
        send(cmd)
        if cmd == "AT\r":
            ""
        else:
            fileOpened.write("SND: {0}\r\n".format(cmd))
        # Reset start_time
        start_time = time.time()
        while(True):
            if (escape_loop == True):
                break
            
            # process timeout of command
            if ((time.time() - start_time) > timeout_max):
                print("timedout")
                break
            # process the modem's response
            while(ser.in_waiting > 0):
                # inefficient, but read one character at a time
                # TODO: refactor to read all bytes in serial buffer
                tmp_char = ser.read(1)
                if(tmp_char == b'\r'):
                    if not tmp_buffer or tmp_buffer.decode() == '\n':
                        tmp_buffer = b''
                        continue
                    # parse the accumulated buffer
                    if not (len(tmp_buffer) > 0):
                        continue

                    result = parse(tmp_buffer, rsp.encode())
                    print ('received ', tmp_buffer)
                    if tmp_buffer.count(b'.') == 3:
                        firmwarev = tmp_buffer.decode()
                        setFirmware(firmwarev)
                        tmp_buffer = tmp_buffer.decode().replace('\n', "")
                        tmp_buffer = tmp_buffer.replace('\r', "")
                        fileOpened.write("RCV: {0}\r\n".format(tmp_buffer))
                        tmp_buffer = b''
                        continue
                    # Check to see if we received what we were expecting
                    if(result.Success == True):
                        print("success")
                        if(callbackFunc != None):
                            callbackFunc(result)
                        # Escape time timeout loop
                        escape_loop = True
                    else:
                        error_count += 1
                        # print("error: cmd: ", cmd, " rsp: ", result.Data)
                    if cmd == "AT\r":
                        tmp_buffer = b''
                        continue
                    else:
                        print("tmp_buffer before: {0}".format(tmp_buffer))
                        tmp_buffer = tmp_buffer.decode().replace('\n', "")
                        tmp_buffer = tmp_buffer.replace('\r', "")
                        print("tmp_buffer: {0}".format(tmp_buffer))
                        fileOpened.write("RCV: {0}\r\n".format(tmp_buffer))
                        tmp_buffer= b""
                else:
                    tmp_buffer += tmp_char
                
            # let outer while loop breathe
            time.sleep(.005)
    fileOpened.close()

def parse(result, expect):

    data = ModemData()
    data.Data = result
    if (result.find(expect) > -1):
        data.Success = True
    else:
        print("failed")
        data.Success = False
    
    return data

"""
Write command to device
"""
def send(cmd):
    # Debug
    # print('sending command: ', cmd)
    # print(cmd.encode())
    ser.write(cmd.encode())

def modemDataReceived(data):
    print('Callback function modemDataReceived ', data)

def getFirmware(fileName, device):
    cmds = {"cfg": [["AT\r", "OK"], ["AT+CGMR\r", "OK"]]}
    fileOpened = open(fileName, "a")
    global ser
    if ser == None:
        ser = Serial(device, baudrate=115200, parity='N', stopbits=1, bytesize=8, xonxoff=0, rtscts=0)
        fileOpened.write("Port opened.\r\n")
    fileOpened.write("## Get Firmware Version.\r\n")
    fileOpened.close()
    handler(cmds, fileName)

def getPackage(fileName, device):
    fileOpened = open(fileName, 'a')
    cmd = "AT$PKG?\r"
    fileOpened.write("### Get Package.\r\n")
    fileOpened.write("SND: {0}\r\n".format(cmd.strip('\r')))
    send(cmd)
    time.sleep(.05)
    tmp_buffer = b""
    cmd = cmd.strip('\r')
    result = ""
    while ser.in_waiting > 0:
        char = ser.read(1)
        if char == b'\r':
            if tmp_buffer.find(b'OK') > -1:
                tmp_buffer = tmp_buffer.decode().replace('\n', "")
                fileOpened.write("RCV: {0}\r\n".format(tmp_buffer.replace('\r', "")))
                tmp_buffer = b''
                continue
            if tmp_buffer.find(b'ERROR') > -1:
                tmp_buffer = tmp_buffer.decode().replace('\n', "")
                fileOpened.write("RCV: {0}\r\n".format(tmp_buffer.replace('\r', "")))
                tmp_buffer = b''
                continue
            if tmp_buffer.find(b'\n') > -1 and len(tmp_buffer) == 1:
                tmp_buffer = b''
                continue
            if tmp_buffer.decode() == cmd.strip("\r"):
                tmp_buffer = b''
                continue
            tmp_buffer = tmp_buffer.strip(b'\n')
            result = tmp_buffer.decode()
            if len(result) == 0:
                tmp_buffer = b''
                continue
            fileOpened.write("RCV: {0}\r\n".format(result))
            print(result, " is result")
            tmp_buffer = b''
        else:
            tmp_buffer += char
    setPackage(result)
    fileOpened.close()

def parse_script(script):
    scriptdict = {"cfg" : []}
    scriptfile = open(script, "r")

    fileLines = scriptfile.readlines()
    count = 0
    while count < len(fileLines):
        line = fileLines[count]
        if line.startswith(">"):
            line = line.replace(">", "")
            if "{APN}" in line:
                line = line.replace("{APN}", apn)
            elif "{DEVICEID}" in line:
                line = line.replace("{DEVICEID}", deviceid)
            elif "{SERVER}" in line and "{PORT}" in line:
                line = line.replace("{SERVER}", server)
                line = line.replace("{PORT}", port)
            
            line = line.strip() + '\r'
            scriptdict["cfg"].append([line])
        elif line.startswith("<"):
            line = line.strip()
            scriptdict["cfg"][-1].append(line.replace("<", ""))
        elif line.startswith("#"):
            scriptdict["cfg"].append([line, "COMMENT"])
        elif not line:
            scriptdict["cfg"].append([line, "BLANK"])
        count += 1

    scriptfile.close()
    return scriptdict

def parse_file(fil):
    print("Parsing params file.")
    paramsfile = open(fil, "r")
    for line in paramsfile:
        linesplit = line.split("=")
        if "baudrate" in line:
            global baud
            baud = linesplit[1].rstrip()
        elif "apn" in line:
            global apn
            apn = linesplit[1].rstrip()
        elif "server" in line:
            global server
            server = linesplit[1].rstrip()
        elif "port" in line:
            global port
            port = str(linesplit[1])
    paramsfile.close()

def Run(_device, _script, _deviceid, _params, fileName):
    print("running mdmcfg...")
    
    # TODO: pass following as args from terminal
    global device
    device = _device
    script = _script
    global deviceid
    deviceid = str(_deviceid)
    params = _params

    if device == None or script == None or deviceid == None or params == None:
        print("Please pass the correct arguments")
        return -1
    
    parse_file(params)
    
    print("Finished parsing the arguments and params file.")

    # Debug
    # device = "/dev/cu.UC-232AC"
    cfg = {"cfg": [["ATE0\r", "OK"], ["AT\r", "OK"], ["AT\r", "OK"]]}
    cfg1 = {"cfg": [["AT\r", "OK"]]}
    
    callbackFunc = modemDataReceived

    scriptdict = parse_script(script)
    # Debug
    # print(scriptdict)
    handler(scriptdict, fileName)

    if ser.isOpen():
        fileOpened = open(fileName, "a")
        fileOpened.write("Port Closed.\r\n")
        fileOpened.close()
        ser.close()
    print("Exiting Provisioning Portion...")

    return 1
