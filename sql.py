from constants import (AccountID, GroupId, getThreshold,
getFirmware, getPackage, getCursor)
import datetime

cursor = getCursor()

def GetLastDeviceIdByRange(bottom, top):
    global cursor
    if cursor == None:
        cursor = getCursor()
    cmd = """\
    DECLARE @DeviceId int;
    EXEC GetLastDeviceIdByRange {0}, {1}, @DeviceId out;
    SELECT @DeviceId AS return_value
    """.format(bottom, top)
    cursor.execute(cmd)

    return_value = cursor.fetchval()
    return return_value

def InsertInitialDevice(deviceid, imei, iccid):
    global cursor
    if cursor == None:
        cursor = getCursor()
    cmd = """\
        EXEC InsertInitialDevice {0}, '{1}', '{2}', '{3}'
        """.format(deviceid, AccountID, imei, iccid)
    cursor.execute(cmd)

def InsertInitialAsset(deviceid):
    global cursor
    if cursor == None:
        cursor = getCursor()
    cmd = """\
        EXEC InsertInitialAsset '{0}', '{1}', {2}, {3}
        """.format(AccountID, GroupId, deviceid, getThreshold())
    cursor.execute(cmd)

def Aurora_InsertNote(deviceid, initials, text):
    global cursor
    if cursor == None:
        cursor = getCursor()
    # 0 = deviceid
    # 1 = datetime
    # 2 = initials
    # 3 = text
    cmd = """\
        EXEC Aurora_InsertNote null, '{0}', 'I', 'Devices', 'Config Device', null, '{1}', '{2}', true
        """.format(deviceid, initials, text)
    cursor.execute(cmd)

def UpdateDeviceProvisioned(datenow, deviceid, apn, server, port, script, logFileName):
    global cursor
    if cursor == None:
        cursor = getCursor()
    _LogFileName = logFileName
    """
    0 = deviceid
    1 = apn
    2 = server
    3 = port
    4 = firmware
    5 = package
    6 = script
    7 = _LogFileName
    """
    cmd = """\
        EXEC UpdateDeviceProvisioned {0}, '{1}', '{2}', {3}, '{4}', '{5}', '{6}', '{7}'
        """.format(deviceid, apn, server, port, getFirmware(), getPackage(), script, _LogFileName)

    cursor.execute(cmd)

def GetDeviceByDeviceId(deviceid):
    global cursor
    if cursor == None:
        cursor = getCursor()
    cmd = """\
        EXEC GetDeviceByDeviceId {0}
        """.format(deviceid)
    
    cursor.execute(cmd)

    return_value = cursor.fetchall()
    return return_value