import socket
import PySimpleGUI as sg
import zmq
import threading
import time

printOwn = lambda *args, **kwargs: window['-MINE-'].print(*args, **kwargs)
printThem= lambda *args, **kwargs: window['-THEIRS-'].print(*args, **kwargs)
context = zmq.Context()
def listen(ip, port):
    socket2 = context.socket(zmq.DEALER)
    socket2.connect("tcp://{}:{}".format(ip,port))
    while True:
        msg = socket2.recv()
        printThem('>' + msg.decode())



port = '20000'
ownport = '20020'
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

    if event == 'Connect':
        port = values['-PORT-']
        ip = values['-IP-']
        t1 = threading.Thread(target=listen, args=(ip, 50000), daemon=True)
        socket = context.socket(zmq.DEALER)
        socket.bind("tcp://{i}:{p}".format(i=ip, p=port))

        t1.start
        window['Connect'].update(disabled=True)
        window['-INPUT-'].update(disabled=False)

window.close()