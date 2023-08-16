# manuscript-central-checker
A Python-based script to check the status of transactions and journals on Manuscript Central

The script has been tested with Python 3.8 on macOS Monterey.
The Ubuntu version needs updates to work with the latest versions of Selenium.

Requirements:
- Python >=3.8
- Selenium >= 4.11.2 (`pip install selenium`)

As of Selenium 4.10.0, a fully-integrated driver manager takes care of downloading the necessary drivers. Thus, manually downloading the ChromeDriver (https://chromedriver.chromium.org/downloads) is not necessary anymore.

After installing the required packages, run the script as follows:

`python msc_script.py -j websites.json -t timeout`

where:
- -j JSON, --json JSON: a json file containing the list of websites to check along with username, password, and the number of max entries to report [optional] (a template json file is provided)
- -t TIMEOUT, --timeout TIMEOUT: [optional] timeout waiting for website response (default=2)


This tool has been tested on:
- Transactions on Reconfigurable Technology and Systems (TRETS) (https://mc.manuscriptcentral.com/trets)
- Transactions on Emerging Topics in Computing (TETC) (https://mc.manuscriptcentral.com/tetc-cs)
- IEEE Journal of Biomedical and Health Informatics (JBHI) (https://mc.manuscriptcentral.com/jbhi-embs)
- Transactions on Parallel and Distributed Systems (TPDS) (https://mc.manuscriptcentral.com/tpds-cs)
- Computing Surveys (CSUR) (https://mc.manuscriptcentral.com/csur)
- Transactions on Computers (TC) (https://mc.manuscriptcentral.com/tc-cs)
- IEEE Transactions on Very Large Scale Integration (TVLSI) (https://mc.manuscriptcentral.com/tvlsi-ieee)
