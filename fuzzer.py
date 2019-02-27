import sys  # For system arguments
import requests  # requests HTTP library
import mechanicalsoup


successfulLinks = []
visitedLinks = []
commonwords = []
commonendings = ['.php', '.jsp', '']

custom_auth_flag = False
custom_auth_file = ''
common_words_flag = False
common_words_file = ''
vectors_flag = False
vectors_file = ''
sensitive_flag = False
sensitive_file = ''
random_flag = False
random = False
slow_flag = False
slow = 500

def readFile(filename):
    text_file = open(filename, "r")
    lines = text_file.readlines()
    return lines


def setflags(action, options):
    global custom_auth_flag
    global custom_auth_file
    global common_words_flag
    global common_words_file
    global vectors_flag
    global vectors_file
    global sensitive_flag
    global sensitive_file
    global random_flag
    global random
    global slow_flag
    global slow
    for opt in options:
        if '--custom-auth=' in opt:
            custom_auth_flag = True
            custom_auth_file = opt[14:]
        elif '--common-words=' in opt:
            common_words_flag = True
            common_words_file = opt[15:]
            commonwords = readFile(common_words_file)
        elif '--vectors=' in opt:
            vectors_flag = True
            vectors_file = opt[10:]
        elif '--sensitive=' in opt:
            sensitive_flag = True
            sensitive_file = opt[12:]
        elif '--random=' in opt:
            random_flag = True
            if opt[9:] == ('true' or 'True'):
                random = True
            elif opt[9:] == ('false' or 'False'):
                random = False
            else:
                print('invalid --random option')
                sys.exit(0)
        elif '--slow=' in opt:
            slow_flag = True
            slow = int(opt[7:])
    if action == 'discover' and common_words_flag == False:
        print('--common-words=file required for discover command')
        sys.exit(0)
    elif action == 'test' and common_words_flag == True:
        print('Not a correct discover option')
        sys.exit(0)
    elif action == 'discover' and (vectors_flag == True or sensitive_flag == True or random_flag == True or slow_flag == True):
        print('Not a correct discover option')
        sys.exit(0)
    elif action == 'test' and vectors_flag == False:
        print('--vector=file required for test command')
        sys.exit(0)
    elif action == 'test' and sensitive_flag == False:
        print('--sensitive=file required for test command')
        sys.exit(0)


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


def discoveraction(url):
    # prints out arguments for clarification
    print('Action: discover')
    print('URL: ' + url)
    if custom_auth_flag is True:
        print('custom_auth: ' + custom_auth_file)
    if custom_auth_file == 'dvwa':
        browser = mechanicalsoup.StatefulBrowser()
        browser.open(url)  # open session
        browser.get_current_page()
        browser.select_form()
        browser["username"] = "admin"  # submit credentials for form
        browser["password"] = "password"
        browser["Login"] = "Login"
        response = browser.submit_selected()
        # print(browser.get_current_page()) #print HTML
    else:  # if not dvwa
        browser = mechanicalsoup.StatefulBrowser()
        browser.open(url)  # + "/" + 'dvwa')
        browser.get_current_page()
        # print(browser.get_current_page())

    discover(browser)

def testaction(url):
    print('test')

def main():
    if len(sys.argv) < 3:
        print("incorrect number of arguments")

    else:
        action = sys.argv[1]
        url = sys.argv[2]
        arg = 3
        options = []
        while arg < len(sys.argv):
            options.append(sys.argv[arg])
            arg += 1
        setflags(action, options)

        #option = sys.argv[3]

        if action == "discover":
            discoveraction(url)
        elif action == 'test':
            testaction(url)

        else:
            print("invalid action")


main()
