import sys
import glob
import serial
from zebra import zebra
import datetime

# seriall = serial.Serial("/dev/cu.UC-232AC1", baudrate=115200)
barcodeprinter = zebra("Barcode3")
labeltoprint = """
^XA
^MD30
^FO400,50^BY3^B3,N,50,N,N^FD41000523^FS
^FO400,120^A0,30,40^FDDevice ID 41000523^FS

^FO400,165^BY2^B3,N,50,N,N^FD013796001346517^FS
^FO400,245^A0,30,40^FDIMEI 013796001346517^FS

^FO400,300^A0,24,26^FDEngenX, LLC^FS
^FO400,325^A0,24,26^FD(812) 759-6900^FS

^FO760,300^A0,24,26^FDF/W: 
20.2.2.56^FS
^FO760,325^A0,24,26^FDPKG: 2-D8^FS

^PQ1
^XZ"""

barcodeprinter.output(labeltoprint)

# if seriall.isOpen():
#     seriall.close()

# seriall.open()
# linetoprint = "^XA ^MD15 ^FO250,50^BY2^B3,N,35,N,N^FD41000523^FS ^FO250,90^ADN^FDDevice ID 41000523^FS  ^FO250,120^BY1^B3,N,35,N,N^FD013796001346517^FS ^FO250,160^ADN^FDIMEI 013796001346517^FS  ^FO250,200^ADN^FDEngenX, LLC^FS ^FO250,225^ADN^FD(812) 759-6900^FS  ^FO450,200^ADN^FDF/W:  20.2.2.56^FS ^FO450,225^ADN^FDPKG: 2-D8^FS  ^PQ1 ^XZ\r"

# seriall.write(linetoprint)