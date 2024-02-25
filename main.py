
import os
import threading
import tkinter
from tkinter import *
import time
import aim_assist_ard
from aim_assist_ard import *
import serial
import yaml

arduino = ''
def connect_to_ard():
    global arduino
    com_port = lbl_connect.get()
    print(com_port)
    arduino = serial.Serial(port=com_port, baudrate=115200, timeout=.1)

data = 'NOT STARTED'

running_func = False
with open('aim_assist.txt', 'w') as f:
    data = f.write('NOT STARTED')
    f.close()
root = Tk()
#root.overrideredirect(1)
root.title('Sly Aim Assist')

with open('aim_assist.txt', 'r') as f:
    data = f.readline()
    f.close()

print(f'aim_assist: {data}')
def read_status():
    while True:
        with open('aim_assist.txt', 'r') as f:
            status = f.readline()
            f.close()
        #print(data)
        lbl_status.config(text=f'STATUS: {status}')
        #lbl_status.setvar(str(data))
        if status == 'TRUE':
            break
        if status != 'TRUE':
            with open(f"weapon_settings.yaml", "r") as yamlfile:
                data = yaml.load(yamlfile, Loader=yaml.FullLoader)
                yamlfile.close()
            weapon_list = []
            for d in data[lb_game.get(lb_game.curselection())]:
                weapon_list.append(d)
            var_weapon.set(weapon_list)
    exit()

def clicked():

    global end_exit, running_func, arduino
    end_exit = False
    if running_func:
        with open('aim_assist.txt', 'w') as f:
            f.write('TRUE')
            f.close()
        time.sleep(1)
        with open('aim_assist.txt', 'w') as f:
            f.write('NOT STARTED')
            f.close()
        threading.Thread(target=read_status).start()

    with open('aim_assist.txt', 'w') as f:
        f.write('STARTED')
        f.close()
    with open('aim_assist.txt', 'r') as f:
        data = f.readline()
        f.close()
    weapon = lb_weapon.get(lb_weapon.curselection())
    game = lb_game.get(lb_game.curselection())
    #print(f'game: {game}')
    print(f'game selected:  {game}')
    print(f'weapon selected:  {weapon}')
    print(data)
    lbl_status.config(text=f'STATUS: {data}')
    #lbl_status.setvar(str(data))
    print('starting aim-assist script...')
    running_func = True
    aim_assist(game, weapon, arduino)

def stop():
    global end_exit
    end_exit = True
    with open('aim_assist.txt',  'w') as f:
        f.write('TRUE')
        f.close()
    time.sleep(1)
    print("stopping aim-assist script...")
    #root.destroy()
    root.quit()
    exit()



WIDTH, HEIGHT = 250, 350
Font_tuple = ('Unispace', 8)
root.geometry('{}x{}'.format(WIDTH, HEIGHT))

canvas = tkinter.Canvas(root, width=WIDTH, height=HEIGHT, highlightthickness=0, background='#40362C')
canvas.pack()



lbl_selection = tkinter.Label(root, text="Select Game", background='#40362C', fg='yellow', font=Font_tuple)
lbl_selection_window = canvas.create_window(5, 40, anchor=tkinter.NW, window=lbl_selection)

lbl_status = tkinter.Label(root, text=f'STATUS: {data}', background='#40362C', fg='yellow', font=Font_tuple, width=20, borderwidth=2, relief="groove")
lbl_status_window = canvas.create_window(100, 10, anchor=tkinter.NW, window=lbl_status)

lbl_status.setvar(str(data))

var_list_sel = tkinter.StringVar()
var_game = tkinter.StringVar()
with open(f"weapon_settings.yaml", "r") as yamlfile:
    data = yaml.load(yamlfile, Loader=yaml.FullLoader)
    yamlfile.close()
games_list = []
for d in data:
    games_list.append(d)
var_game.set(games_list)

lb_game = tkinter.Listbox(root, listvariable=var_game, width=30, height=5, background='#40362C', fg='yellow', font=Font_tuple, borderwidth=2, relief="groove", exportselection=False)
lb_game.select_set(0)


lbl_weapon = tkinter.Label(root, text="Select Weapon", background='#40362C', fg='yellow', font=Font_tuple)
lbl_weapon_window = canvas.create_window(5, 160, anchor=tkinter.NW, window=lbl_weapon)

var_list_weapon = tkinter.StringVar()
var_weapon = tkinter.StringVar()
var_weapon.set(('glock','acc_honey_badger','p90'))
lb_weapon = tkinter.Listbox(root, listvariable=var_weapon, width=30, height=5, background='#40362C', fg='yellow', font=Font_tuple, borderwidth=2, relief="groove", exportselection=False)
lb_weapon.select_set(0)
# Put a tkinter widget on the canvas.
button_s = tkinter.Button(root, text="Stop", command=lambda: threading.Thread(target=stop).start(), background='#40362C', fg='yellow', font=Font_tuple)
button_s_window = canvas.create_window(25, 10, anchor=tkinter.NW, window=button_s)

button_e = tkinter.Button(root, text="Start", command=lambda: threading.Thread(target=clicked).start(), background='#40362C', fg='yellow', font=Font_tuple)

button_e_window = canvas.create_window(25, 315, anchor=tkinter.NW, window=button_e)

game_window = canvas.create_window(10, 65, anchor=tkinter.NW, window=lb_game)
weapon_window = canvas.create_window(10, 185, anchor=tkinter.NW, window=lb_weapon)


lbl_connect = tkinter.Entry(root, width=10, background='#a18a74', fg='yellow', font=Font_tuple)
lbl_connect_window = canvas.create_window(10, 285, anchor=tkinter.NW, window=lbl_connect)

lbl_connect.insert(0, "COM9")

button_a = tkinter.Button(root, text="Connect to Arduino", command=lambda: threading.Thread(target=connect_to_ard).start(), background='#40362C', fg='yellow', font=Font_tuple)
button_a_window = canvas.create_window(100, 281, anchor=tkinter.NW, window=button_a)

root.after(500, lambda: threading.Thread(target=read_status).start())
root.mainloop()
