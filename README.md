# GPS Provisioning Script

## Table of contents
- [Download](#download)
- [Requirements](#requirements)
- [Mac Printer Setup](#printermac)
- [Script Usage](#run)
- [References](#ref)
- [Extra](#extra)

<div id='download'/>

## How to download the script
- [Click Here](https://github.com/tmeserve/ProvisioningScript/archive/nocups.zip) to download the script
- *EXTRACT* the zip file
  - Will need [7Zip](http://www.7-zip.org/download.html) or [WinRAR](http://www.win-rar.com/download.html)

<div id='requirements'/>

## Prerequisites
- Install [python 3.7.2](https://www.python.org/downloads/release/python-372/)
  - To install python 3.7.2 on mac go to [here](https://www.youtube.com/watch?v=8BiYGIDCvvA)
- _Pip usage_
  - *ENTER* in Terminal
    - `cd (directory of the extracted downloaded files)`
    - **Please note that the text in the parentheses is something you input**
    - `pip3.7 install -r requirements.txt`
- Will need an FTP server, an SQL server, and a website ready to show the logs, to store the files, and to store the notes.

<div id='printermac'/>

## To set up the printer on a Mac
- *PLUG IN* the printer through the serial port to usb

<div id='run'/>

## Running the Script
- *ENTER* in Terminal
  - `cd (directory of the extracted downloaded files)`
  - **Please note that the text in the parentheses is something you input**
  - `python3.7 runner.py`

<div id='ref'/>

## Credit
- [John Cobb](https://github.com/johncobb/cfgmdm)

<div id='extra'/>

## Extra Information
- The COM Port is the name or location of the serial port.