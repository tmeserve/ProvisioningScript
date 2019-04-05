from pyodbc import connect
import os

AccountID = "3B71BE1C-460F-437D-BEAB-6A1380940C86"
GroupId = "E5680B2F-662F-4EEE-B0F8-44417135AF15"

conn = connect(driver='{ODBC Driver 17 for SQL Server}',
uid='provisioning',
pwd='EngenX!',
server='192.168.1.115',
database='XiGPS',
autocommit=True)

cursor = conn.cursor()

cwd = os.getcwd()

baudrate=115200
apn="c1.korem2m.com"
server="gps1.engenx.com"
port=1721

idlethreshold = 0

def setThreshold(threshold):
    idlethreshold = threshold

firmware = None

def setFirmware(firm):
    global firmware
    firmware = firm

package = None

def setPackage(pack):
    global package
    package = pack
