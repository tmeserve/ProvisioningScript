## Installing a Virtual Environment
#### Reference : https://virtualenv.pypa.io/en/stable/installation/

#### Prerequisites:

Installing PiP

```console
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py`

python get-pip.py --user
```

### Install virtualenv  
```console
pip install --user virtualenv
```

Create a folder in tesseract/parsers to house the virtual environment (env). Also, specify this project is using python3  
```console
virtualenv -p python3 env
```

Freezing dependencies
```console
pip freeze > requirements.txt
```

Activate environment  
```console
. env/bin/activate
```

Installing dependencies
```console
pip install -r requirements.txt
```

Running the code
```console
python3 main.py -device /dev/cu.devicename -baud 115200 -profile kore -script mdm-std-binary
```



To stop the virtual session  
```console
deactivate
```

# GPS Provisioning Script

## Table of contents
- [Requirements](#requirements)
- [Cups Setup](#printermac)
- [Printer Windows Set up](#printerwin)
- [Running the Script](#run)
- [Extra](#extra)

<div id='requirements'/>
## Requirements Installation
- Type `pip3.7 install -r requirements.txt` and press enter
- Install [python 3.7.2](https://www.python.org/downloads/release/python-372/)
  - To install python 3.7.2 on mac go to [here](https://www.youtube.com/watch?v=8BiYGIDCvvA)
  - To install python 3.7.2 on windows go to [here](https://www.ics.uci.edu/~pattis/common/handouts/pythoneclipsejava/python.html)
- If mac
  - Install CUPS and [Set Up the Printer](#printermac)
    - For an installation tutorial go [here](http://support.ordercup.com/support/solutions/articles/217695-installing-the-cups-driver-for-zebra-printers-on-mac-os-x)
- Type `pip3.7 install -r requirements.txt` and press enter

<div id='printermac'/>
## To set up the printer with CUPS
- Go to http://localhost:631/
  - *CLICK* `Adding Printers and Classes` under `CUPS for Administrators`
  - *CLICK* `Add Printer` under `Printers`
  - Login with your username and password for your mac.
  - Select the zebra label printer that you are using. This will be under "`Local Printers`
  - Change the name of the printer for ease of use for the script and yourself.
  - Uncheck `Share This Printer`
  - Click `Continue`
  - Choose the correct option in the "Model" options
  - Choose the type of your printer.
  - Click `Add Printer`
    - Change the media size to custom
    - Set the width to `2.25` and the height to `1`
    - Change the units to `Inches`
    - Change the resolution to `300 DPI`
    - Set the media Tracking to `Non-continuous (Web sensing)`
    - Click `Set Default Options`
- Go to http://localhost:631/printers
  - Click on the name of the printer you just created
  - Where it says `Administration` click there and select `Set Default Options`
  - Click `Printer Settings`
    - Change the Darkness to `24`
    - Click `Set Default Options`

<div id='printerwin'/>
## To set up the printer on windows

<div id='run'/>
## Running the Script
- Type in CMD or Terminal depending on your OS and press enter python3.7 runner.py

<div id='extra'/>
## Extra Information
- The COM Port is the name or location of the serial port.