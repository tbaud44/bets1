#-*- coding: utf-8 -*-
'''
Created on 17 mai 2017

@author: Thierry BAUDOUIN
classe permettant la gestion de la bibliotheque video representees par des bande annonce, pub et animation Beaulieu
gere la persistance des informations avec la couche modele
'''
from datetime import date
import datetime

import pickle
import re

from transverse.BlogabetException import BlogException, BlogWarning
from transverse.Util import Util
from selenium import webdriver
from selenium.webdriver.common.by import By
from transverse import BlogabetException
from Modele.Tip import Tip

class TipsManager(object):
    '''
    Gestion de la bibliotheque de videos
    '''
    def __init__(self):
        '''
        Constructor
        '''
        #calcul des criteres
        self.critere_roi = int(Util.configValue('criteres', 'roi'))
        self.critere_tips = int(Util.configValue('criteres', 'tips'))
        self.critere_ic = int(Util.configValue('criteres', 'ic'))
        self.lancerFirefox = False  #permet de activer/desactiver appel au navigateur
        self.__load()
        
    def initfirefox(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://blogabet.com"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def __load(self):
        '''
        construit la liste des tips a partir d'un fichier tips.obj'''
        try:
            fichierTips=Util.configValue('commun', 'fichierTips')
            with open(fichierTips, 'rb') as fichier:
                mon_depickler = pickle.Unpickler(fichier)
                self.bestTips = mon_depickler.load()
                fichier.close()
        except (IOError,FileNotFoundError) as e:
            print ('creation du fichier')
            with open(fichierTips, 'w') as nouvFichier: #on cree le fichier
                nouvFichier.close()
                self.bestTips = {} #dictionnaire de tous tips conserves
        except EOFError:     #fichier vide
            self.bestTips = {} #dictionnaire de tous tips conserves
        
            
    def save(self):
        '''
        sauvegarde la liste des tips best dans un fichier tips.obj
        '''
        fichierTips=Util.configValue('commun', 'fichierTips')
        with open(fichierTips , 'wb') as fichier:
            mon_pickler = pickle.Pickler(fichier)
            mon_pickler.dump(self.bestTips)
        fichier.close()
            
    def parseRoi(self,roiTips):
        '''analyse et extrait une chaine de type  +29% (44) ou -52% (27)
           retourne un tuplet de 2 entiers(roi,nbTips) 
        '''        
        retour = re.match(r"\+([\d]{1,5})% \(([\d]{1,8})\)", roiTips)          
        if retour:    
                return (int(retour.group(1)),int(retour.group(2)))
        retour2 = re.match(r"-([\d]{1,5})% \(([\d]{1,8})\)", roiTips)          
        if retour2:    
                return (int(retour2.group(1))*-1,int(retour2.group(2)))
        #cas du 0%
        retour3 = re.match(r"0% \(([\d]{1,8})\)", roiTips)          
        if retour3:    
                return (0,int(retour3.group(1)))
        
        #pas de correspondance donc erreur
        print('Erreur ROI', roiTips)
        raise BlogabetException.BlogWarning('parsingROI')    
    
    def parseIC(self,ic):
        '''analyse et extrait une chaine de type  8/10 qui correspond à l'indice de confiance
           retourne l'indice
        '''        
        retour = re.match(r"([\d]{1,2})/10", ic)          
        if retour:    
                return (int(retour.group(1)))
        #pas de correspondance donc erreur
        raise BlogabetException.BlogWarning('parsingIC')  
    
    def parseMarcheDateEvt(self,marche):
        '''analyse et extrait une chaine de type  Tennis / ATP / Kick off: 22 Sep 2017, 16:00 
           retourne un tuplet (marche, date)
        '''        
        retour = re.match(r"(.*)Kick off: (.*)", marche)          
        if retour:    
                marche = retour.group(1)
                dateEvtStr = retour.group(2)
                d=datetime.datetime.strptime(dateEvtStr, '%d %b %Y, %H:%M')
                return (marche, d)
        #pas de correspondance donc erreur
        raise BlogabetException.BlogWarning('parsingMarche')    
           
    def filtrerPayant(self, paid):
        '''regarde le contenu de la chaine si egal à Paid pick'''
        return re.search(r"Paid pick", paid)
    
    def parseCombo(self, combo):
        '''regarde le contenu de la chaine si egal à combo pick'''
        return re.search(r"Combo pick", combo)
    
    def filtrerLive(self, books):
        '''regarde le contenu de la chaine si egal à LIVE'''
        '''NE MARCHE PAS !! faire un TU et search'''
        return re.search(r"LIVE", books)
    
    def filtrerRoi(self, roi):
        '''regarde la valeur est inferieur à un seuil'''
        return (roi <self.critere_roi)
    
    def filtrerIC(self, ic):
        '''regarde la valeur est inferieur à un seuil'''
        return (ic <self.critere_ic)
    
    def filtrerTips(self, tips):
        '''regarde la valeur est inferieur à un seuil'''
        return (tips <self.critere_tips)
        
    def getColorTip(self, tip, dateNow):
        '''retourne une couleur en fonction de la date'''
        dateTipPlus2Heure =  tip.dateEvt + datetime.timedelta(hours=2)
        if  dateTipPlus2Heure >= dateNow:
            if tip.status.value==2:
                return 'darkgreen' #c'est bon le tip est pris
            if tip.status.value==3:
                return 'palegreen' #c'est bon le tip est pris
            if tip.status.value==4:
                return 'palegreen' #c'est bon le tip est pris
            if tip.status.value==1:
                return 'green' #c'est bon le tip est pris
            
        else:
            if tip.status.value==2:
                return 'maroon'
            else:
                return 'red'
          
    # combo pick
    # cote /html/body/div[2]/div/div[3]/div/div/div[1]/div/div[2]/div/ul/li[1] /div[2]/div[2]/div[1]/div[1]/span
    # ic /html/body/div[2]/div/div[3]/div/div/div[1]/div/div[2]/div/ul/li[1]   /div[2]/div[2]/div[1]/div[2]/span
    # book /html/body/div[2]/div/div[3]/div/div/div[1]/div/div[2]/div/ul/li[1]  /div[2]/div[2]/div[1]/div[2]/a
    # marche /html/body/div[2]/div/div[3]/div/div/div[1]/div/div[2]/div/ul/li[1]  /div[2]/div[2]/div[2]
                                                                                                                       
    def rechercherTipsWeb(self):
        '''recherche tous les tips disponibles sur la page de blogabets
        '''
        print ('Debut recherche tips ')
        driver = self.driver
        driver.get(self.base_url + "/tips")
        #p1 = driver.find_element_by_tag_name("BODY").text
        
        #p3 = driver.find_elements(By.XPATH, '/html/body/div[2]/div/div[3]/div/div/div[1]/div/div[2]/div/ul')
        #attendre 10 sec que la page se charge
        
        try:
            for i in range(1,20):
                xpathtip = "/html/body/div[2]/div/div[3]/div/div/div[1]/div/div[2]/div/ul/li[{0}]".format(i)
                print ('Traitement ', i)
                #roi et picks realises
                tip = Tip()
                try:
                    #payant ou gratuit
                    ## /html/body/div[2]/div/div[3]/div/div/div[1]/div/div[2]/div/ul/li[7] /div[2]/div[2]/div/h3
                    ispaid = driver.find_elements(By.XPATH, xpathtip+'/div[2]/div[2]/div/h3')[0].text
                    if self.filtrerPayant(ispaid):
                        continue
                    
                    #auteur
                    #/html/body/div[2]/div/div[3]/div/div/div[1]/div/div[2]/div/ul/li[5] /div[2]/div[1]/div[1]/a
                    autheur = driver.find_elements(By.XPATH, xpathtip+'/div[2]/div[1]/div[1]/a')[0].text
                    tip.setAutheur(autheur)
                    #/html/body/div[2]/div/div[3]/div/div/div[1]/div/div[2]/div/ul/li[2]/div[1]/span
                    roi_picks = driver.find_elements(By.XPATH, xpathtip+'/div[1]/span')[0].text
                    (roi, nbtips) = self.parseRoi(roi_picks)
                    tip.setRoi(roi)
                    if self.filtrerRoi(roi):
                        continue
                    tip.setNbTips(nbtips)
                    if self.filtrerTips(nbtips):
                        continue
                    
                    #pas exception levee donc on peut cree le tip
                    print ('roi', roi_picks)
                    
                    #analyse
                    #/html/body/div[2]/div/div[3]/div/div/div[1]/div/div[2]/div/ul/li[4] /div[2]/div[2]/div[2]/span[2]
                    analyse = driver.find_elements(By.XPATH, xpathtip+'/div[2]/div[2]/div[2]/span[2]')[0].text
                    tip.setAnalyse(analyse)
                    
                    #titre tip et url
                    # /html/body/div[2]/div/div[3]/div/div/div[1]/div/div[2]/div/ul/li[7] /div[2]/div[2]/div/h3
                    # combo pick /html/body/div[2]/div/div[3]/div/div/div[1]/div/div[2]/div/ul/li[1] /div[2]/div[2]/div[1]/h3/a
                    titre = driver.find_elements(By.XPATH, xpathtip+'/div[2]/div[2]/div[1]/h3/a')[0].text
                    print ('titre', titre)
                    combo = self.parseCombo(titre)
                    tip.setTitre(titre)
                    
                    if not combo:
                        #choixGagnant
                        #/html/body/div[2]/div/div[3]/div/div/div[1]/div/div[2]/div/ul/li[1] /div[2]/div[2]/div[1]/div[1]
                        choixGagnant = driver.find_elements(By.XPATH, xpathtip+'/div[2]/div[2]/div[1]/div[1]')[0].text
                        print ('choixGagnant', choixGagnant)
                        tip.setChoixGagnant(choixGagnant)
                        
                        #indice confiance
                        #/html/body/div[2]/div/div[3]/div/div/div[1]/div/div[2]/div/ul/li[1] /div[2]/div[2]/div[1]/div[2]/span
                        indice_confiance = driver.find_elements(By.XPATH, xpathtip+'/div[2]/div[2]/div[1]/div[2]/span')[0].text
                        ic = self.parseIC(indice_confiance)
                        tip.setIC(ic)
                        print ('indice confiance', indice_confiance)
                        if self.filtrerIC(ic):
                            continue
                    
                        #bookmaker
                        #/html/body/div[2]/div/div[3]/div/div/div[1]/div/div[2]/div/ul/li[2]  /div[2]/div[2]/div[1]/div[2]
                        #/html/body/div[2]/div/div[3]/div/div/div[1]/div/div[2]/div/ul/li[6]  /div[2]/div[2]/div[1]/div[2]
                        books = driver.find_elements(By.XPATH, xpathtip+'/div[2]/div[2]/div[1]/div[2]')[0].text
                        print ('books', books)
                        tip.setBooks(books)
                        if self.filtrerLive(books):
                            continue
                        #marche sport et dateEvt
                        #/html/body/div[2]/div/div[3]/div/div/div[1]/div/div[2]/div/ul/li[3]  /div[2]/div[2]/div[1]/div[3]
                        marcheSport_dateEvt = driver.find_elements(By.XPATH, xpathtip+'/div[2]/div[2]/div[1]/div[3]')[0].text
                        print ('marcheSport_dateEvt', marcheSport_dateEvt)
                        #Tennis / ATP / Kick off: 22 Sep 2017, 16:00
                        #Football / Argentina / Kick off: 22 Sep 2017, 22:05
                        #Football / China / Kick off: 22 Sep 2017, 11:35
                        (marche, dateEvt) = self.parseMarcheDateEvt(marcheSport_dateEvt)
                        tip.setMarche(marche)
                        tip.setDateEvt(dateEvt)
                        
                    else:
                        choixGagnant = driver.find_elements(By.XPATH, xpathtip+'/div[2]/div[2]/div[2]')[0].text
                        print ('choixGagnant', choixGagnant)
                        tip.setChoixGagnant(choixGagnant)
                        
                        indice_confiance = driver.find_elements(By.XPATH, xpathtip+'/div[2]/div[2]/div[1]/div[2]/span')[0].text
                        ic = self.parseIC(indice_confiance)
                        tip.setIC(ic)
                        print ('indice confiance', indice_confiance)
                        if self.filtrerIC(ic):
                            continue
                    
                        #bookmaker
                        #/html/body/div[2]/div/div[3]/div/div/div[1]/div/div[2]/div/ul/li[2]  /div[2]/div[2]/div[1]/div[2]
                        books = driver.find_elements(By.XPATH, xpathtip+'/div[2]/div[2]/div[1]/div[2]')[0].text
                        tip.setBooks(books)
                        if self.filtrerLive(books):
                            continue
                        
                    #type pari
                    #/html/body/div[2]/div/div[3]/div/div/div[1]/div/div[2]/div/ul/li[2]/div[2]/div[2]/div[1]/div[1]
                    #type_pari = tip.find_elements(By.XPATH, '/div[2]/div[2]/div[1]/div[1]')
                    
                    #on conserve le tip s'il n'est pas deja present
                    clef = self.getClefTip(tip)
                    if not clef in self.bestTips:
                        print ('tip conserve')
                        self.bestTips[clef]=tip
                except BlogabetException.BlogWarning:
                    print ('Probleme avec ce pari')        
        except IndexError:
                print('plus de paris à ', datetime.datetime.now().isoformat())
                return 
        print ('Fin recherche tips à ', datetime.datetime.now().isoformat())    
    
    def getClefTip(self, tip):
        ''' construit une clef de hash pour un tip'''
        return tip.autheur+'-'+ str(tip.roi) + '%-' + tip.titre
    
    def getTip(self, clef):
        ''' retourne un tip en fonction de sa clef'''
        return self.bestTips[clef]
    
    def getAllTipsTriees(self,filtreRoi=10, filtreTips=50):
        '''
         methode qui retourne tous les tips selon un ordre de tri sur la date
         retourne un tableau d'objets Modele Videos
         p1 filtre roi
         p2 filtre tips
        '''
        l=list(self.bestTips.values())
        #filtrer la liste
        lfiltree = [x for x in l if x.roi >= filtreRoi and x.nbtips >= filtreTips] # Plus simple que filter, également :)
 
        return sorted(lfiltree, key=lambda t:t.dateEvt)
        