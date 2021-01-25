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
        self.config.set('SEARCH', '# see: https://github.com/ACC1100/linkedin-auto_connect#Config for explanation of values and how to customise')
        self.config.set('SEARCH', 'keywords', '')
        self.config.set('SEARCH', 'network_depths', 'S')
        self.config.set('SEARCH', 'regions', '101452733')
        self.config.set('SEARCH', 'schools', '10231, 10242')

        self.config.add_section('CONNECTIONS')
        self.config.set('CONNECTIONS', 'random', 'False')

        self.config.set('CONNECTIONS', 'message', '')
    
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
                    network_depths=self._string_to_list(self.config["SEARCH"]['network_depths']),
                    regions=self._string_to_list(self.config["SEARCH"]['regions']),
                    schools=self._string_to_list(self.config["SEARCH"]['schools']),
                    profile_languages=["en"])
        print("finished search")
        return results
    
    def _string_to_list(self, string):
        """converts items separated by comma in string to list form"""
        return list(map(lambda x: x.strip(), string.split(',')))

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