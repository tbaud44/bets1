#-*- coding: utf-8 -*-
'''
Created on 10 mai 2017

@author: Thiery BAUDOUIN
Programme principal lancant l'interface graphique qui initialise des données necessaires
'''
from Vue.BlogabetVue import *
import time
from selenium import webdriver
from Controleur.TipsManager import TipsManager

if __name__ == '__main__': 
 
    #driver = webdriver.Firefox()
    #time.sleep(5)
    #driver.quit()
    
    ihm = Interface()
    ihm.tm.initfirefox()
    ihm.dessiner()
    
    ihm.initialiserDonnees() 
    try:
        
        ihm.mainLoop()
    except :
        print ("Erreur geree")
    exit(0)        