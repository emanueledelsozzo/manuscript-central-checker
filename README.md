# manuscript-central-checker
A Python-based script to check the status of transactions and journals on Manuscript Central

The script has been tested on Python 3.6 with ChromeDriver 98.0.4758.102

Requirements:
- Python >=3.6
- Selenium (`pip install selenium`)
- ChromeDriver (https://chromedriver.chromium.org/downloads)

After installing the required packages, run the script as follows:

python msc_script.py -j websites.json -t timeout

where:
-j JSON, --json JSON: a json file containing the list of websites to check along with username and password (a template json file is provided)
-t TIMEOUT, --timeout TIMEOUT: [optional] timeout waiting for website response (default=2)
