import time
from adafruit_circuitplayground.express import cpx

SETTING_TIME = 0
COUNTING_DOWN = 1
COUNTING_PAUSED = 2
COUNTING_FINISHED = 3

CURRENT_STATE = SETTING_TIME

IGNORE_NEXT_ACTION = False

# in seconds
COUNTDOWN_INTERVAL = 60

old_a_btn = False
old_b_btn = False

time_setting = 0

cpx.pixels.brightness = 0.01

cur_countdown_time = -1

start_time = -1

last_tick = -1

while True:

    # LED Setting during setting time state
    if CURRENT_STATE == SETTING_TIME:
        cpx.red_led = True
        for i in range(0, 10):
            if time_setting >= (i + 1) * 5:
                cpx.pixels[i] = (0, 0, 150)
    else:
        cpx.red_led = False

    # LED setting during counting down state
    if CURRENT_STATE == COUNTING_DOWN:
        # print("%s - %s " % (time.monotonic(), cur_countdown_time))
        for i in range(0, 10):
            if cur_countdown_time / COUNTDOWN_INTERVAL >= ((i) * 5):
                cpx.pixels[i] = (0, 0, 150)
            else:
                cpx.pixels[i] = (0, 0, 0)
        # print(time.monotonic())
        if time.monotonic() > last_tick + 1:
            last_tick = time.monotonic()
            cur_countdown_time -= 1

            if cur_countdown_time == 0:
                CURRENT_STATE = COUNTING_FINISHED

            if cur_countdown_time % 2 == 0:
                print("tick: %s" % cur_countdown_time)
            else:
                print("tock: %s" % cur_countdown_time)

    if CURRENT_STATE == COUNTING_PAUSED:
        for i in range(0, 10):
            if cur_countdown_time / COUNTDOWN_INTERVAL >= (i * 5):
                cpx.pixels[i] = (0, 150, 0)
            else:
                cpx.pixels[i] = (0, 0, 0)

    # LED setting during counting finished state
    if CURRENT_STATE == COUNTING_FINISHED:
        cpx.pixels.fill((0, 0, 255))
        cpx.play_tone(262, 0.3)

        cpx.pixels.fill((0, 255, 0))
        cpx.play_tone(294, 0.3)

        cpx.pixels.fill((0, 0, 0))

    # A button pressed and released
    if (not cpx.button_a) and (old_a_btn):
        if not IGNORE_NEXT_ACTION:
            if CURRENT_STATE == SETTING_TIME:
                print("Button A pressed !")

                # B button was also down
                if cpx.button_b:
                    CURRENT_STATE = COUNTING_DOWN
                    IGNORE_NEXT_ACTION = True
                    cur_countdown_time = COUNTDOWN_INTERVAL * time_setting
                    start_time = time.monotonic()
                    print(
                        "countdown time: %s - start_time: %s"
                        % (cur_countdown_time, start_time)
                    )
                # B button was not down
                else:
                    time_setting += 10

            elif CURRENT_STATE == COUNTING_FINISHED:
                CURRENT_STATE = SETTING_TIME

            elif CURRENT_STATE == COUNTING_PAUSED:
                CURRENT_STATE = COUNTING_DOWN
            elif CURRENT_STATE == COUNTING_DOWN:
                CURRENT_STATE = COUNTING_PAUSED

        else:
            IGNORE_NEXT_ACTION = False
            print("Button A action ignored, reseting")

    # B button pressed and released
    if (not cpx.button_b) and (old_b_btn):
        if not IGNORE_NEXT_ACTION:
            if CURRENT_STATE == SETTING_TIME:
                print("Button B pressed !")

                # A button was also down
                if cpx.button_a:
                    CURRENT_STATE = COUNTING_DOWN
                    IGNORE_NEXT_ACTION = True
                    cur_countdown_time = COUNTDOWN_INTERVAL * time_setting
                    start_time = time.monotonic()
                    print("countdown time: %s - start_time: %s")
                else:
                    time_setting += 5

            elif CURRENT_STATE == COUNTING_PAUSED:
                CURRENT_STATE = COUNTING_DOWN
            elif CURRENT_STATE == COUNTING_DOWN:
                CURRENT_STATE = COUNTING_PAUSED

        else:
            IGNORE_NEXT_ACTION = False
            print("Button B action ignored, reseting")

    if CURRENT_STATE == COUNTING_FINISHED:
        if cpx.button_a:
            CURRENT_STATE = SETTING_TIME
            IGNORE_NEXT_ACTION = True
            time_setting = 0
        if cpx.button_b:
            CURRENT_STATE = SETTING_TIME
            IGNORE_NEXT_ACTION = True
            time_setting = 0

    old_a_btn = cpx.button_a
    old_b_btn = cpx.button_b

    time.sleep(50 / 1000)
    # print("%s - %s" % (cpx.button_a, cpx.button_b))
