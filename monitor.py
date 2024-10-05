import sys
import socket
import ssl #module for secure communication with https
from urllib.parse import urlparse

def web_monitor(url): #Consolidating code into a function so that it is reusable with referenced and redirected URLs

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
        print(f'Error parsing URL {url}:\n{e}\n')
        return #exit function after exception

    # create client socket, connect to server
    sock = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((host, port))

        #If URL contains HTTPS, wrap socket with SSL
        if parsed_url.scheme == 'https':
            #SSL context creation
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT) #Protocol
            context.load_default_certs() #Certs
            sock = context.wrap_socket(sock, server_hostname=host) #Wrap sock for HTTPS

    except Exception as e:
        print(f'Network Error while connecting to {url}:\n{e}\n')
        return #Skip to next url if exception occurs

    if sock: #If an error occurs and no sock variable is created, the program will move onto the next url
        try:
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
            # print(f'Response from {url}:\n{response.decode("utf-8")}\n')
            response_str = response.decode('utf-8')

            headers, body = response_str.split('\r\n', 1)
            status_line = headers.split('r\n')[0]
            status_code = int(status_line.split(' ')[1])
            status_message = ' '.join(status_line.split(' ')[2:])  # The status message
            
            print(f'URL: {url}\nStatus: {status_code} {status_message}\n')

            # added code
            if (status_code == 301 or status_code == 302):
                header_lines = headers.split('\r\n')
                for line in header_lines:
                    if line.startswith('Location:'):
                        location_url = line.split(':', 1)[1].strip()  # Ensure ':' is properly handled
                        
                        # Handle relative URLs using urljoin
                        #if not location_url.startswith('http'):
                         #   location_url = urljoin(url, location_url)

                        print(f'Redirected URL: {location_url}')  # Debugging output
                        web_monitor(location_url)  # Recursive call to follow redirect
                    break
            
        except Exception as e:
            print(f'Error receiving response from {url}:\n{e}\n')#Just in case there is an error receiving data from the url
        finally:
            sock.close()
        
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

for url in urls: #for loop
    url = url.strip() #remove whitespace
    web_monitor(url) #main function call