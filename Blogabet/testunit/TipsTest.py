'''
Created on 15 juil. 2017

@author: HOME
'''
import datetime
import os
import random
import unittest
from Controleur.TipsManager import TipsManager
from transverse import BlogabetException


class TipsTest(unittest.TestCase):


    def setUp(self):
        self.tm = TipsManager()
        


    def tearDown(self):
        pass


    def test_parseRoi(self):
        
        retour = self.tm.parseRoi('+29% (44)')
        self.assertEqual((29,44), retour)
        
        retour = self.tm.parseRoi('-52% (27)')
        self.assertEqual((-52,27), retour)
        
        retour = self.tm.parseRoi('+127% (11)')
        self.assertEqual((127,11), retour)
        
        #cas du 0% (nouveau parieur
        #0% (2)
        retour = self.tm.parseRoi('0% (2)')
        self.assertEqual((0,2), retour)
        
        try:
            retour = self.tm.parseRoi('titi (27)')
            self.fail('pas exception levee')
        except: BlogabetException.BlogWarning    
    
    def test_parseIC(self):
        
        retour = self.tm.parseIC('1/10')
        self.assertEqual(1, retour)
        
        retour = self.tm.parseIC('5/10')
        self.assertEqual(5, retour)
        
        retour = self.tm.parseIC('10/10')
        self.assertEqual(10, retour)
        
        try:
            retour = self.tm.parseIC('titi (27)')
            self.fail('pas exception levee')
        except: BlogabetException.BlogWarning    
    
    def test_parseMARCHE(self):
    #Tennis / ATP / Kick off: 22 Sep 2017, 16:00    
        (marche, d1) = self.tm.parseMarcheDateEvt('Tennis / ATP / Kick off: 22 Sep 2017, 16:00')
        self.assertEqual('Tennis / ATP / ', marche)
        d1Str = d1.strftime('%d %b %Y, %H:%M')
        self.assertEqual('22 Sep 2017, 16:00', d1Str)
        
        (marche, d1) = self.tm.parseMarcheDateEvt('Football / Argentina / Kick off: 22 Sep 2017, 22:05')
        self.assertEqual('Football / Argentina / ', marche)
        d1Str = d1.strftime('%d %b %Y, %H:%M')
        self.assertEqual('22 Sep 2017, 22:05', d1Str)
        
        try:
            retour = self.tm.parseIC('Tennis / ATP / VV: 22 Sep 2017, ')
            self.fail('pas exception levee')
        except: BlogabetException.BlogWarning    
        
    def test_filtrerLive(self):
        #exemple 1/10 LIVE Bet365
        self.assertTrue(self.tm.filtrerLive('1/10 LIVE Bet365'))
        self.assertFalse(self.tm.filtrerLive('1/10 188bet'))
          
         
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testPlPlay']
    unittest.main()