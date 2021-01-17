import json
import configparser
import random
import time
from linkedin_api import Linkedin

# print(config['SEARCH']['keywords'])

class Auto_Connector:
    def __init__(self) -> None:
        self.config = configparser.ConfigParser(allow_no_value=True)
        self.config.read('config.ini')
        if len(self.config.sections()) == 0:
            self._create_config()
            self.config.read('config.ini')
        
        try:
            with open("credentials.json", "r") as f:
                self.credentials = json.load(f)
        except FileNotFoundError:
            self.credentials = self._create_credentials()

        print('authenticating')
        self.linkedin = Linkedin(self.credentials["username"], self.credentials["password"])
        print('successfully authenticated')
            
    def _create_config(self):
        print('no config detected')

        self.config.add_section('SEARCH')
        self.config.set('SEARCH', '# change keywords to search for\n# leave empty for no keywords\n# default empty')
        self.config.set('SEARCH', 'keywords', '')

        self.config.add_section('CONNECTIONS')
        self.config.set('CONNECTIONS', '# randomise order which connections are sent based on search results\n# False: no randomise, add connections sequentially from first to last in order provided in search results\n# True: add connections in random order from search results')
        self.config.set('CONNECTIONS', 'random', 'False')

        self.config.set('CONNECTIONS', '# change the connection message\n# default empty')
        self.config.set('CONNECTIONS', 'message', '')
    
        self.config.set('CONNECTIONS', '# change the time between connection requests, time is randomised between lower and upper bounds\n# WARNING, LOWER AVERAGE WAIT TIMES IS LIKELY TO INCREASE CHANCE OF BAN\n# default lower=5, upper=50\n# input must be integer')
        self.config.set('CONNECTIONS', 'lower_wait_time', '5')
        self.config.set('CONNECTIONS', 'upper_wait_time', '50')

        with open('config.ini', 'w') as f:
            self.config.write(f)
        
        print('successfully created new config')
    
    def _create_credentials(self):
        print('no credentials detected')
        username = input("enter username/email: ")
        password = input("enter password: ")

        new_credentials = {}
        new_credentials['username'] = username
        new_credentials['password'] = password

        with open("credentials.json", "w") as f:
            json.dump(new_credentials, f, ensure_ascii=False, indent=4)

        print('successfully created new credentials')
        return new_credentials

    def search(self):
        print("running search")
        results = self.linkedin.search_people(
                    keywords=self.config["SEARCH"]['keywords'],
                    network_depths=["S"],
                    profile_languages=["en"])
        print("finished search")
        return results

    def connect(self, search_results):
        print("initiating auto-connect")
        print("ctrl+c to cancel at anytime")
        while True:
            if self.config["CONNECTIONS"]['random'] == "True":
                item = random.choice(search_results)
            else:
                item = search_results[0]
            search_results.remove(item) # yep, this is slow, search results are in list form

            urn = item['urn_id']
            pid = item['public_id']
            if urn is not None:
                status = self.linkedin.add_connection(pid, profile_urn=urn, message=self.config["CONNECTIONS"]['message'])
                if status is True:
                    print(f"Error connecting with: {pid}")
                else:
                    print(f"Success: {pid}")
            
                wait = round(random.random() * random.randrange(int(self.config["CONNECTIONS"]['lower_wait_time']), int(self.config["CONNECTIONS"]['upper_wait_time'])), 2)
                print(f"waiting {wait} seconds")
                time.sleep(wait)


if __name__ == "__main__":
    connector = Auto_Connector()
    connector.connect(connector.search())
