## GPIO Web Controller
This project is a simple Flask-based web application that allows you to control a GPIO pin on a Raspberry Pi via a web interface. The interface includes a dropdown menu to select a time duration, which activates the GPIO pin for the selected duration. The button and dropdown are disabled during the activation period, and a countdown timer is displayed indicating the remaining time until the button becomes available again. GPIO 7 is used in the script.

### Features
Control GPIO pin 7 (GPIO4 in BCM mode) via a web interface. Select activation duration from a dropdown. 
Live countdown timer displayed next to the button showing remaining time until reactivation. Automatically re-enable the button and dropdown after the selected time has elapsed.

### Prerequisites
- Raspberry Pi
- Python 3
- Flask library (pip3 install flask).
- RPi.GPIO library (pip3 install RPi.GPIO).

### Usage
Select a time duration from the dropdown menu.
Click the "Activate GPIO Pin 7" button.
The GPIO pin 7 will be set to HIGH for the selected duration.
The button and dropdown will be disabled during the countdown period.
A live countdown timer will be displayed next to the button, showing the remaining time.
Once the time has elapsed, the GPIO pin will be set to LOW, and the button and dropdown will be re-enabled.

### How It Works
The web interface is served using Flask. When you select a duration and click the button, the selected time is sent to the server.
The GPIO pin is activated (set to HIGH) for the specified duration. The server keeps track of the remaining time and updates the client every second.
Once the countdown finishes, the GPIO pin is deactivated (set to LOW), and the button becomes available again.

### Troubleshooting
There is no need to run the script as root or with elevated permissions. Reserved ports, which are accessible only to root, are in the range 1 to 1023. By default port 5000 is used.
If the web interface is not accessible, check the IP address of your Raspberry Pi and make sure it’s correct.
Make sure Flask and RPi.GPIO are installed.
