from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import datetime
import time

# TODO: import classes and log in data from JSON file

# Class information in format: [class code, start time, end time]
a_classes = [['advisoryboydsmidt', datetime.time(9, 15), datetime.time(9, 35)],
			 ['stoneapesa1', datetime.time(9, 40), datetime.time(11, 10)],
			 ['bacoymulti2', datetime.time(11, 15), datetime.time(12, 45)],
			 ['aet_randall_sr3', datetime.time(1, 30), datetime.time(3, 00)],
			 ]
b_classes = [['mobleyadvisoryrrh', datetime.time(9, 00), datetime.time(9, 20)],
			 ['walshde', datetime.time(9, 26), datetime.time(10, 26)],
			 ['briaap2020', datetime.time(2, 35), datetime.time(3, 35)],
			 ]

# Log-In info
lcps_id = '833724'
lcps_password = '!QAZ2wsx#EDC'

# A/B Day Info
# 0 = Monday, 6 = Sunday
ab_day_schedule = [[1, 'A'],
				   [2, 'B'],
				   [3, 'A'],
				   [4, 'B']
				   ]

# Set selenium chrome options
opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
opt.add_experimental_option("prefs", {
	"profile.default_content_setting_values.media_stream_mic": 1,
	"profile.default_content_setting_values.media_stream_camera": 1,
	"profile.default_content_setting_values.geolocation": 1,
	"profile.default_content_setting_values.notifications": 1
})

PATH = 'D:/Program Files (x86)/ChromeDriver/chromedriver.exe'
driver = webdriver.Chrome(PATH, options=opt)


def calc_ab_day(current_datetime):
	# TODO: calculate whether today is a day or b day
	pass


def get_class_code(current_datetime, a_classes, b_classes):
	# TODO: calculate which class has a start time that is the closest to the current time and return class code
	return a_classes[0][0]


def join_google_meet(class_code):
	# Go to google log in page
	driver.get(
		"https://accounts.google.com/ServiceLogin?service=mail&passive=true&rm=false&continue=https://mail.google.com/mail/&ss=1&scc=1&ltmpl=default&ltmplcache=2&emr=1&osid=1#identifier")
	# Fill out email and click enter
	login_field = WebDriverWait(driver, 10).until(
		EC.element_to_be_clickable((By.ID, 'identifierId')))
	login_field.send_keys(lcps_id + '@lcps.org')
	login_field.send_keys(Keys.RETURN)
	# Find password field
	password_field = WebDriverWait(driver, 10).until(
		EC.element_to_be_clickable((By.ID, 'password')))
	password_field = password_field.find_element_by_tag_name('input')
	password_field.send_keys(lcps_password)
	password_field.send_keys(Keys.RETURN)
	# Wait till logged in
	time.sleep(5)
	# Join Google Meet
	driver.get("https://g.co/meet/" + class_code)
	driver.refresh()
	# Disable Video and Audio
	driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[5]/div[3]/div/div/div[2]/div/div[1]/div[1]/div/div[4]/div[2]/div/div').click()
	time.sleep(2)
	driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[5]/div[3]/div/div/div[2]/div/div[1]/div[1]/div/div[4]/div[1]/div').click()
	time.sleep(2)
	# Join
	driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[5]/div[3]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]').click()
	time.sleep(2)


if __name__ == '__main__':
	curr_datetime = datetime.datetime.now()
	class_code = get_class_code(curr_datetime)
	join_google_meet(class_code)
	while (True):
		curr_datetime = datetime.datetime.now()
		# TODO: Check if breakout room pop up appears, if it does then join similarly if breakout room was joined, check if return to main room pop up appears
		# TODO: Check if current time is the class end time
		pass
