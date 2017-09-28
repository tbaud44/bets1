#-*- coding: utf-8 -*-
'''
Created on 30 mai 2017

@author: HOME
Frame permettant de saisir une fiche d'une ba,pub
'''

from Modele.Tip import Tip,Status
from transverse.Util import Util
import tkinter as tk


class Fiche(object):
    '''
    Fenetre, type formulaire, permettant de saisir infos d'une video: pub, ba, animBeaulieu
    '''


    def __init__(self, rootTK):
        '''
        Constructor
        '''
        self.tk=rootTK
        
        '''
        affiche la frame avec ses composants
        '''
    def afficher(self, tip:Tip):
        wdw = tk.Toplevel()
        wdw.geometry(Util.configValue('dimensions', 'geometryFiche'))
        
       # wdw.geometry("{}x{}+{}+{}".format(300, 390, 400, 300))
        #wdw.geometry('+400+300')
        self.tip = tip
        self.frame = wdw
        self.__dessiner()
        
        #rendre la fenetre modale
        wdw.transient(self.tk)
        wdw.grab_set()
        self.tk.wait_window(wdw)
          
    def __dessiner(self):
        
        master = self.frame
        tip = self.tip
        """construit les widgets """
        frameFiche = tk.LabelFrame(master, width=18, height=55, text='Detail Tip ')

        
        tk.Label(frameFiche, width = 15,text='Titre').grid(in_=frameFiche, sticky=tk.W, row=1, column=1)
        self.entryTitre= tk.Entry(frameFiche, width = 50)
        self.entryTitre.grid(in_=frameFiche, sticky=tk.W, row=1, column=2)
    
        '''affectation donnee '''
        self.entryTitre.insert(0, tip.titre)
        self.entryTitre.config(state=tk.DISABLED)
        
        tk.Label(frameFiche, width=15, text='Date Evt').grid(in_=frameFiche, sticky=tk.W, row=2, column=1)
        self.entryDateEvt= tk.Entry(frameFiche, width = 25)
        self.entryDateEvt.grid(in_=frameFiche, sticky=tk.W, row=2, column=2)
        '''affectation donnee '''
        self.entryDateEvt.insert(0, tip.dateEvt.strftime('%d %b %Y, %H:%M'))
        self.entryDateEvt.config(state=tk.DISABLED)
        
        
        tk.Label(frameFiche, width=15, text='Roi').grid(in_=frameFiche, sticky=tk.W, row=3, column=1)
        self.entryRoi= tk.Entry(frameFiche, width = 10)
        self.entryRoi.grid(in_=frameFiche, sticky=tk.W, row=3, column=2)
        '''affectation donnee '''
        self.entryRoi.insert(0, str(tip.roi))
        self.entryRoi.config(state=tk.DISABLED)
        
        tk.Label(frameFiche, width = 15,text='Nb tips history').grid(in_=frameFiche, sticky=tk.W, row=4, column=1)
        self.entryNbtips= tk.Entry(frameFiche, width = 25)
        self.entryNbtips.grid(in_=frameFiche, sticky=tk.W, row=4, column=2)
    
        '''affectation donnee '''
        self.entryNbtips.insert(0, str(tip.nbtips))
        self.entryNbtips.config(state=tk.DISABLED)
        
        tk.Label(frameFiche, width=15, text='ChoixGagnant').grid(in_=frameFiche, sticky=tk.W, row=5, column=1)
        self.entryChoixGagnant= tk.Entry(frameFiche, width = 70)
        self.entryChoixGagnant.grid(in_=frameFiche, sticky=tk.W, row=5, column=2)
        '''affectation donnee '''
        self.entryChoixGagnant.insert(0, tip.choixGagnant)
        self.entryChoixGagnant.config(state=tk.DISABLED)
        
        tk.Label(frameFiche, width=15, text='Indice confiance').grid(in_=frameFiche, sticky=tk.W, row=6, column=1)
        self.entryIC= tk.Entry(frameFiche, width = 10)
        self.entryIC.grid(in_=frameFiche, sticky=tk.W, row=6, column=2)
        '''affectation donnee '''
        self.entryIC.insert(0, str(tip.ic))
        self.entryIC.config(state=tk.DISABLED)
        
        tk.Label(frameFiche, width=15, text='Books').grid(in_=frameFiche, sticky=tk.W, row=7, column=1)
        self.entryBooks= tk.Entry(frameFiche, width = 35)
        self.entryBooks.grid(in_=frameFiche, sticky=tk.W, row=7, column=2)
        '''affectation donnee '''
        self.entryBooks.insert(0, tip.books)
        self.entryBooks.config(state=tk.DISABLED)
        
        tk.Label(frameFiche, width=15, text='Marche').grid(in_=frameFiche, sticky=tk.W, row=8, column=1)
        self.entryMarche= tk.Entry(frameFiche, width = 70)
        self.entryMarche.grid(in_=frameFiche, sticky=tk.W, row=8, column=2)
        '''affectation donnee '''
        self.entryMarche.insert(0, tip.marche)
        self.entryMarche.config(state=tk.DISABLED)
        
        tk.Label(frameFiche, width=15, text='Date enreg').grid(in_=frameFiche, sticky=tk.W, row=9, column=1)
        self.entryMarche= tk.Entry(frameFiche, width = 25)
        self.entryMarche.grid(in_=frameFiche, sticky=tk.W, row=9, column=2)
        '''affectation donnee '''
        self.entryMarche.insert(0, tip.dateEnreg.strftime('%d %b %Y, %H:%M'))
        self.entryMarche.config(state=tk.DISABLED)
        
        #analyse
        S = tk.Scrollbar(frameFiche)
        self.textAnalyse = tk.Text(frameFiche, height=7, width=50)
        #S.pack(side=tk.RIGHT, fill=tk.Y)
        S.config(command=self.textAnalyse.yview)
        self.textAnalyse.config(yscrollcommand=S.set)
        self.textAnalyse.grid(in_=frameFiche, sticky=tk.W, row=10, column=2)
    
        '''affectation donnee '''
        self.textAnalyse.insert(tk.END, tip.analyse)
        self.textAnalyse.config(state=tk.DISABLED)
        
        self.varStatusTip = tk.IntVar()
        self.varStatusTip.set(tip.status.value)
        
        radATTENTE = tk.Radiobutton(
            master, text="ATTENTE",
            variable=self.varStatusTip,
            value= Status.ATTENTE.value,
            command=self.__rbChecked)
        radATTENTE.grid(in_=frameFiche, pady=5, sticky=tk.W, row=11, column=1)
        
        radPRIS = tk.Radiobutton(
            master, text="PRIS",
            variable=self.varStatusTip,
            value= Status.PRIS.value,
            command=self.__rbChecked)
        radPRIS.grid(in_=frameFiche, sticky=tk.W, row=11, column=2)
        
        radABSENT = tk.Radiobutton(
            master, text="ABSENT",
            variable=self.varStatusTip,
            value= Status.ABSENT.value,
            command=self.__rbChecked)
        
        radABSENT.grid(in_=frameFiche, sticky=tk.W, row=12, column=1)
        
        radREFUSE = tk.Radiobutton(
            master, text="REFUSE",
            variable=self.varStatusTip,
            value= Status.REFUSE.value,
            command=self.__rbChecked)
        radREFUSE.grid(in_=frameFiche, sticky=tk.W, row=12, column=2)
         
         
        '''ajout des 2 boutons'''
        boutonAnnuler=tk.Button(master, width=10, text="Annuler", command=master.destroy)
           
        boutonEnregistrer=tk.Button(master, width=10, text="Enregistrer", command=self.__enregistrerFicheTip)
          #  .grid(in_=frameFiche, sticky=tk.W, padx=5, pady=5, row=8, column=2)
        
        frameFiche.pack(padx=15, pady=15)
        boutonAnnuler.pack(side=tk.LEFT, padx=15)
        boutonEnregistrer.pack(side=tk.RIGHT, padx=15)
        
    def __rbChecked(self):
        '''methode appelle lors d'un click sur radio button fiche'''
        print ('chgt status tip', str(self.varStatusTip.get()))
        
    def __enregistrerFicheTip(self):
        '''methode appelle lors d un click sur bouton enregistrer'''
        '''on enregistre les donnees modifiables'''    
        #seul le status peut changé
        statut = self.varStatusTip.get()
        if (statut ==1):
            self.tip.status = Status.ATTENTE
        if (statut ==2):
            self.tip.status = Status.PRIS
        if (statut ==3):
            self.tip.status = Status.ABSENT
        if (statut ==4):
            self.tip.status = Status.REFUSE
        self.frame.destroy()    
            
        