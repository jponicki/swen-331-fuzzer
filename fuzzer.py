import sys  # For system arguments
import requests  # requests HTTP library

if len(sys.argv) < 4:
    print("incorrect number of arguments")

else:
    action = sys.argv[1]
    url = sys.argv[2]

    if action == "discover" or action == "test":
        page = None
        session = None
        print('Action: ' + action)
        print('URL' + url)

    else:
        print("invalid action")
