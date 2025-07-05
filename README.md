# Label Studio Scripts
This is a collection of helper scripts for your Label Studio instance. It is implemented using Label Studio HTTP API (for more details, see [here](https://api.labelstud.io/api-reference)).

Usage:
1. Clone the repository
2. Create locally in the root directory file called `secrets.txt`
3. Enter your Personal Access Token (found in Account & Settings in Label Studio) in JSON format: `{"API_KEY": "<your personal access token>"}`
#
* `leaderboard.py` - Generates project(s) leaderboard to motivate users to perform better through friendly competition
* `create_tabs.py` - Distributes all images across multiple tabs to help multiple users collaborate more efficiently

For usage and arguments of each script, see the top comment in the respective python file.  
