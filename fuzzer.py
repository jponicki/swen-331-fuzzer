import sys  # For system arguments
import requests  # requests HTTP library
import mechanicalsoup


visitedlinks = []

'''
def findLinks(browser):
    link = browser.links()
    visitedlinks.append(browser.get_url)
    if len(link) > 0:
        print(browser.get_url() + ' has the following links')
        for i in link:
            print(i)
        for i in link:
            browser.follow_link(i)
            if browser.get_url() not in visitedlinks:
                visitedlinks.append(browser.get_url())
                try:
                    findLinks(browser)
                except:
                    print('Cannot reach: ' + browser.get_url())
    else:
        print(browser.get_url() + 'has no links')
'''

def findLinks(browser):
    link = browser.links()
    if len(link) > 0:
        print(browser.get_url() + ' has the following links')
        for i in link:
            print(i)
    



commonwords = ['admin', 'login', 'password', 'security']
commonendings = ['.php', '.jsp']


if len(sys.argv) < 4:
    print("incorrect number of arguments")

else:
    action = sys.argv[1]
    url = sys.argv[2]
    option = sys.argv[3]
    if action == "discover":
        # prints out arguments for clarification
        print('Action: ' + action)
        print('URL: ' + url)
        print('Option: ' + option)

        if '--custom-auth=' in option:
            custom_auth = option[14:]
            print('custom_auth: ' + custom_auth)
            if custom_auth == 'dvwa':
                browser = mechanicalsoup.StatefulBrowser()
                browser.open(url) # open session
                browser.get_current_page()
                browser.select_form()
                browser["username"] = "admin"   #submit credentials for form
                browser["password"] = "password"
                browser["Login"] = "Login"
                response = browser.submit_selected()
                #print(browser.get_current_page()) #print HTML
            else: #if not dvwa
                browser = mechanicalsoup.StatefulBrowser()
                browser.open(url)  # + "/" + 'dvwa')
                browser.get_current_page()
                #print(browser.get_current_page())
            findLinks(browser)


    else:
        print("invalid action")
