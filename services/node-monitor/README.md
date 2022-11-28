# node-monitor
## Description
Thing (systemd daemon) I made to monitor temperatures and turn on a little light when things get too spicy. 

The USB light I used:
<https://www.amazon.com/gp/product/B07CKFLQ5V/ref=ppx_yo_dt_b_asin_title_o06_s00?ie=UTF8&psc=1>


## Virtual Environment Setup Notes:
1. Update system, install `pip` & install `virtualenv` :
```bash
sudo apt update
sudo apt full-upgrade -y
sudo apt install python3-pip python3-venv -y
```

2. Create some organization:
```bash
mkdir -p /home/pi/venvs/node-monitor
```

3. Create the virtual environment:
```bash
python3 -m venv /home/pi/venvs/node-monitor/venv
```

4. Source the virtual environment's `activate` file:
```bash
source /home/pi/venvs/node-monitor/venv/bin/activate
```

5. Verify the correct python is being used:

```bash
which python
```

#### Example output of sourcing, getting the python path, and checking the version:
```bash
pi@rpiswtest:~ $ source /home/pi/venvs/node-monitor/venv/bin/activate
(venv) pi@rpiswtest:~ $ which python
/home/pi/venvs/node-monitor/venv/bin/python
(venv) pi@rpiswtest:~ $ python --version
Python 3.9.2
(venv) pi@rpiswtest:~ $
```

6. Install the required packages (manual):
```bash
python -m pip install colorzero gpiozero pkg-resources pyserial
```

7. Deactivate the virtual environment:
```bash
deactivate
```

#### The virtual environment for node-monitor should now be setup.