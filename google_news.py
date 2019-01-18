import time, re                                                     # time.sleep, re.split
import sys                                                          # some prints
from selenium import webdriver                                      # for running the driver on websites
from datetime import datetime                                       # for tagging log with datetime
from selenium.webdriver.common.keys import Keys                     # to press keys on a webpage
# import browser_unit
import google_ads                                                   # interacting with Google ads and Ad Settings
import google_search                                                # interacting with Google Search

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

class GoogleNewsUnit(google_ads.GoogleAdsUnit):

    def __init__(self, browser, log_file, unit_id, treatment_id, headless=False, proxy=None):
#         google_search.GoogleSearchUnit.__init__(self, browser, log_file, unit_id, treatment_id, headless, proxy=proxy)
        google_ads.GoogleAdsUnit.__init__(self, browser, log_file, unit_id, treatment_id, headless, proxy=proxy)
#       browser_unit.BrowserUnit.__init__(self, browser, log_file, unit_id, treatment_id, headless, proxy=proxy)
    
    def get_suggested(self):
        """Get top news articles from Google News"""
        self.driver.set_page_load_timeout(60)
        self.driver.get("http://news.google.com")
        tim = str(datetime.now())
#        print "Fetching top news stories"
        topdivs1 =self.driver.find_element_by_xpath("/html[1]/body[1]/div[8]/c-wiz[1]/div[1]/div[1]/div[1]/main[1]/c-wiz[1]/div[1]/div[8]/div[1]/article[1]/div[1]/div[1]/h3[1]/a[1]/span[1]")
        sys.stdout.write(".")
        sys.stdout.flush()
        new1=topdivs1.get_attribute("innerHTML").strip()
        heading = "for_you"
        #print "Title:", title, ", ago:", ago, ", agency:", agency
        news1 = strip_tags(heading+"@|"+new1).encode("utf8")
        self.log('measurement', 'news', news1)

        topdivs2 =self.driver.find_element_by_xpath("/html[1]/body[1]/div[8]/c-wiz[1]/div[1]/div[1]/div[1]/main[1]/c-wiz[1]/div[1]/div[7]/div[1]/article[1]/div[1]/div[1]/h3[1]/a[1]/span[1]")
        sys.stdout.write(".")
        sys.stdout.flush()
        new2=topdivs2.get_attribute("innerHTML").strip()
        news2 = strip_tags(heading+"@|"+new2).encode("utf8")
        self.log('measurement', 'news', news2)



        #print "Done getting top stories"

    def get_allbutsuggested(self):  # Slow execution
        """Get all news articles (except suggested stories) from Google News"""
        self.driver.set_page_load_timeout(60)
        self.driver.get("http://news.google.com")
        tim = str(datetime.now())
#        print "Fetching top news stories"
        topdivs =self.driver.find_elements_by_css_selector("div.mEaVNd div.ZulkBc.qNiaOd h4:nth-child(1) a.ipQwMb.Q7tWef")
        print ("\n# articles in Top News: ", len(topdivs))
        sys.stdout.write(".")
        sys.stdout.flush()
        for el in topdivs:
            #           print "div", i, "out of", len(topdivs)
            news1 =el.find_element_by_tag_name("span").get_attribute("innerHTML").strip()
            heading = "Top News"
            #print "Title:", title, ", ago:", ago, ", agency:", agency
            news = strip_tags(heading+"@|"+news1).encode("utf8")
            self.log('measurement', 'news', news)


    
    def get_news(self,type, reloads, delay):
        """Get news articles from Google"""
        rel = 0
        while (rel < reloads):  # number of reloads on sites to capture all ads
            time.sleep(delay)
            try:
                s = datetime.now()
                if(type == 'sug'):
                    self.get_suggested()
                elif(type == 'all'):
                    self.get_allbutsuggested()
                else:
                    raw_input("No such news category found: %s!" % site)
                e = datetime.now()
                self.log('measurement', 'loadtime', str(e-s))
            except:
                self.log('error', 'collecting', 'news')
                pass
            rel = rel + 1
    
    def read_articles(self, count=5, agency=None, keyword=None, category=None, time_on_site=20):
        """Click on articles from an agency, or having a certain keyword, or under a category"""
        self.driver.set_page_load_timeout(60)
        self.driver.get("http://news.google.com")
        tim = str(datetime.now())
        i = 0
        for i in range(0, count):
            links = []
            if(agency != None):
                links.extend(self.driver.find_elements_by_xpath(".//div[@class='esc-lead-article-source-wrapper'][contains(.,'"+agency+"')]/.."))
            if(keyword != None):
                links.extend(self.driver.find_elements_by_xpath(".//td[@class='esc-layout-article-cell'][contains(.,'"+keyword+"')]"))
            if(category != None):
                header = self.driver.find_element_by_xpath(".//div[@class='section-header'][contains(.,'"+category+"')]")
                links.extend(header.find_elements_by_xpath("../div/div/div/div/div/table/tbody/tr/td[@class='esc-layout-article-cell']"))
            if(i==0):
                print "# links found:", len(links)
            if(i>=len(links)):
                break
            links[i].find_element_by_xpath("div[@class='esc-lead-article-title-wrapper']/h2/a/span").click()
            sys.stdout.write(".")
            sys.stdout.flush()
            for handle in self.driver.window_handles:
                self.driver.switch_to.window(handle);
                if not(self.driver.title.strip() == "Google News"):
                    time.sleep(time_on_site)
                    site = self.driver.current_url
                    self.log('treatment', 'read news', site)
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])
