**To anyone reading this - this is an old thing I made/forked, honestly it's a little embarassing and I wanted to private it but you can't private forks. Therefore, I'm opting to keep this public for knowedge preservation, please save your judgement** :,)

---

# LinkedIn Autoconnect
Python script to automatically connect with other second degree connections on LinkedIn.

WARNING: RUNNING THIS SCRIPT MAY GET YOU BANNED ON LINKEDIN, [see original repo for more details](https://github.com/tomquirk/linkedin-api).

# API
This script forks [Tom Quirk's original-unofficial-linkedin-api](https://github.com/tomquirk/linkedin-api) with some slight modifications. Since adding connections is not supported in the master branch, and [abinpaul1](https://github.com/tomquirk/linkedin-api/pull/136)'s pull request has not been merged yet, I have manually applied the merge. I have also fixed a bug in another section of the code. Additionally, the constant `_MAX_REPEATED_REQUESTS` in `linkedin.py` was change from `200` to `50` to speed up search process

Nothing else was changed, so as such, any issues which persist with the master branch of [linkedin-api](https://github.com/tomquirk/linkedin-api) will still persist in this version.

# Details
By default, this script will search for second degree connections via LinkedIn's default search, with no search keywords. (This can be replicated through their website to see what results you might find). Then, the script will iterate through all search results and send connection requests, with random intervals between requests to mitigate ban rates.

# How to install
1. Download entire repository
2. Extract files to some directory
3. (optional but highly recommended) Create venv in same directory: `python -m venv venv`
4. Install modified LinkedIn API: `pip install .\pkg_dir\`

OR alternatively, install API via github: `pip install 'git+https://github.com/ACC1100/linkedin-auto_connect.git#egg=linkedin-auto_connect&subdirectory=pkg_dir'`

5. Run `autoconnect.py` file and follow instructions
6. (optional) modify `config.ini` to change script settings

# Config

## Possible config changes:
### Search
- Add keywords
- Change network depth
- Change regions
- Change schools
### Connections
- Randomise the order which connections are sent (as opposed to directly iterating from start to finish)
- Include a connection message when sending connections
- Change the lower and upper bound on time between connection requests

## Explanation of default values and config parameters:
### SEARCH
- `keywords = ` Change keywords to search for
    - Leave empty for no keywords
- `keyword_title = ` Change keywords to search for in TITLE
    - Leave empty for no keywords
##### FOR THE FOLLOWING PARAMETERS, PLEASE ENSURE ALL VALUES ARE SEPARATED BY COMMAS
- `network_depths = S` S for second, use O for third+
- `regions = 101452733` 101452733, for Australia, 
    - To find more region codes, do a search on the LinkedIn website with a country filter and find the corresponding value in the URL
- `schools = ` E.g. 10231, for Monash University, Australia. 
    - To find more school codes, do a search on LinkedIn website with a school filter and find the corresponding value in the URL
### CONNECTIONS
- `random = False` randomise order which connections are sent based on search results
    - False: no randomise, add connections sequentially from first to last in order provided in search results
    - True: add connections in random order from search results
    - CASE SENSITIVE
- `message =` change the connection message, limited to 140 characters.
    - Default empty
- `lower_wait_time = 5` `upper_wait_time = 50` change the time between connection requests, time is randomised between lower and upper bounds
