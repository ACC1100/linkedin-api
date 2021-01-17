# LinkedIn Autoconnect
Python script to automatically connect with other second degree connections on LinkedIn.

WARNING: RUNNING THIS SCRIPT MAY GET YOU BANNED ON LINKEDIN, [see original repo for more details](https://github.com/tomquirk/linkedin-api).

# API
This script forks [Tom Quirk's original-unofficial-linkedin-api](https://github.com/tomquirk/linkedin-api) with some slight modifications. Since adding connections is not supported in the master branch, and [abinpaul1](https://github.com/tomquirk/linkedin-api/pull/136)'s pull request has not been merged yet, I have manually applied the merge. I have also fixed a bug in another section of the code. 

Nothing else was changed, so as such, any issues which persist with the master branch of [linkedin-api](https://github.com/tomquirk/linkedin-api) will still persist in this version.

# Details
By default, this script will search for second degree connections via LinkedIn's default search, with no search keywords. (This can be replicated through their website to see what results you might find). Then, the script will iterate through all search results and send connection requests, with random intervals between requests to mitigate ban rates.

Possible config changes:
- Add keywords to search
- Randomise the order which connections are sent (as opposed to directly iterating from start to finish)
- Include a connection message when sending connections
- Change the lower and upper bound on time between connection requests

# How to install
1. Download entire repository
2. Extract files to some directory
3. (optional but highly recommended) Create venv in same directory: `python -m venv venv`
4. Install modified LinkedIn API: `pip install .\pkg_dir\`
4. OR alternatively, install API via github: `pip install 'git+https://github.com/ACC1100/linkedin-auto_connect.git#egg=linkedin-auto_connect&subdirectory=pkg_dir'`
5. Run `autoconnect.py` file and follow instructions
6. (optional) modify `config.ini` to change script settings