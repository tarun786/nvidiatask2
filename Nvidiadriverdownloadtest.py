# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import alert_is_present
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time,os,sys
sys.path = ['..'] + sys.path
import requests
fileName=__file__
pathname = os.path.dirname(fileName)
class Verifynvidiadriverdownloads():
    def setUp(self):

        # setup the url
        firefox_capabilities = DesiredCapabilities.FIREFOX
        firefox_capabilities['marionette'] = False

        # you probably don't need the next 3 lines they don't seem to work anyway
        firefox_capabilities['handleAlerts'] = True
        firefox_capabilities['acceptSslCerts'] = True
        firefox_capabilities['acceptInsecureCerts'] = True

        # In the next line I'm using a specific FireFox profile because
        # I wanted to get around the sec_error_unknown_issuer problems with the new Firefox and Marionette driver
        # I create a FireFox profile where I had already made an exception for the site I'm testing
        # see https://support.mozilla.org/en-US/kb/profile-manager-create-and-remove-firefox-profiles#w_starting-the-profile-manager

        ffProfilePath = 'D:\work'
        profile = webdriver.FirefoxProfile(profile_directory=ffProfilePath)
        profile.set_preference("browser.download.manager.showWhenStarting", False)
        profile.set_preference("browser.download.dir","D:\\work");
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", 'application/octet-stream,application/zip, application/x-msdownload, application/exe, application/x-exe, application/dos-exe, vms/exe, application/x-winexe, application/msdos-windows, application/x-msdos-program')
        geckoPath = r'nvidiatask2\geckodriver.exe'
        self.driver = webdriver.Firefox(firefox_profile=profile, capabilities=firefox_capabilities,
                                    executable_path=geckoPath)
        self.driver.get("http://www.nvidia.com/Download/index.aspx?lang=en-us")
        self.driver.maximize_window()

    def test_different_driver_download_test(self):
        driver=self.driver
        elemets=len(driver.find_elements_by_xpath(".//*[@id='selProductSeriesType']/option"))
        print(elemets)


        count=0
        flg = 0

        for index in range(elemets):
            time.sleep(10)
            if (count > 0 and index>0 and flg==0):

                driver.find_element_by_link_text("Download Drivers").click()
                time.sleep(15)
            flg=0
            dropdown = Select(driver.find_element_by_id("selProductSeriesType"))

            dropdown.select_by_index(index)

            print("element selected  "+str(index))
            driver.find_element_by_id("imgSearch").click()

            if(self.is_element_present("xpath",".//*[@id='lblMessage']/li")):
                print(driver.find_element_by_xpath(".//*[@id='lblMessage']/li").text)
                count=count+1
                flg=1
                continue

            elif(not self.is_element_present("id","imgDwnldBtn")):
                driver.find_element_by_xpath(".//*[@id='sideNav']/table/tbody/tr/td/a/img").click()
                count=count+1
                flg = 1
                continue

            else:
                 driver.find_element_by_id("imgDwnldBtn").click()
            time.sleep(10)

            if(driver.find_element_by_xpath(".//*[@id='mainContent']/table/tbody/tr/td[1]/a/img").is_enabled()):
                #download driver
                driver.find_element_by_xpath(".//*[@id='mainContent']/table/tbody/tr/td[1]/a/img").click()
                print("200 Success")
            else:
                print("404 Error")
            time.sleep(10)
            count=count+1
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
##        self.assertEqual([], self.verificationErrors)
def main(argv=None):
    obj = Verifynvidiadriverdownloads()
    obj.setUp()
    rtnValue=obj.test_different_driver_download_test()
    obj.tearDown()
    sys.exit(rtnValue)
if __name__ == "__main__":
    main()
