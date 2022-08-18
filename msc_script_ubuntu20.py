from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

import argparse
import json

from time import sleep

default_max_entry = 100

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def get_entries(driver, timeout, max_entry):
	try:
		element_present = EC.presence_of_element_located((By.ID, "authorDashboardQueue"))
		WebDriverWait(driver, timeout).until(element_present)
		author_table = driver.find_element(by=By.ID, value="authorDashboardQueue")
		queue_id=0
		while(queue_id < max_entry):
			try:
				current_queue="queue_"+str(queue_id)
				queue_bar = author_table.find_element(by=By.ID, value=current_queue)
				# infos = queue_bar.find_elements_by_tag_name("td")
				infos = queue_bar.find_elements(by=By.TAG_NAME, value="td")
				infos_len = len(infos)
				adm_found = False
				adm_index = -1
				for c, i in enumerate(infos):
					if not adm_found:
						adms = [j.strip() for j in i.text.split("\n") if "ADM:" in j or "INF:" in j or "EIC:" in j]
						if len(adms) > 0:
							data = "\n".join(adms)
							adm_found = True
							adm_index = c
						else:
							data = ""
					elif c - adm_index == 2:
						data = bcolors.FAIL + i.text.strip() + bcolors.ENDC
					elif c < infos_len - 2:
						data = i.text.strip()
					elif c < infos_len - 1:
						continue
					else:
						data = "Submitted on: " + i.text.strip()
					if data != "":
						print(data)


				print("\n\n")
				queue_id += 1
			except NoSuchElementException:
				break
	except TimeoutException:
		print("Timed out waiting for author page to load")
		exit()

def query_website(driver, url, username, password, max_entry, timeout):

	driver.get(url)

	try:
		element_present = EC.presence_of_element_located((By.NAME, "USERID"))
		WebDriverWait(driver, timeout).until(element_present)
		login_bar = driver.find_element(by=By.NAME, value="USERID")

		login_bar.clear()
		login_bar.send_keys(username)
		pass_bar = driver.find_element(by=By.NAME, value="PASSWORD")
		pass_bar.clear()
		pass_bar.send_keys(password)
		pass_bar.send_keys(Keys.RETURN)
	except TimeoutException:
		print("Timed out waiting for page %s to load" % url)
		exit()

	sleep(timeout)

	nav_links = driver.find_elements(by=By.CLASS_NAME, value="nav-link")
	for i in nav_links:
		if(i.text == "Author"):
			i.click()
			get_entries(driver, timeout, max_entry)
			break

	decision = driver.find_elements(by=By.CLASS_NAME, value="nav-submenu")
	for i in decision:
		if("Manuscripts with Decisions" in i.text):
			i.click()
			get_entries(driver, timeout, max_entry)
			break

	coauthor = driver.find_elements(by=By.CLASS_NAME, value="nav-submenu")
	for i in coauthor:
		if("Manuscripts I Have Co-Authored" in i.text):
			i.click()
			get_entries(driver, timeout, max_entry)
			break

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-j", "--json", type=str, required=True, \
		help="a json file containing the list of websites to check along with username, password, \
			and the number of max entries to report [optional]")
	parser.add_argument("-t", "--timeout", type=int, default=2, \
		help="[optional] timeout waiting for website response (default=2)")
	args = parser.parse_args()
	json_file_name = args.json

	options = Options()
	options.add_argument("--headless")
	#options.add_argument("--disable-dev-shm-usage")
	#options.add_argument("--no-sandbox")
	serv = Service('/snap/bin/chromium.chromedriver')
	driver = webdriver.Chrome(service=serv, options=options)

	print("\n\n")

	with open(json_file_name) as json_file:
		data = json.load(json_file)
		for k in data.keys():
			print(bcolors.WARNING + "-----------------Querying %s----------------\n\n\n" % (k) + bcolors.ENDC)
			url = data[k][0]["url"]
			username = data[k][0]["username"]
			password = data[k][0]["password"]
			max_entry = data[k][0]["max_entry"] if "max_entry" in data[k][0] else default_max_entry
			query_website(driver, url, username, password, max_entry, args.timeout)



if __name__ == '__main__':
	main()

