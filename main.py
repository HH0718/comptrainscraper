from bs4 import BeautifulSoup as bs
import datetime
import re
import requests
import time
import webbrowser

while True:
    list = []
    parsed = []
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    str_tomorrow = tomorrow.strftime('%A %m.%d.%y')
    class_programming = 'http://comptrain.co/class/programming/'
    individual_programming = 'http://comptrain.co/individuals/home/'
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(class_programming, headers=headers)

    class_comptrain = bs(res.text, "html.parser")

    for i in class_comptrain.find_all('h1'):
        list.append(i)

    for i in list:
        n = (bs(str(i), "html.parser").text).strip()
        # print(n)

        parsed.append(n)
    for i in parsed:
        print(i)
    if str_tomorrow in parsed:

        print(f"Found tomorrow's {str_tomorrow} workout posted in CompTrain.co")
        
    else:
        print(f"Tomorrow's workout {str_tomorrow} is not posted yet.")

    for i in range(5, 0, -1):
        time.sleep(1)
        print(f"Checking in {i} seconds.")

