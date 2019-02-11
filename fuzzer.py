import sys  # For system arguments
import requests  # requests HTTP library
import mechanicalsoup

if len(sys.argv) < 4:
    print("incorrect number of arguments")

else:
    action = sys.argv[1]
    url = sys.argv[2]
    option = sys.argv[3]
    if action == "discover" or action == "test":
        page = None
        session = None
        print('Action: ' + action)
        print('URL' + url)
        print('Option' + option)



    else:
        print("invalid action")
