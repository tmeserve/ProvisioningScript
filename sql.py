from constants import (cursor, AccountID, GroupId, idlethreshold,
firmware, package)
import datetime

def GetLastDeviceIdByRange(bottom, top):
    cmd = """\
    DECLARE @DeviceId int;
    EXEC GetLastDeviceIdByRange {0}, {1}, @DeviceId out;
    SELECT @DeviceId AS return_value
    """.format(bottom, top)
    cursor.execute(cmd)

    return_value = cursor.fetchval()
    return return_value

def InsertInitialDevice(deviceid, imei, iccid):
    cmd = """\
        EXEC InsertInitialDevice {0}, '{1}', '{2}', '{3}'
        """.format(deviceid, AccountID, imei, iccid)
    cursor.execute(cmd)

def InsertInitialAsset(deviceid):
    cmd = """\
        EXEC InsertInitialAsset '{0}', '{1}', {2}, {3}
        """.format(AccountID, GroupId, deviceid, idlethreshold)
    cursor.execute(cmd)

def Aurora_InsertNote(deviceid, initials, text):
    # 0 = deviceid
    # 1 = datetime
    # 2 = initials
    # 3 = text
    cmd = """\
        EXEC Aurora_InsertNote null, '{0}', 'I', 'Devices', 'Config Device', null, '{1}', '{2}', true
        """.format(deviceid, initials, text)
    cursor.execute(cmd)

def UpdateDeviceProvisioned(datenow, deviceid, apn, server, port, script, logFileName):
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
        EXEC UpdateDeviceProvisioned {0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}
        """.format(deviceid, apn, server, port, firmware, package, script, _LogFileName)

    cursor.execute(cmd)

def GetDeviceByDeviceId(deviceid):
    cmd = """\
        EXEC GetDeviceByDeviceId {0}
        """.format(deviceid)
    
    cursor.execute(cmd)

    return_value = cursor.fetchall()
    return return_value