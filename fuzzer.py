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
        print('URL: ' + url)
        print('Option: ' + option)

        if '--custom-auth=' in option:
            custom_auth = option[14:]
            print('custom_auth: ' + custom_auth)
            if custom_auth == 'dvwa':
                browser = mechanicalsoup.StatefulBrowser()
                browser.open(url)
                browser.get_current_form().print_summary()



    else:
        print("invalid action")
