import time
import unittest
import sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


this_experiment = sys.argv[1]
manifest_loc = sys.argv[2]
config_loc = sys.argv[3]
time_bloc =  sys.argv[4]
ip = "http://127.0.0.1"



class local():
  def setUp(self):
    self.driver = webdriver.Chrome();
    # Get Admin page and assert on what we received
    self.driver.get(ip + "/admin");
    self.nav("Log in | Django site admin","404")

  # Login into https://54.149.235.92/admin using 
  # credentials admin/password
  def test_local(self):
    self.login();
    self.enter_experiment()


  def login(self):
    # Performs login for driver
    elem_user = self.driver.find_element_by_name("username")
    elem_user.clear()
    elem_user.send_keys("root")

    elem_pass = self.driver.find_element_by_name("password")
    elem_pass.clear()
    elem_pass.send_keys("root")
    
    #launch 
    elem_pass.send_keys(Keys.RETURN)
    self.nav("Site administration | Django site admin", "Failed to log in")

  


  # Define experiment (create new / access alresdy created one)
  def enter_experiment(self):
    # Navigate to the experiment tab
    self.driver.get(ip + "/admin/expecon/experiment/")
    self.nav("Select experiment to change | Django site admin", "Did not reach experiments")
    exists = False

    # Try to grab all already entered experiements, and check to see if exists
    try:
      # Grab rows, stringify them , parse them by newline
      rows = self.driver.find_element_by_id("result_list")
      rows_string = rows.text
      rows_string_parsed = rows_string.splitlines()
      # Check if one is equal to 
      for i in rows_string_parsed:
        #*****************************************************************************
        # if i == experiment: # Change to gloabal var
        if i == this_experiment:
        #*****************************************************************************
          exists = True
          elem = self.driver.find_element_by_link_text(this_experiment)
          self.driver.get(elem.get_attribute("href"))
          self.perform_experiment()
    # Possibly a none existent element
    except NoSuchElementException:
      pass
    if not exists:
      # if DNE add the experiment
      self.driver.get(ip + "/admin/expecon/experiment/add/")
      self.nav("Add experiment | Django site admin", "Failed to add experiment")

      manifest_upload = self.driver.find_element_by_name("file")
      #*******************************************************************************************
      # Change file location
      manifest_upload.send_keys(manifest_loc)

      # manifest_upload.send_keys("/home/daniel/Documents/Programming/LEEPS/Code/2.2/redwood/static/redwood-high-frequency-trading-remote/manifest.json")
      #*******************************************************************************************  

      # Grab save & continue, then return
      save = self.driver.find_element_by_name("_continue")
      save.send_keys(Keys.RETURN)

      # Find correct js script and execute to add new session
      aElements = self.driver.find_elements_by_tag_name("a")
      for name in aElements:
          if(name.get_attribute("href") is not None and "javascript:void(0)" in name.get_attribute("href") and "Add another Session" in name.text):
              name.click()
              break

      # Grab save & continue, then return
      save = self.driver.find_element_by_name("_continue")
      save.send_keys(Keys.RETURN)

      # Rename
      experiment_name = self.driver.find_element_by_name("name")
      experiment_name.clear()
      #***************************************************************************
      experiment_name.send_keys(this_experiment) # Change to gloabal variable
      #***************************************************************************

      # Grab save & continue, then return
      save = self.driver.find_element_by_name("_continue")
      save.send_keys(Keys.RETURN)

      self.perform_experiment()

  def perform_experiment(self):
    #
    aElements = self.driver.find_elements_by_tag_name("a")
    for name in aElements:
        if("View on site" in name.text):
          session_text = name.get_attribute("href")
          i = len(session_text)-2
          session_number = ""
          while session_text[i] != '/':
            session_number = session_number + str(session_text[i])
            i = i - 1
          session_number = session_number[::-1]
          break


    for i in range(1,5):
      script = "window.open('" + ip + "/session/"+session_number+"/subject/" + str(i) + "');"
      
      self.driver.execute_script(script)
      self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
      # time.sleep(2)
      self.driver.switch_to_window(self.driver.window_handles[0])

    for i in range(1,5):
      self.driver.switch_to_window(self.driver.window_handles[i])
      # time.sleep(4)
    self.driver.switch_to_window(self.driver.window_handles[0])

    

    get_string = ip + "/session/"+session_number+"/admin"
    self.driver.get(get_string)

    test = self.driver.find_element_by_tag_name('input')
    print("Config loc:")
    print(config_loc)
    test.send_keys(config_loc)
    
    reset = self.driver.find_element_by_id("reset-session")
    reset.send_keys(Keys.RETURN)
    time.sleep(2)
    start = self.driver.find_element_by_id("start-session")
    start.send_keys(Keys.RETURN)


  def nav(self, title, err):
    assert title in self.driver.title, err

  
  def tearDown(self):
    # self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL+Keys.SHIFT+"q")
    # self.driver.quit()
    pass





x = local()
x.setUp()
x.test_local()
x.tearDown()

    

  



# if __name__ == "__main__":

#   this_experiment = str(sys.argv[1])
#   manifest_loc = str(sys.argv[2])
#   config_loc = str(sys.argv[3])
#   sys.exit(unittest.main())
