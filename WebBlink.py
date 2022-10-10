import network
import socket
from time import sleep
import machine
from machine import Pin

ssid = 'ChangeMe'
password = 'ChangeMe'
onboard_LED = Pin('LED', Pin.OUT)

def turn_on():
    onboard_LED.value(1)
    
def turn_off():
    onboard_LED.value(0)
    
turn_off()
    
def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    print('Connecting to WiFi ')
    while wlan.isconnected() == False:
        print(".",end="")
        sleep(0.5)
    ip = wlan.ifconfig()[0]
    print("")
    print(f'IP address is {ip}')
    return ip
    
def open_socket(ip):
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def webpage():
    html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <title>LED Control</title>
            </head>
            <center><b>
            <form action="./turn_on">
            <input type="submit" value="LED On" style="height:120px; width:120px" />
            </form>
            <table><tr>
            <td><form action="./turn_off">
            <input type="submit" value="LED Off" style="height:120px; width:120px" />
            </form></td>
            </body>
            </html>
            """
    return str(html)

def serve(connection):
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/turn_on?':
            turn_on();
        elif request == '/turn_off?':
            turn_off();
        html = webpage()
        client.send(html)
        client.close()

try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()
