# GPS Provisioning Script

## Table of contents
- [Download](#download)
- [Requirements](#requirements)
- [Mac Printer Setup](#printermac)
- [Virtual Environment](#venv)
- [Script Usage](#run)
- [References](#ref)
- [Extras](#extra)

<div id='download'/>

## How to download the script
- *ENTER* in Terminal
  - `git clone https://github.com/tmeserve/ProvisioningScript.git`

<div id='requirements'/>

## Prerequisites
- Install [python 3.7.2](https://www.python.org/downloads/release/python-372/)
  - To get help with installing python 3.7.2 on mac go to [here](https://www.youtube.com/watch?v=8BiYGIDCvvA)
- _Pip usage_
  - *ENTER* in Terminal
    - Change into the directory of the cloned repository
      - `console cd user/yourName/ProvisioningScript-nocups`
      - Needs to be run in a [virtual environment](#venv)
    - `pip3.7 install -r requirements.txt`
- _Drivers_
  - Install the [drivers](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-2017) according to your operating system.
- Will need an FTP server, an SQL server, and a website ready to show the logs, to store the files, and to store the notes.

<div id='printermac'/>

## To set up the printer on a Mac
- *PLUG IN* the printer through the serial port to usb

<div id='venv'/>

## Set up a virtual environment
- *ENTER* in Terminal
  - `pip install --user virtualenv`
  - Change into the directory of the cloned repository
    - `cd user/yourName/my-project/`
  - `pip freeze > requirements.txt`
  - `virtualenv -p python3 my-project`
  - `. path/to/my-project/bin/activate`
- To deactivate the virtualenv
  - *ENTER* in Terminal
    - `deactivate`

<div id='run'/>

## Running the Script
- *ENTER* in Terminal
  - Change into the directory of the cloned repository
    - `cd user/yourName/my-project`
  - `python3.7 runner.py`

<div id='ref'/>

## Credit
- [John Cobb](https://github.com/johncobb/cfgmdm)
- [Venv Installation](https://virtualenv.pypa.io/en/stable/installation/)
- [Venv Usage](https://virtualenv.pypa.io/en/stable/userguide/)

<div id='extra'/>

## Extra Information
- The COM Port is the name or location of the serial port.