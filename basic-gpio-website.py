from flask import Flask, render_template_string, request, jsonify
import RPi.GPIO as GPIO
from threading import Thread
import time

app = Flask(__name__)

# GPIO output
gpio_output = 7

# Exposed port for the website
website_port = 5000

# GPIO setup (GPIO 7 is GPIO4 in BCM mode)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(gpio_output, GPIO.OUT)

# Track whether the button should be disabled
is_disabled = False
remaining_time = 0

# HTML template with a dropdown for time options
html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GPIO Control</title>
    <script>
        function activateGPIO() {
            const selectedTime = document.getElementById('time-select').value;
            fetch('/activate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ duration: selectedTime })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('GPIO pin 7 has been activated for ' + selectedTime + ' seconds!');
                    document.getElementById('control-button').disabled = true;
                    document.getElementById('time-select').disabled = true;
                    updateRemainingTime();
                } else {
                    alert(data.message);
                }
            });
        }

        // Update the remaining time every second
        function updateRemainingTime() {
            fetch('/remaining-time')
            .then(response => response.json())
            .then(data => {
                if (data.remaining_time > 0) {
                    document.getElementById('remaining-time').innerText = 'Remaining time: ' + data.remaining_time + ' seconds';
                    setTimeout(updateRemainingTime, 1000);
                } else {
                    document.getElementById('remaining-time').innerText = '';
                    document.getElementById('control-button').disabled = false;
                    document.getElementById('time-select').disabled = false;
                }
            });
        }
    </script>
</head>
<body>
    <h1>GPIO Control</h1>
    <label for="time-select">Select duration:</label>
    <select id="time-select" {{ 'disabled' if is_disabled else '' }}>
        <option value="10">10 seconds</option>
        <option value="30">30 seconds</option>
        <option value="60">1 minute</option>
        <option value="300">5 minutes</option>
        <option value="3600">1 hour</option>
    </select>
    <button id="control-button" onclick="activateGPIO()" {{ 'disabled' if is_disabled else '' }}>Activate GPIO Pin 7</button>
    <p id="remaining-time"></p>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(html_template, is_disabled=is_disabled)

@app.route('/activate', methods=['POST'])
def activate():
    global is_disabled, remaining_time
    if is_disabled:
        return jsonify(success=False, message='The button is currently disabled. Please wait.')

    # Get the selected duration from the POST request
    data = request.json
    duration = int(data.get('duration', 10))  # Default to 10 seconds if not provided

    # Activate GPIO
    GPIO.output(gpio_output, GPIO.HIGH)
    print(f'GPIO pin {gpio_output} is now ON for {duration} seconds')
    is_disabled = True
    remaining_time = duration

    # Start a timer in a separate thread to disable GPIO after the selected duration
    def timer():
        global remaining_time, is_disabled
        while remaining_time > 0:
            time.sleep(1)
            remaining_time -= 1

        GPIO.output(gpio_output, GPIO.LOW)
        print('GPIO pin ', gpio_output, ' is now OFF')
        is_disabled = False

    Thread(target=timer).start()

    return jsonify(success=True)

@app.route('/remaining-time')
def get_remaining_time():
    return jsonify(remaining_time=remaining_time)

@app.route('/check-status')
def check_status():
    return jsonify(is_disabled=is_disabled)

# Clean up GPIO on shutdown
def cleanup_gpio():
    GPIO.output(gpio_output, GPIO.LOW)
    GPIO.cleanup()
    print('GPIO cleaned up')

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=website_port)
    finally:
        cleanup_gpio()  # Ensures GPIO cleanup on shutdown
