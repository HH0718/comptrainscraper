from bs4 import BeautifulSoup as bs
import configparser
import pendulum
import requests
import time
import twilio_api


class CompTrain:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.raw_list = []
        self.parsed_list = []
        self.class_url = 'http://comptrain.co/class/programming/'
        self.individual_url = 'http://comptrain.co/individuals/home/'
        self.found_WOD = False

    def check_date_change(self, today):
        while self.found_WOD:
            if pendulum.today().format('%A %m.%d.%y') != today:
                print('Today is a new day! Let us check for a new WOD')
                self.found_WOD = False
                self.wod_is_posted(self.class_url)
            else:
                print("Tommorrow's WOD has been posted and checked. Waiting for a new day to check again.")
                time.sleep(10)  # one hour is 3600 seconds

    def get_current_dates(self):
        """Provides a formatted date string to compare scraped HTML tags."""
        today = pendulum.today().format('%A %m.%d.%y')
        tomorrow = pendulum.tomorrow().format('%A %m.%d.%y')
        return {'today': today, 'tomorrow': tomorrow}

    def scrape_programming(self, url):
        """Scrapes desired website for posted WODs based on dates.

        :param url: str:

        """
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        html = bs(response.text, "html.parser")

        for tag in html.find_all('h1'):
            self.raw_list.append(tag)

        for dates in self.raw_list:
            clean_dates = (bs(str(dates), "html.parser").text).strip()
            self.parsed_list.append(clean_dates)

    def wod_is_posted(self, url):
        while not self.found_WOD:
            date = self.get_current_dates()

            if date['tomorrow'] in self.parsed_list:
                self.config.read('config.ini')
                body = f"Found tomorrow's ({date['tomorrow']}) WOD at {url}"
                print(body)
                for r, value in list(self.config.items('to')):
                    print(value)
                    twilio_api.send_message(self.config['from']['pa'], value, body)
                self.found_WOD = True
                self.check_date_change(date['today'])
            else:
                print(f"Tomorrow WOD ({date['tomorrow']}) has not been posted yet.")
                time.sleep(5)


if __name__ == "__main__":
    test = CompTrain()
    test.scrape_programming(test.class_url)
    test.wod_is_posted(test.class_url)
