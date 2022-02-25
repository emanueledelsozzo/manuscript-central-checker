from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import argparse
import json

from time import sleep

def query_website(driver, url, username, password, timeout):

	driver.get(url)

	try:
		element_present = EC.presence_of_element_located((By.NAME, "USERID"))
		WebDriverWait(driver, timeout).until(element_present)
		login_bar = driver.find_element_by_name("USERID")
		login_bar.clear()
		login_bar.send_keys(username)
		pass_bar = driver.find_element_by_name("PASSWORD")
		pass_bar.clear()
		pass_bar.send_keys(password)
		pass_bar.send_keys(Keys.RETURN)
	except TimeoutException:
		print("Timed out waiting for page %s to load" % url)
		exit()

	sleep(timeout)

	nav_links = driver.find_elements_by_class_name("nav-link")
	for i in nav_links:
		if(i.text == "Author"):
			i.click()
			break
	
	try:
		element_present = EC.presence_of_element_located((By.ID, "authorDashboardQueue"))
		WebDriverWait(driver, timeout).until(element_present)
		author_table = driver.find_element_by_id("authorDashboardQueue")
		queue_id=0
		while(True):
			try:
				current_queue="queue_"+str(queue_id)
				queue_bar = author_table.find_element_by_id(current_queue) 
				print(queue_bar.text)
				queue_id += 1
			except:
				break
	except TimeoutException:
		print("Timed out waiting for author page to load")
		exit()






def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-j", "--json", type=str, required=True, \
		help="a json file containing the list of websites to check along with username and password")
	parser.add_argument("-t", "--timeout", type=int, default=2, \
		help="[optional] timeout waiting for website response (default=2)")
	args = parser.parse_args()
	json_file_name = args.json

	options = Options()
	options.add_argument("--headless")
	driver = webdriver.Chrome('./chromedriver', options=options)

	with open(json_file_name) as json_file:
		data = json.load(json_file)
		for k in data.keys():
			print("\n\n-----------------Querying %s----------------\n\n" % k)
			url = data[k][0]["url"]
			username = data[k][0]["username"]
			password = data[k][0]["password"]
			query_website(driver, url, username, password, args.timeout)



if __name__ == '__main__':
	main()

