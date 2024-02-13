import json
import socket
import time

def load_config():
    with open('./config/conf.json', 'r') as f:
        config = json.load(f)
    return config

def send_udp_broadcast(config):
    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        udp_socket.settimeout(config["timeout"])
        query = {"command": "hello", "peer_id": config["peer_id"]}
        query_json = json.dumps(query).encode()

        udp_socket.sendto(query_json, ('172.31.255.255', config["broadcast_port"]))
        print("UDP broadcast sent.")

        port = udp_socket.getsockname()
        
        print("Socket poslouchá na portu:", port)
        return udp_socket
    except Exception as e:
        print("Error occurred while sending UDP broadcast:", e)

def receive_udp_responses(udp_socket):
    try:
        while True:
            try:
                data, addr = udp_socket.recvfrom(1024)
                print(f"Data: {data}")
                response = json.loads(data.decode())
                print(response)
                
            except socket.timeout:
                
                break
            except json.JSONDecodeError as e:
                print("Error decoding JSON response:", e)
            except socket.error as e:
                print("Socket error occurred:", e)
            except Exception as e:
                print("Error occurred while receiving UDP response:", e)

    except Exception as e:
        print("Error occurred while setting up UDP socket for receiving:", e)


    

def main():
    config = load_config()
    udp_discovery_config = config["udp_discovery"]
    udp_broadcast_config = config["udp_broadcast"]
    
    while True:
        socket =  send_udp_broadcast(udp_broadcast_config)
        receive_udp_responses(socket)

        time.sleep(udp_broadcast_config["timeout"])

if __name__ == "__main__":
    main()