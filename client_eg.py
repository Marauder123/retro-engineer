import space_api
import time

ip = "10.184.1.111"
port = 9876
role = "weapons"
team = "retro"
weapon_id = 1

space_api.connect(role, team, ip, port)

message = ""

while message != "quit":
    time.sleep(0.1)
    for response_number in range(len(space_api.message_stack)):
        response = space_api.message_stack.pop()
        if response["type"] == "environment":
            for item in response["response"]:
                if item['type'] != 'none':
                    print(item)
        elif response["type"] == "safe":
            print(response["data"])
        elif response["type"] == "begin_action":
            print(response["data"])
        elif response["type"] == "earpiece_info":
            print(response["data"])
        else:
            print(response["data"])
    message = input('> ')
    if message == "print":
      print(f"My ID: {space_api.connection_id}")
      print(space_api.message_stack)
    elif message == "left":
        space_api.move("left")
    elif message == "right":
        space_api.move("right")
    elif message == "shield":
        space_api.add_shield()
    elif message == "consume":
        space_api.consume_shield()
    elif message == "status":
        print(space_api.ship)
    elif message.split(" ")[0] in ["shoot", "power"]:
        message_list = message.split(" ")
        match message_list[0]:
            case "shoot":
                space_api.shoot(message_list[1])
            case "power":
                space_api.power(message_list[1], message_list[2])
    else:
        print("Not an option.")
space_api.disconnect()
