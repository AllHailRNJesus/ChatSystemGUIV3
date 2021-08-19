import socket
import PySimpleGUI as sg
import zmq
import threading
from multiprocessing import Process
import time
ownport = '20020'
printOwn = lambda *args, **kwargs: window['-MINE-'].print(*args, **kwargs)
printThem= lambda *args, **kwargs: window['-THEIRS-'].print(*args, **kwargs)
context = zmq.Context.instance()
socket2 = context.socket(zmq.DEALER)
def listen(ip):
    print('listener is running..')

    socket2.bind("tcp://{}:{}".format(ip,ownport))
    while True:
        msg = socket2.recv()
        print('message: ' + msg.decode())
        printThem('>' + msg.decode())



port = '20000'

ip = '127.0.0.1'
sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Own IP: {}:{}'.format(socket.gethostbyname(socket.gethostname()), ownport))],
            [],
            [sg.Multiline('', size=(60,20), key='-MINE-', disabled=True),sg.Multiline('', size=(60,20), key='-THEIRS-', disabled=True)],
            [sg.Text('Send message:'), sg.InputText(key='-INPUT-', do_not_clear=False, disabled=True)],
            [sg.Button('Send'), sg.Button('Quit')],
            [sg.InputText('Input the ip here',key='-IP-')],
            [sg.InputText('Input the port here', key='-PORT-'), sg.Button('Connect'), sg.Button('Disconnect')]

        ]
# Create the Window
window = sg.Window('Window Title', layout, size=(1200,600))
# Event Loop to process "events" and get the "values" of the inputs
socket = context.socket(zmq.DEALER)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Quit': # if user closes window or clicks quit
        break
    if event == 'Send':
        if values['-INPUT-'] == '':
            pass
        else:
            printOwn(values['-INPUT-'])
            msg = values['-INPUT-']
            print(msg)
            socket.send_string(msg)

    P = threading.Thread(target=listen, args=(ip,), daemon=True)
    if event == 'Connect':
        port = str(values['-PORT-'])
        ip = str(values['-IP-'])

        print('booting up listener...')
        socket.connect("tcp://{i}:{p}".format(i=ip, p=port))
        P.start()

        print('after thread start...')
        window['Connect'].update(disabled=True)
        window['-INPUT-'].update(disabled=False)

    if event == 'Disconnect':
        port = str(values['-PORT-'])
        ip = str(values['-IP-'])

        print("socket 1: ", socket.get(zmq.IDENTITY))
        print("socket 2: ", socket2.get(zmq.IDENTITY))

        socket.disconnect("tcp://{i}:{p}".format(i=ip, p=port))
        socket2.disconnect("tcp://{i}:{p}".format(i=ip, p=port))
        print("socket 1: ", socket.get(zmq.IDENTITY))
        print("socket 2: ", socket2.get(zmq.IDENTITY))
        window['Connect'].update(disabled=False)
        window['-INPUT-'].update(disabled=True)
        #P.kill = True

window.close()
