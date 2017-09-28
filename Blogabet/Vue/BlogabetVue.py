#-*- coding: utf-8 -*-
'''
Created on 9 mai 2017

@author: Thierry Baudouin
classe qui dessine les widgets de la fenetre principale de l'ihm
ne contient pas de traitement ni de logique metier
'''
import time
from tkinter import Canvas
from datetime import datetime
from Controleur.TipsManager import TipsManager
from Vue.FicheTip import Fiche
import tkinter as tk
from transverse.Util import Util
from transverse import BlogabetException


#import progressbar
class Interface:
    
    '''Notre fenetre principale.
    Tous les widgets sont stockes comme attributs de cette fenetre.'''
    def __init__(self):
        super().__init__()
        
        self.root=tk.Tk()
        self.root.title(Util.configValue('commun', 'titre'))
        tk.Grid.columnconfigure(self.root,5,weight=1)
        tk.Grid.rowconfigure(self.root,2,weight=1)
        self.root.geometry(Util.configValue('commun', 'geometry'))
        self.root.configure(bg="#FEFEE2")
        #enreg StringVar
        self.tm = TipsManager()
        self.dicoWidget = {}
    
    def getId(self, id):
        return self.dicoWidget[id]
    
    def afficherEtatFirefox(self):
        svfirefox = self.getId('etatFirefox')
        
        if self.tm.lancerFirefox:
            svfirefox.set('FIREFOX ACTIVE')
        else:
            svfirefox.set('FIREFOX DESACTIVE')
       
        '''methode qui cree les objets graphiques fenetre principale'''   
    def dessiner(self):
        
        """construit les widgets """
        
        #L1C3 titre global
        #heureL1C6
        tk.Label(self.root, text='Best tips', font=('Helvetica', 13, 'bold'), width = 25).grid( sticky=tk.W, row=0, column=1)
        
        etatfirefox = tk.StringVar()
        self.dicoWidget['etatFirefox']=etatfirefox
        labelL1C2 = tk.Label(self.root, textvariable=etatfirefox, anchor=tk.NW, width=20, bg="#FEFEE2", font=('Helvetica', 10))
        labelL1C2.grid(row=1, column=1, padx=1, sticky=tk.W)
        self.afficherEtatFirefox()
        
        labelL2C3 = tk.Label(self.root, width = 15,text='Filtre ROI')
        labelL2C3.grid( sticky=tk.W, row=2, column=2)
        self.entryfiltreRoi= tk.Entry(self.root, width = 10)
        self.entryfiltreRoi.grid(sticky=tk.W, row=2, column=3)
        self.entryfiltreRoi.insert(0, str(self.tm.critere_roi))
    
        labelL2C4 = tk.Label(self.root, width = 15,text='Filtre TIPS')
        labelL2C4.grid( sticky=tk.W, row=2, column=4)
        self.entryfiltreTips= tk.Entry(self.root, width = 10)
        self.entryfiltreTips.grid(sticky=tk.W, row=2, column=5)
        self.entryfiltreTips.insert(0, str(self.tm.critere_tips))
    
        pwL3C1 = tk.PanedWindow(self.root, orient=tk.HORIZONTAL) #regroupe la liste et le sidebar
       
        listTips = tk.Listbox(pwL3C1, width=50, height=25)
        self.dicoWidget['listTips']=listTips
        
        sbar = tk.Scrollbar(pwL3C1)
        sbar.config(command=listTips.yview)
        listTips.config(yscrollcommand=sbar.set)
        #sbar.pack(side=RIGHT, fill=Y)
        
        pwL3C1.add(listTips)
        self.listTipsIHM = listTips
        pwL3C1.add(sbar)
        #ajout du menu contextuel
        self.creerMenuContextuel(listTips)
        # attach popup to frame
        listTips.bind("<Button-3>", self.popup)

        
        pwL3C1.grid(row=3, column=1, padx=5, sticky=tk.NW)

        
        #handler pour quitter application
        self.root.protocol("WM_DELETE_WINDOW", self.quitter)

        pwL9C1 = tk.PanedWindow(self.root, orient=tk.HORIZONTAL) #regroupe les 2 boutons
        
        #handler pour quitter application
        self.root.protocol("WM_DELETE_WINDOW", self.quitter)

        boutonQuitter=tk.Button(pwL9C1, command=self.quitter, text="Quitter") 
        boutonRefresh=tk.Button(pwL9C1, text="refresh", command=self.refresh)
        boutonEtatFirefox=tk.Button(pwL9C1, text="Etat firefox", command=self.chgtEtatFirefox)
               
        
        pwL9C1.add(boutonQuitter, width=80, height=35)
        
        pwL9C1.add(boutonRefresh,width=80, height=35)
        pwL9C1.add(boutonEtatFirefox,width=80, height=35)
        
        pwL9C1.grid(row=4, sticky=tk.NW, column=1, padx=5)
      
       # f = Fiche(self.root)
      #  f.afficher(self.bm.biblioGenerale.videos['Bande-Annonce Panique - Film 1946 (Drame).flv'])
        #########################"
    def creerMenuContextuel(self, bibliIHM):
        '''
        methode qui cree un menu contextuel sur la bibliotheque video
        '''
         # create a popup menu
        self.aMenu = tk.Menu(self.root, tearoff=0)
        self.aMenu.add_command(label="Fiche Tip" , command=self.afficheFrameFicheTip)
        self.aMenu.add_command(label="Supprimer", command=self.supprimerTip)
            
    def popup(self, event):
        '''
        methode evenement click droit qui affiche le menu contextuel
        '''
        self.aMenu.post(event.x_root, event.y_root)
     
        '''methode qui change etat appel firefox'''
    def chgtEtatFirefox(self):
        self.tm.lancerFirefox = not self.tm.lancerFirefox
        self.afficherEtatFirefox() 
        
    def _getCurrentTipBibli(self):
        '''
        methode qui retourne la selection tip de la liste
        '''
    # get selected line index
        listWidget = self.getId('listTips')  
        
        if not listWidget.curselection():
            raise BlogabetException.BlogException('selectionTipKO')
        index = listWidget.curselection()[0]
    # get the line's text
        selTip = listWidget.get(index)
        return selTip
    
        '''methode qui affiche une nouvelle fenetre avec le tip en detail'''
    def afficheFrameFicheTip(self):
        '''
        methode qui affiche la frame avec la fiche tip (attributs, nom, titre, date, etc ...)
        ''' 
        selTipIHM =self._getCurrentTipBibli()
        fiche = Fiche(self.root)
        tipObj = self.tm.getTip(selTipIHM)
        fiche.afficher(tipObj)
    
    '''methode qui supprime le tip '''
    def supprimerTip(self):
        
        i=4        
    
    
    def initialiserDonnees(self):
        '''methode qui charge l'ihm des donnees
          '''
        #toutes les minutes on lance firefox sur blogabet
        if self.tm.lancerFirefox:
            self.tm.rechercherTipsWeb()
            self.tm.save()
        duree=int(Util.configValue('commun', 'dureeSleepFirefox'))
        self.root.after(1000*duree, self.initialiserDonnees) 
            
    def refresh(self):
        '''methode qui affiche les donnees des tips calcules
          '''
        listWidget = self.getId('listTips')  
        listWidget.delete(0, tk.END)
        now = datetime.now()
        for tip in self.tm.getAllTipsTriees(filtreRoi=int(self.entryfiltreRoi.get()), filtreTips=int(self.entryfiltreTips.get())):
            listWidget.insert(tk.END, self.tm.getClefTip(tip))
            listWidget.itemconfig(tk.END, bg=self.tm.getColorTip(tip, now)) #couleur specifique selon la date du tip
         
        
 
    def quitter(self):
        '''methode de fin de l application'''
        '''sauvegarde sur disque'''
        self.tm.save()
        self.root.quit()
        #sauvegarde de la bibliotheque video memoire sur le disque (bib.obj)
    
        '''methode qui renvoie la valeur de la dimension d'un widget'''
    def _getDimension(self, codeDimensionWidget):
         return Util.configValue('dimensions', codeDimensionWidget)
      
    def mainLoop(self):
        '''
        methode qui gere la boucle evenement utilisateur
        '''     
        self.root.mainloop()  