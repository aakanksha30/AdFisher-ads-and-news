# In this experiment we intend to find discrimination on basis of race -- african american
# We will first set gender to male/female for all simulated users and then collect ads from job websites - 
 

import sys, os
sys.path.append("../core")          # files from the core
import adfisher                     # adfisher wrapper function
import web.pre_experiment.alexa     # collecting top sites from alexa
import web.google_news              # interacting with Google News
import converter.reader             # read log and create feature vectors
import analysis.statistics          # statistics for significance testing

log_file = 'log.exp3.txt'
site_file = '---------------' # sites representing black population

def make_browser(unit_id, treatment_id):
    b = web.google_news.GoogleNewsUnit(browser='firefox', log_file=log_file, unit_id=unit_id,
        treatment_id=treatment_id, headless=False, proxy = None)
    return b

#############################
####	we will set gender as male here
##############################


# web.pre_experiment.alexa.collect_sites(make_browser, num_sites=5, output_file=site_file,
#     alexa_link="http://www.alexa.com/topsites")

# Control Group treatment
def control_treatment(unit):
    pass


# Experimental Group treatment
def exp_treatment(unit):
    unit.visit_sites(site_file)
    pass


# Measurement - Collects ads
def measurement(unit):
    sites = ['monster','bbc','toi','guardian']
    for site in sites:
        unit.collect_ads(site=site, reloads=2, delay=5)



# Shuts down the browser once we are done with it.
def cleanup_browser(unit):
    unit.quit()

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

def load_results():
    pass

def test_stat(observed_values, unit_assignments):
    pass
############	there is another file for analysis

adfisher.do_experiment(make_unit=make_browser, treatments=[control_treatment, exp_treatment],
                        measurement=measurement, end_unit=cleanup_browser,
                        load_results=load_results, test_stat=test_stat, ml_analysis=True,
                        num_blocks=1, num_units=2, timeout=2000,
                        log_file=log_file, exp_flag=True, analysis_flag=False,
                        treatment_names=["control", "experimental"])



