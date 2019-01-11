import time, re                                                     # time.sleep, re.split
import sys                                                          # some prints
from selenium import webdriver                                      # for running the driver on websites
from datetime import datetime                                       # for tagging log with datetime
from selenium.webdriver.common.keys import Keys                     # to press keys on a webpage
import browser_unit
from selenium.common.exceptions import NoSuchElementException

import string
import random

SEPARATOR='@|'


MAX_COLLECTED = 4


# get login ids
def clean(s):
    toks = s.strip().split(' ')
    return toks

with open('female_names.txt') as f:
    FEMALE_CREDENTIALS = map(clean, f.readlines())
    print FEMALE_CREDENTIALS

with open('male_names.txt') as f:
    MALE_CREDENTIALS = map(clean, f.readlines())


# Let's stick to 1 job for now
JOBS = ['software+engineer']
JOBS_SALARY = ['sales']

# Locations may vary
LOCATIONS = ['New+Milford%2C+CT', 'New+York%2C+NY', 'Seattle%2C+WA']

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












class IndeedAdsUnit(browser_unit.BrowserUnit):

  def __init__(self, browser, log_file, unit_id, treatment_id, headless=False, proxy=None):
    browser_unit.BrowserUnit.__init__(self, browser, log_file, unit_id, treatment_id, headless, proxy=proxy)

  def get_random_entry(self, array):
    index = random.randrange(1,len(array)-1)
    return array[index]



  def get_login_credentials(self, gender):
    '''returns (username, password)'''
    if (gender=='male'): #male
      return self.get_random_entry(MALE_CREDENTIALS)
    else: # female 
      return self.get_random_entry(FEMALE_CREDENTIALS)



  def create_user(self, gender, job_description):
  	self.driver.get('http://www.indeed.com/')

	email_txt=self.get_login_credentials(gender)

	signin = self.driver.find_element_by_css_selector(".icl-DesktopGlobalHeader-items--right:nth-child(2) li.icl-DesktopGlobalHeader-item:nth-child(2) > a.icl-DesktopGlobalHeader-link").click()

  	signin_but = self.driver.find_element_by_css_selector('span.pass-LinkItem-content')
  	signin_but.click()


  	email = self.driver.find_element_by_id('register_email')
  	email.send_keys(email_txt)

  	retype_email = self.driver.find_element_by_id('register_retype_email')
  	retype_email.send_keys(email_txt)

  	password = self.driver.find_element_by_id('register_password')
  	password.send_keys('1234@5678')

  	create_button = self.driver.find_element_by_css_selector('button.icl-Button.icl-Button--primary.icl-Button--md.icl-Button--block:nth-child(6)').click()

  	#start searching for jobs now
  	search_bar = self.driver.find_element_by_id('text-input-what')
  	search_bar.send_keys(job_description)

  	search_button = self.driver.find_element_by_css_selector('div.icl-WhatWhere-buttonWrapper>button')
  	search_button.click()
  '''

  # Collects Salary Statistics for separate analysis later
  def collect_salary(self):
      # Salary ranges 30,000 - 125,000 by 5k's
      salary_cutoffs = map(lambda x : str(x) + ',000', range(30, 125, 5))
      salaries = []
      for sal in salary_cutoffs:
          try:
            title = self.driver.find_element_by_partial_link_text(sal).get_attribute('title')
            salaries.append(title)
            self.log('measurement', 'salary', title)
          except:
            pass

  def get_salary_info(self, description):
    newstr = description.replace(",","")
    salary = []
    for i, ch in enumerate(newstr):
      money = ''
      if (ch=='$'):
        index = 1
        while (newstr[i+index].isdigit() and index < len(newstr)):
          money = money + newstr[i+index]
          index = index+1
      if (len(money)):
        salary.append(money)
    return salary

## NOT TO BE USED

  def indeed_salary(self, fname, rel):
    driver = self.driver
    driver.set_page_load_timeout(60)
    # Varies the location per reload cycle
    exp_link = "http://www.indeed.com/jobs?q="
    exp_link += JOBS_SALARY[rel % len(JOBS_SALARY)]
    exp_link += "&l=" + LOCATIONS[rel % len(LOCATIONS)]
    driver.get(exp_link)
    time.sleep(5)
    driver.execute_script('window.stop()')
    # Get rid of initial advertisement overlay
    try:
      driver.find_element_by_id('prime-popover-close-button').click()
      time.sleep(1)
      driver.execute_script('window.stop()')
    except:
      pass
    ctime = str(datetime.now())
    # Find the advertisement listings using selenium
    sponsored_jobs = driver.find_element_by_css_selector('div[data-tn-section="sponsoredJobs"]')
    job_listings = sponsored_jobs.find_elements_by_css_selector('div[data-tn-component="sponsoredJob"]')
    for job in job_listings:
      description = job.find_element_by_class_name('sjcl').get_attribute('innerHTML').strip()
      salary = self.get_salary_info(description)
      if (len(salary) > 0):
        salary_str = ' '.join(salary)
        print salary_str
        ad = strip_tags(ctime+'@|'+salary_str+'@|'+'PLACEHOLDER'+'@|'+'PLACEHOLDER').encode("utf8")
        self.log('measurement', 'ad', ad)
      driver.switch_to.default_content()

  '''
  # Collects the top 3 "Sponsored" listings (ads)
  def indeed_ads(self, fname, rel, salary):
      driver = self.driver
      driver.set_page_load_timeout(60)
      # Varies the location per reload cycle
      exp_link = "http://www.indeed.com/jobs?q="
      exp_link += JOBS[rel % len(JOBS)]
      exp_link += "&l=" + LOCATIONS[rel % len(LOCATIONS)]
      driver.get(exp_link)
      time.sleep(5)
      driver.execute_script('window.stop()')
      # Get rid of initial advertisement overlay
      try:
        driver.find_element_by_id('prime-popover-close-button').click()
        time.sleep(1)
        driver.execute_script('window.stop()')
      except:
        pass
      ctime = str(datetime.now())
      # Find the advertisement listings using selenium
      job_listings = driver.find_elements_by_css_selector('div.companyInfoWrapper')
      
      for listing in job_listings:
	    company = listing.find_element_by_css_selector('.company').get_attribute('innerHTML')
	    location = listing.find_element_by_css_selector('.location').get_attribute('innerHTML')
	    ad = strip_tags(ctime+SEPARATOR+company +SEPARATOR+'URL'+SEPARATOR+location).encode("utf8")
	    self.log('measurement', 'ad', ad)
        # Optionally find the salary statistics as well
        #if salary:
            #self.collect_salary(driver)
            driver.switch_to.default_content()
   

  def collect_ads(self, reloads, delay, salary=None, file_name=None):
      if not file_name:
          file_name = self.log_file
      rel = 0
      while (rel < reloads):
        time.sleep(delay)
        s = datetime.now()
        #if (salary):
         # self.indeed_salary(file_name, rel)
        #else:
        self.indeed_ads(file_name, rel, salary=None)
        e = datetime.now()
        self.log('measurement', 'loadtime', str(e-s))
        rel += 1

