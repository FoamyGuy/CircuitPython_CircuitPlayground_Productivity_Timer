# Productivity Timer
This is an application for Circuit Playground devices to make them into a productivity timer. It is inspired by the Pomodoro technique, but this can also be used as a general timer for anything that can be broken into 5 minute increments.

Works on both [Circuit Playground Express](https://www.adafruit.com/product/3333) and [Circuit Playground Bluefruit](https://www.adafruit.com/product/4333) devices.

# Installation
- Requires the [circuitplayground library](https://learn.adafruit.com/circuitpython-made-easy-on-circuit-playground-express). Make sure you have that available on your device.
- Backup your existing `code.py` file with a different name.
- Copy the `code.py` file from this project and paste it onto your `CIRCUITPY` drive of the Circuit Playground device.

# Usage
The app has 3 main states:
- Time Setting State
    - This is the state the app begins with.
    - D13 LED is ON during this state.
    - Set the time by pressing (A) or (B) buttons on the device.
    - (A) adds 10 minutes. (B) adds 5 minutes.
    - Every 5 minutes is represented by 1 of the Neopixels. (A) button will light up 2 pixels. (B) button will light up 1 pixel.
    - The Pomodoro technique uses 25 minutes so you could press (A) (A) (B) to get to 25 minutes for that.
    - When the desired time is set you can start the count down by holding one button down and then pressing and releasing the other button. Then finally releasing the first button.
    - If you accidentally press a button too many times you can press reset to start over. 
- Time Counting Down State
    - Each of the 5 minute interval LEDs will turn off in succession as time passes.
    - Press either button to pause the count down.
        - Remaining time pixels will turn green during Paused state.
        - Press either button again to resume.
    - After the full time has elapsed the timer will enter the Counting Finished state.

- Counting Finished State:
    - The Neopixles will play an animation and the speaker will play some tones.
    - Press and hold either button to go back to the Time Setting State.