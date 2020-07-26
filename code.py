import time
from adafruit_circuitplayground.express import cpx

# state variables
STATE_SETTING_TIME = 0
STATE_COUNTING_DOWN = 1
STATE_COUNTING_PAUSED = 2
STATE_COUNTING_FINISHED = 3

# state we are currently in
CURRENT_STATE = STATE_SETTING_TIME

# sometimes we need to ignore button releases.
IGNORE_NEXT_ACTION = False

# set to 60 for normal mode
COUNTDOWN_INTERVAL = 60  # in seconds
# set to 1 for hyper speed demo mode

# previous iteration button values
old_a_btn = False
old_b_btn = False

# current timer length during STATE_SETTING_TIME
time_setting = 0  # in minutes.

# Very dim. Change if you want brighter.
cpx.pixels.brightness = 0.01

# current remaining time during STATE_COUNTING_DOWN
cur_countdown_time = -1  # in minutes

# time that countown begain
start_time = -1  # in time.monotonic() units

# last time we counted down
last_tick = -1 # in time.monotonic() units

while True:

    if CURRENT_STATE == STATE_SETTING_TIME:
        # D13 on
        cpx.red_led = True

        # Set the Neopixels according to current time_setting
        for i in range(0, 10):
            if time_setting >= (i + 1) * 5:
                cpx.pixels[i] = (0, 0, 150)
    else:
        # D13 off
        cpx.red_led = False

    if CURRENT_STATE == STATE_COUNTING_DOWN:
        # Set the Neopixels according to cur_countdown_time
        for i in range(0, 10):
            if cur_countdown_time / COUNTDOWN_INTERVAL >= ((i) * 5):
                cpx.pixels[i] = (0, 0, 150)
            else:
                cpx.pixels[i] = (0, 0, 0)
        # if its been long enough then count down by 1
        if time.monotonic() > last_tick + 1:
            last_tick = time.monotonic()
            cur_countdown_time -= 1

            if cur_countdown_time == 0:  # if the time is over
                CURRENT_STATE = STATE_COUNTING_FINISHED

            # Only for debugging:
            if cur_countdown_time % 2 == 0:
                print("tick: %s" % cur_countdown_time)
            else:
                print("tock: %s" % cur_countdown_time)

    if CURRENT_STATE == STATE_COUNTING_PAUSED:
        # Set the Neopixels green according to cur_countdown_time
        for i in range(0, 10):
            if cur_countdown_time / COUNTDOWN_INTERVAL >= (i * 5):
                cpx.pixels[i] = (0, 150, 0)
            else:
                cpx.pixels[i] = (0, 0, 0)

    if CURRENT_STATE == STATE_COUNTING_FINISHED:
        # LED animation and song
        cpx.pixels.fill((0, 0, 255))
        cpx.play_tone(262, 0.3)
        cpx.pixels.fill((0, 255, 0))
        cpx.play_tone(294, 0.3)
        cpx.pixels.fill((0, 0, 0))

    # (A) button was pressed and released
    if (not cpx.button_a) and old_a_btn:
        if not IGNORE_NEXT_ACTION:
            if CURRENT_STATE == STATE_SETTING_TIME:
                # B button was also down
                if cpx.button_b:  # if (B) button was also down then start the countdown timer
                    CURRENT_STATE = STATE_COUNTING_DOWN
                    IGNORE_NEXT_ACTION = True
                    cur_countdown_time = COUNTDOWN_INTERVAL * time_setting
                    start_time = time.monotonic()
                    print(
                        "countdown time: %s - start_time: %s"
                        % (cur_countdown_time, start_time)
                    )
                # B button was not down
                else:  # add 10 minutes to current time_setting
                    time_setting += 10
            elif CURRENT_STATE == STATE_COUNTING_PAUSED:
                # Resume counting
                CURRENT_STATE = STATE_COUNTING_DOWN
            elif CURRENT_STATE == STATE_COUNTING_DOWN:
                # Pause counting
                CURRENT_STATE = STATE_COUNTING_PAUSED
        else:
            IGNORE_NEXT_ACTION = False

    # B button pressed and released
    if (not cpx.button_b) and old_b_btn:
        if not IGNORE_NEXT_ACTION:
            if CURRENT_STATE == STATE_SETTING_TIME:
                # A button was also down
                if cpx.button_a:  # if (A) button was also down then start the countdown timer
                    CURRENT_STATE = STATE_COUNTING_DOWN
                    IGNORE_NEXT_ACTION = True
                    cur_countdown_time = COUNTDOWN_INTERVAL * time_setting
                    start_time = time.monotonic()
                    print("countdown time: %s - start_time: %s")
                else:  # add 5 minutes to the current time_setting
                    time_setting += 5
            elif CURRENT_STATE == STATE_COUNTING_PAUSED:
                # Resume counting
                CURRENT_STATE = STATE_COUNTING_DOWN
            elif CURRENT_STATE == STATE_COUNTING_DOWN:
                # Pause counting
                CURRENT_STATE = STATE_COUNTING_PAUSED
        else:
            IGNORE_NEXT_ACTION = False

    if CURRENT_STATE == STATE_COUNTING_FINISHED:
        # Reset back to time setting state
        if cpx.button_a or cpx.button_b:
            CURRENT_STATE = STATE_SETTING_TIME
            IGNORE_NEXT_ACTION = True
            time_setting = 0

    old_a_btn = cpx.button_a
    old_b_btn = cpx.button_b
    # Tiny sleep
    time.sleep(50 / 1000)
