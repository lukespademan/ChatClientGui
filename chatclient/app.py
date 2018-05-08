import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, LEFT, RIGHT
import threading
from socket import *
from queue import Queue
import atexit
import sys
messages = toga.Table(headings=['Hello', 'World'], data=[])
msgs = []
running = True
class ChatClient(toga.App):
    def startup(self):
        # Create a main window with a name matching the app
        self.main_window = toga.MainWindow(title=self.name)
        global msgs
        global messages
        messages = toga.Table(headings=['IP', 'Message'], data=[])
        msgs = []
        input_box = toga.Box()
        message_input = toga.TextInput()

        def button_handler(widget):
            global sock
            sock.send(message_input.value.encode("utf-8"))
            message_input.value = ""
            
        button = toga.Button('Send', on_press=button_handler)

        # Create a main content box
        input_box.add(message_input)
        input_box.add(button)
        main_box = toga.Box()
        main_box.add(messages)
        main_box.add(input_box)

        input_box.style.update(direction=ROW)
        messages.style.update(flex=1)
        message_input.style.update(flex=1)
        main_box.style.update(direction=COLUMN, padding_top=10)

        # Add the content on the main window
        self.main_window.content = main_box

        # Show the main window
        self.main_window.show()

def recv_thread(sock):
    global running
    while running:
        data = sock.recv(1024).decode("utf-8")
        global msgs
        global message
        data = data.split(":", 1)
        msgs.append(data)
        messages.data = msgs
def bye(t):
    global sock
    global running
    running = False
    sock.close()
    sys.exit()
sock = None
def main():
    q = Queue()
    host = "127.0.0.1"
    port = 25000
    global sock
    sock = socket()
    sock.connect((host, port))

    #sock.send(text.encode("utf-8"))
    t = threading.Thread(target=recv_thread, args=(sock,))
    t.start()
    atexit.register(lambda t=t: bye(t))
    return ChatClient('Chat Client', 'com.lukespademan.chatclient')
    
