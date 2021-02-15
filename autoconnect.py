import json
import configparser
import random
import time
import signal
import sys
from linkedin_api import Linkedin

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
        """Creates search config file"""
        print('no config detected')

        self.config.add_section('SEARCH')
        self.config.set('SEARCH', '# see: https://github.com/ACC1100/linkedin-auto_connect#Config for explanation of values and how to customise')
        self.config.set('SEARCH', 'keywords', '')
        self.config.set('SEARCH', 'keyword_title', '')
        self.config.set('SEARCH', 'network_depths', 'S')
        self.config.set('SEARCH', 'regions', '101452733')
        self.config.set('SEARCH', 'schools', '')

        self.config.add_section('CONNECTIONS')
        self.config.set('CONNECTIONS', 'random', 'False')

        self.config.set('CONNECTIONS', 'message', '')
    
        self.config.set('CONNECTIONS', 'lower_wait_time', '5')
        self.config.set('CONNECTIONS', 'upper_wait_time', '50')

        with open('config.ini', 'w') as f:
            self.config.write(f)
        
        print('successfully created new config')
    
    def _create_credentials(self):
        """Creates login credentials file in PLAIN TEXT"""
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
        """Searches for people based on config parameters, writes results to JSON and returns results"""
        print("running search")
        results = self.linkedin.search_people(
                    keywords=self.config["SEARCH"]['keywords'],
                    network_depths=self._string_to_list(self.config["SEARCH"]['network_depths']),
                    regions=self._string_to_list(self.config["SEARCH"]['regions']),
                    schools=self._string_to_list(self.config["SEARCH"]['schools']),
                    profile_languages=["en"],
                    keyword_title=self.config["SEARCH"]['keyword_title'])
        print("finished search")

        with open("search_results.json", "w") as f:
            json.dump(results, f, ensure_ascii=True, indent=4)
        print("wrote search results to file")

        return results
    
    def _string_to_list(self, string):
        """converts items separated by comma in string to list form, returns None if string is empty"""
        output = list(map(lambda x: x.strip(), string.split(',')))
        if len(output) == 0:
            return None
        else:
            return output

    def connect(self):
        try:
            with open("search_results.json", "r") as f:
                search_results = json.load(f)
            
            print("existing search results found, continue with existing results?")
            print("or create new results?")
            print("0: continue, 1: create new")
            response = input()

            if response == "0":
                search_results = search_results
            elif response == "1":
                search_results = self.search()
            else:
                print("invalid response, closing")
                return

        except FileNotFoundError:
            search_results = self.search()

        print("initiating auto-connect")
        print("ctrl+c to cancel at anytime")

        fail_count = 0
        self.search_results = search_results
        while True:
            if self.config["CONNECTIONS"]['random'] == "True":
                item = random.choice(self.search_results)
            else:
                item = self.search_results[0]
            self.search_results.remove(item) # probably slow

            urn = item['urn_id']
            pid = item['public_id']
            if urn is not None:
                status = self.linkedin.add_connection(pid, profile_urn=urn, message=self.config["CONNECTIONS"]['message'])
                if status is True:
                    print(f"Error connecting with: {pid}")
                    fail_count += 1
                else:
                    print(f"Success: {pid}")
                    fail_count = 0
            
                wait = round(random.random() * random.randrange(int(self.config["CONNECTIONS"]['lower_wait_time']), int(self.config["CONNECTIONS"]['upper_wait_time'])), 2)
                print(f"waiting {wait} seconds")
                time.sleep(wait)
            
            if fail_count >= 5:
                print("ERROR: FAILED 5 CONSECUTIVE CONNECTIONS,")
                print("you are likely to be rate limited,")
                print("double check by manually sending a connection through LinkedIn website")
                print("EXITING")
                return


        

    def signal_handler(self, sig, frame):
        with open("search_results.json", "w") as f:
            f.seek(0)
            json.dump(self.search_results, f, ensure_ascii=True, indent=4)
        print('successfully saved updated search before exiting')
        sys.exit(0)



if __name__ == "__main__":
    connector = Auto_Connector()
    signal.signal(signal.SIGINT, connector.signal_handler)
    connector.connect()