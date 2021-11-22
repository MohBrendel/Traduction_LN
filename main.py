from __future__ import division
import sys
import time
from pprint import pprint
import bs4
from numpy import*
from math import*
import requests
import os
import csv
from fpdf import FPDF
from googletrans import Translator
from sspg import*
from bestlightnovel import*
from lightnovelworld import*

pdf = FPDF()
translator = Translator()

# Obtention du site
#|---------------------------------------------|
def reconnaissance(url):
	if url.find('bestlightnovel')!=-1:
		Site = 1
		return Site
	if url.find('lightnovelworld')!=-1:
		Site = 2
		return Site
#|---------------------------------------------|

#---------------------------------------------
#----------Vérification du module-------------
#---------------------------------------------
translation = translator.translate('''It's a test, to testify the good working of the module''', dest="fr")
titre_text = (f"{translation.text}")
print(titre_text)
cond = str(input('Le texte est-il en français ? (o/n): '))
if cond=='n':
	print("Réessayer plus tard")
	time.sleep(2)
	sys.exit()
# Si le module est vérifié, chargement du fichier de traduction manuel
Origine = []
traduction = []
with open('Nom_propre.txt') as Nom:
    Nom_lec = csv.reader(Nom)
    for row in Nom_lec:
        Origine.append(row[0])
        traduction.append(row[1])
Remplacement = len(Origine)
Nom.close()
#---------------------------------------------
#---------------------------------------------


#---------------Ecrire dans un PDF------------------
def Ecrire_PDF(titre_text,k,police_ec,Taille_Pol_norm,Taille_Pol_Tit,Remplacement):
	titre_text=('Chapitre '+str(k)+': '+TRADUCTION(titre_text)).encode('latin-1', 'ignore').decode('latin-1')
	pdf.set_font(police_ec, 'B', size=eval(Taille_Pol_Tit))
	pdf.multi_cell(0, 6, txt = titre_text+'\n'+'\n', align = 'C') 
	pdf.set_font(police_ec, size=eval(Taille_Pol_norm))

	doc = open("Script"+str(k)+"_"+str(Remplacement)+".txt", "r", encoding='utf-8') 
	for g in doc: 
		g=g.encode('latin-1', 'ignore').decode('latin-1')
		pdf.multi_cell(0, 6, txt = g, align = 'L') 
	doc.close()	

	for i in range(1,Remplacement+1):
		if os.path.exists("Script"+str(k)+"_"+str(i)+".txt"):
			os.remove("Script"+str(k)+"_"+str(i)+".txt")
		else:
			print("problème de suppression")
	if os.path.exists("Script"+str(k)+"_"+str(Remplacement+1)+".txt"):
		os.remove("Script"+str(k)+"_"+str(Remplacement+1)+".txt")
	else:
		print("problème de suppression")
	if os.path.exists("Script0_0.txt"):
		os.remove("Script0_0.txt")
#---------------Ecrire dans un PDF------------------


#---------------------------------------------
#---------------Traitement url----------------
#---------------------------------------------
print('''Donnez l'url du roman (sur BestlightNovel uniquement pour le mmoment): ''')
url = input('Exemple :https://bestlightnovel.com/novel_888159695/chapter_84 \n')
urlcond = reconnaissance(url)
dep = input('Donnez le chapitre de départ: ') # Obtention des bornes
arr = input('Donnez le chapitre de fin (delta max 50): ')

# Détermination du site de lightnovel
def traitement_url(url2,urlcond):
	if urlcond==1:
		index = url2.find('chapter_')
		url2=list(url2)
		del(url2[index+len(list('chapter_')):len(url2)])
		return str(''.join(url2))
	if urlcond==2:
		index = url2.find('chapter-')
		url2=list(url2)
		del(url2[index+len(list('chapter-')):len(url2)])
		return str(''.join(url2))
url2 = traitement_url(url,urlcond)
#---------------------------------------------
#---------------------------------------------

#Peaufinage PDF
#|------------------------------------------------------------|
Titre_doc = input('Donnez le titre du document pdf: ')
print("{Courier, Helvetica, Times, Arial}")
police_ec = input("Quel police d'écriture ? \n")
Taille_Pol_Tit = input('Taille de la police des titres: ')
Taille_Pol_norm = input('Taille de la police du texte: ')
#|------------------------------------------------------------|

if urlcond==1: #Pour bestlightnovel
	for k in range(eval(dep),eval(arr),1):
		pdf.add_page() 
		titre_text = Bestlightnovel(k,url2,Origine,traduction)
		Ecrire_PDF(titre_text,k,police_ec,Taille_Pol_norm,Taille_Pol_Tit,Remplacement)
if urlcond==2:
	for k in range(eval(dep),eval(arr),1):
		pdf.add_page() 
		titre_text = Lightnovelworld(k,url2,Origine,traduction)
		Ecrire_PDF(titre_text,k,police_ec,Taille_Pol_norm,Taille_Pol_Tit,Remplacement)

pdf.output(str(Titre_doc)+".pdf").encode('latin-1','ignore')