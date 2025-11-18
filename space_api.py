from websocket import create_connection
import threading
import json

api_version = "0.91"
client_type = "python"

ship = { "total_power" : 4,
         "available_power" : 1,
         "pilot_power" : 1,
         "science_power" : 1,
         "weapon_power" : 1,
         "shield" : 0
    }

active = True
server_message = ""
server = None
message_stack = []

#variables from server:
#encounter_state (WAITING, IN_PROGRESS, ENDED_FAIL, ENDED_WIN, UDEAD)

playername = "Clarence"
role = "science"
team = "tech"
connection_id = 0

server_fails = 0

#Listener thread receives responses from the server
#It writes to global variables for access via other functions
def listener(_server):
    global server_message
    global server_fails
    global active
    while active:
        try:
            server_message = _server.recv()#.decode("utf-8")
            try:
                server_response = json.loads(server_message)
                if server_response["type"] == "status":
                    update_ship_status(server_response["data"])
                else:
                    message_stack.append(server_response)
            except:
                print("Server sent non-JSON response!")
        except Exception as e:
            print(e)
            disconnect()

def update_ship_status(status):
    global ship
    ship["total_power"] = status["total_power"]
    ship["available_power"] = status["available_power"]
    ship["pilot_power"] = status["pilot_power"]
    ship["science_power"] = status["science_power"]
    ship["weapon_power"] = status["weapon_power"]
    ship["shield"] = status["shield"]
    ship["hp"] = status["hp"]

def send_instruction(instruction):
    instruction["role"] = role
    instruction["team"] = team
    instruction["version"] = api_version
    server.send(json.dumps(instruction))

def move(direction):
    instruction = {"action":"move", "direction":direction}
    send_instruction(instruction)

def shoot(weapon_id):
    instruction = {"action":"shoot", "weapon_id":weapon_id}
    send_instruction(instruction)

def add_shield():
        instruction = {"action":"shield"}
        send_instruction(instruction)

def power(direction, target):
    instruction = {"action":"power", "direction":direction, "target":target}
    send_instruction(instruction)

def disconnect():
    print("Disconnecting...")
    global server
    global active
    active = False
    server.close()

def connect(_role, _team, _ip, _port):
    global server
    global role
    global team
    role = _role
    team = _team
    connected = False
    try:
        server = create_connection(f"ws://{_ip}:{_port}")
        instruction = {"action":"join"}
        send_instruction(instruction)
        listener_thread = threading.Thread(target = listener, args=(server,))
        listener_thread.start()
        connected = True
    except Exception as e:    
        print("Error connecting to the server: " + str(e))
    return connected
