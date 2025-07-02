# Label Studio Scripts
This is a collection of helper scripts for your Label Studio instance. It uses Label Studio HTTP API.

Usage:
1. Clone the repository
2. Create locally in the root directory file called `secrets.py`
3. Enter your Personal Access Token (found in Account & Settings in Label Studio) in JSON format: `{"API_KEY": "<your personal access token>"}`
#
* `leaderboard.py` - Generates project(s) leaderboard to motivate users to perform better
* `create_tabs.py` - Splits all images into different tabs so that multiple users can organize simultaneous labeling better  

For usage and arguments of each script, see the top comment in the python file.  
