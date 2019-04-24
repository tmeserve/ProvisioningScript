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

## To set up
- Install python 3.7.2

### If mac
- Install CUPS and set up the printer

## To set up the printer with CUPS
- Go to http://localhost:631/
  - Click `Adding Printers and Classes` under `CUPS for Administrators`
  - Click `Add Printer` under `Printers`
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

## Once python 3.7.2 is install go to the directory of the script in CMD or Terminal and enter
- pip3.7 install -r requirements.txt

## To set up the printer on windows

## Running the Script
- Type in CMD or Terminal depending on your OS and press enter python3.7 runner.py

## Extra Information
- The COM Port is the name or location of the serial port.