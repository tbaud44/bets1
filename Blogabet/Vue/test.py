'''
Created on 19 sept. 2017

@author: baudouin
'''

# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
from time import sleep

class T5(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://blogabet.com"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_t5(self):
        driver = self.driver
        driver.get(self.base_url + "/tips")
        #p1 = driver.find_element_by_tag_name("BODY").text
        
        #p3 = driver.find_elements(By.XPATH, '/html/body/div[2]/div/div[3]/div/div/div[1]/div/div[2]/div/ul')
        #attendre 10 sec que la page se charge
        sleep(10)
        try:
            for i in range(1,30):
                xpathtip = "/html/body/div[2]/div/div[3]/div/div/div[1]/div/div[2]/div/ul/li[{0}]".format(i)
                tip = driver.find_elements(By.XPATH, xpathtip)[0]
                
                #roi et picks realises
                #/html/body/div[2]/div/div[3]/div/div/div[1]/div/div[2]/div/ul/li[2]/div[1]/span
                roi_picks = driver.find_elements(By.XPATH, xpathtip+'/div[1]/span')[0].text
                print ('roi', roi_picks)
                #titre tip et url
                #/html/body/div[2]/div/div[3]/div/div/div[1]/div/div[2]/div/ul/li[2]/div[2]/div[2]/div[1]/h3/a
                titre_url = driver.find_elements(By.XPATH, xpathtip+'/div[2]/div[2]/div[1]/h3/a')[0].text
                print ('titre', titre_url)
                
                #type pari
                #/html/body/div[2]/div/div[3]/div/div/div[1]/div/div[2]/div/ul/li[2]/div[2]/div[2]/div[1]/div[1]
                #type_pari = tip.find_elements(By.XPATH, '/div[2]/div[2]/div[1]/div[1]')
                
                #book
                #/html/body/div[2]/div/div[3]/div/div/div[1]/div/div[2]/div/ul/li[2]/div[2]/div[2]/div[1]/div[2]/a
                #book = tip.find_elements(By.XPATH, '/li[2]/div[2]/div[2]/div[1]/div[2]/a')
        except IndexError:
                print('plus de paris')
                return
                
        mon_fichier = open("/data/tmp/fichier.html", "w") # Argh j'ai tout écrasé !

        
        #mon_fichier.write(p2)
        mon_fichier.close()
        print("")
        # ERROR: Caught exception [ERROR: Unsupported command [getHtmlSource |  | ]]
        print("")
    
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
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()    