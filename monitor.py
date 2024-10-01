import sys
import socket
from urllib.parse import urlparse

# get urls_file name from command line
if len(sys.argv) != 2:
    print('Usage: monitor urls_file')
    sys.exit()

# text file to get list of urls
urls_file = sys.argv[1]

# Reading the file
try:
    with open(urls_file, 'r') as file:
        urls = file.readlines()
except FileNotFoundError:
    print('File '+ urls_file +' not found.')
    sys.exit()

for url in urls:
    url = url.strip()

    try:
        #Parsing
        parsed_url = urlparse(url)


        # server, port, and path should be parsed from url
        host = parsed_url.hostname
        path = parsed_url.path if parsed_url.path else '/'

        #change port dependent on scheme
        if parsed_url.scheme == 'https':
            port = 443
        else:
            port = 80
        #print(f'{url}\n')
        #print(f'{host}\n')
        #print(f'{path}\n')
        #print(f'{port}\n')
    except Exception as e:
        print(f'Error parsing URL {url}: {e}')

"""
sock = None
# create client socket, connect to server
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    sock.connect((host, port))
except Exception as e:
    print(f'Network Error:\n {e}')

if sock:
    # send http request
    request = f'GET {path} HTTP/1.0\r\n'
    request += f'Host: {host}\r\n'
    request += '\r\n'
    sock.send(bytes(request, 'utf-8'))

    # receive http response
    response = b''
    while True:
        data = sock.recv(4096)
        response += data
        if not data:
            break
    print(response.decode('utf-8'))
    sock.close()
"""