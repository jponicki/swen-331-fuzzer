import sys  # For system arguments
import requests  # requests HTTP library
import mechanicalsoup


successfulLinks = []
visitedLinks = []
commonwords = ['admin', 'login', 'password', 'security']
commonendings = ['.php', '.jsp', '']

def discover(browser):
    link = browser.links()
    browser.get_current_page()
    #print form summary
    try:
        browser.select_form()
        print('\n' + browser.get_url() + ' form summary:')
        browser.get_current_form().print_summary()
    except mechanicalsoup.LinkNotFoundError:
        print('No form available')

    #print cookies
    print('\n' + browser.get_url() + ' Cookies:')
    try:
        print(browser.get_cookiejar())
    except mechanicalsoup.LinkNotFoundError:
        print('No cookies')

    #prints links on page
    if len(link) > 0:
        print('\n' + browser.get_url() + ' has the following links')
        for i in link:
            print(i)

    #prints guessed links
    print('\n' + 'Guessed links: ')
    for i in commonwords:
        for j in commonendings:
            try:
                browser.find_link(i + j)
                print('Successful:' + i + j)
                successfulLinks.append(i+j)
            except mechanicalsoup.LinkNotFoundError:
                print('Failed:' + i + j)
    for i in successfulLinks:
        browser.follow_link(i)
        if browser.get_url() not in visitedLinks:
            visitedLinks.append(browser.get_url())
            try:
                discover(browser) #recursion
            except:
                print('Cannot reach: ' + browser.get_url())



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
            discover(browser)


    else:
        print("invalid action")
