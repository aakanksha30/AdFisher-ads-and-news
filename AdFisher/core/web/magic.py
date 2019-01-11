import time, re                                                     # time.sleep, re.split
import sys                                                          # some prints
from selenium import webdriver                                      # for running the driver on websites
from datetime import datetime                                       # for tagging log with datetime
from selenium.webdriver.common.keys import Keys                     # to press keys on a webpage
from selenium.webdriver.common.action_chains import ActionChains    # to move mouse over
# import browser_unit
import google_search                                                # interacting with Google Search



def clean(s):
    toks = s.strip().split(' ')
    return toks

with open('filename') as f:
    FEMALE_CREDENTIALS = map(clean, f.readlines())
    print FEMALE_CREDENTIALS

with open('filename') as f:
    MALE_CREDENTIALS = map(clean, f.readlines())





# strip html
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data() 

class MagicBricksUnit(google_search.GoogleSearchUnit):

    def __init__(self, browser, log_file, unit_id, treatment_id, headless=False, proxy=None):
    	google_search.GoogleSearchUnit.__init__(self, browser, log_file, unit_id, treatment_id, headless, proxy=proxy)
#   	browser_unit.BrowserUnit.__init__(self, browser, log_file, unit_id, treatment_id, headless, proxy=proxy)



    def get_random_entry(self, array):
    	index = random.randrange(1,len(array)-1)
    	return array[index]

    def get_login_credentials(self, gender):
    '''returns (username, password)'''
    	if (gender=='male'): #male
      		return self.get_random_entry(MALE_CREDENTIALS)
    	else: # female 
      		return self.get_random_entry(FEMALE_CREDENTIALS)

      
    def create_user(self, gender, occupation):
    	"""user's gender is either male or female"""
    	[user_email, user_password] = self.get_login_credentials(gender)

    	#user_email = MALE_EMAIL if (gender=='male') else FEMALE_EMAIL
    	#user_password = MALE_PASSWORD if (gender=='male') else FEMALE_PASSWORD
	
    	self.driver.get("https://www.linkedin.com/")
	
    	login_email = self.driver.find_element_by_id("login-email")
    	login_email.send_keys(user_email)

    	login_password = self.driver.find_element_by_id("login-password")
    	login_password.send_keys(user_password)

    	signin = self.driver.find_element_by_css_selector("#login-submit")
    	signin.click()
	
    	self.occupation = occupation



    def collect_ads(self, reloads, delay, site, file_name=None):
        if file_name == None:
            file_name = self.log_file
        rel = 0
        while (rel < reloads):  # number of reloads on sites to capture all ads
            time.sleep(delay)
            try:
                s = datetime.now()
                if(site == 'magicbricks'):
                	self.save_magic_bricks(file_name)
                else:
                    raw_input("No such site found: %s!" % site)
                e = datetime.now()
                self.log('measurement', 'loadtime', str(e-s))
            except:
                self.log('error', 'collecting ads', 'Error')
            rel = rel + 1

    def save_magic_bricks(self, file):
        driver = self.driver
        id = self.unit_id
        sys.stdout.write(".")
        sys.stdout.flush()
        driver.set_page_load_timeout(60)
        driver.get("https://www.magicbricks.com/")
        time.sleep(10)
        driver.execute_script('window.stop()')
        tim = str(datetime.now())
        els=driver.find_elements_by_css_selector('div#projGalTwo a >div:nth-child(2)')
        for el in els:
        	name=el.find_element_by_class_name('pgTwoName').get_attribute('innerHTML').strip()
        	group=el.find_element_by_class_name('pgTwoGroup').get_attribute('innerHTML').strip()
        	address =el.find_element_by_class_name('pgTwoAdd').get_attribute('innerHTML').strip()
        	bhk=el.find_element_by_class_name('pgTwoType').get_attribute('innerHTML').strip()
        	price=el.find_element_by_class_name('pgTwoPrice').get_attribute('innerHTML').strip()
        	ad=strip_tags(name+"@|"+group+"@|"+address+"@|"+bhk+"@|"+price).encode("utf8")
        	self.log('measurement', 'ad', ad)





