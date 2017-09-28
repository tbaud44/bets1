#-*- coding: utf-8 -*-
'''
Created on 17 mai 2017

@author: Thierry baudouin
classe de tip representant un pronostic sur un pari
'''
from datetime import datetime

from enum import Enum


class Status(Enum):
    ATTENTE = 1
    PRIS = 2
    ABSENT = 3
    REFUSE = 4
            
class Tip(object):
    '''
    classe de donnee representant une video
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.dateEnreg = datetime.now()
        self.status = Status.ATTENTE
        #self.dateEvt = dateEvt
        #self.book = book
        #self.titre = titre
        #self.indiceConfiance = indiceConfiance
        #self.analyse = analyse
      
    def setRoi(self, roi):
        self.roi = roi
        
    def setNbTips(self, nbTips):
        self.nbtips = nbTips
        
    def setTitre(self, titre):
        self.titre = titre
            
    def setChoixGagnant(self, choixGag):
        self.choixGagnant = choixGag
    
    #indice de confiance        
    def setIC(self, ic):
        self.ic = ic
            
    #bookmkers        
    def setBooks(self, books):
        self.books = books
    
    #autheur        
    def setAutheur(self, autheur):
        self.autheur = autheur
    
    #dateEvt        
    def setDateEvt(self, dateEvt):
        self.dateEvt = dateEvt
            
    #marche : rubrique du tip chez le bookmaker        
    def setMarche(self, marche):
        self.marche = marche
    
    #analyse : analyse du tip        
    def setAnalyse(self, analyse):
        self.analyse = analyse
            