import serial
import win32api
import time
import keyboard
import yaml
import random
# Set whether the anti-recoil is enabled by default
enabled = False
# Set the toggle button
toggle_button = 'num lock'

def write_read(x, ard):
    ard.write(bytes(x, 'utf-8'))


def is_mouse_down():  # Returns true if the left mouse button is pressed
    lmb_state = win32api.GetKeyState(0x01)
    return lmb_state < 0

def aim_assist(game, weapon, ard):

    global enabled, toggle_button, horizontal_range, min_vertical, max_vertical, min_firerate, max_firerate, end_exit
    with open(f"{game}_settings.yaml", "r") as yamlfile:
        data = yaml.load(yamlfile, Loader=yaml.FullLoader)
        print("Read successful")
        yamlfile.close()
    #print(data)
    print(data[game][weapon])
    w_name = weapon
    weapon = data[game][weapon]
    horizontal_range = weapon['horizontal_range']
    min_vertical = weapon['min_vertical']
    max_vertical = weapon['max_vertical']
    min_firerate = weapon['min_firerate']
    max_firerate = weapon['max_firerate']

    print("Anti-recoil started!!")
    if enabled:
        print("Status: ENABLED")
    else:
        print("Status: DISABLED")

    last_state = False
    while True:
        with open('aim_assist.txt', 'r') as f:
            status = f.readline()
            f.close()

        if status == 'TRUE':
            enabled = False
            exit()

        key_down = keyboard.is_pressed(toggle_button)
        # If the toggle button is pressed, toggle the enabled value and print
        if key_down != last_state:
            last_state = key_down
            if last_state:
                enabled = not enabled
                if enabled:
                    print("Anti-recoil ENABLED")
                    with open('aim_assist.txt', 'w') as f:
                        f.write('ENABLED')
                        f.close()
                else:
                    print("Anti-recoil DISABLED")
                    with open('aim_assist.txt', 'w') as f:
                        f.write('DISABLED')
                        f.close()
        if not is_mouse_down():
            start_time = True
        if is_mouse_down() and enabled:
            if start_time:
                start = time.time()
                start_time = False
                if w_name == 'havoc':
                    time.sleep(0.5)

            # Offsets are generated every shot between the min and max config settings
            offset_const = 1000
            bonus_offset = eval(weapon['bonus_offset'])
            horizontal_offset = eval(weapon['horizontal_offset'])
            vertical_offset = eval(weapon['vertical_offset'])
            # Move the mouse with these offsets
            write_read(str(int(horizontal_offset)) + ";" + str(int(vertical_offset)), ard)
            # Generate random time offset with the config settings
            time_offset = eval(weapon['time_offset'])
            time.sleep(time_offset)
