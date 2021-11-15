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

translator = Translator()

#Introduction
translation = translator.translate('''It's a test, to testify the good working of the module''', dest="fr")
titre_text = (f"{translation.text}")
print(titre_text)
cond = str(input('Le texte est-il en français ? (o/n): '))
if cond=='n':
	print("Réessayer plus tard")
	time.sleep(2)
	sys.exit()
Origine = []
traduction = []
with open('Nom_propre.txt') as Nom:
    Nom_lec = csv.reader(Nom)
    for row in Nom_lec:
        Origine.append(row[0])
        traduction.append(row[1])
Nom.close()
print('''Donnez l'url du roman (sur BestlightNovel uniquement pour le mmoment): ''')
url = input('Exemple :https://bestlightnovel.com/novel_888159695/chapter_84 \n')
dep = input('Donnez le chapitre de départ: ')
arr = input('Donnez le chapitre de fin (delta max 60): ')
url2 = list(url)
del(url2[51:len(url2)])
url2 = str(''.join(url2))
Titre_doc = input('Donnez le titre du document pdf: ')

#Peaufinage
print("{Courier, Helvetica, Times, Arial}")
police_ec = input("Quel police d'écriture ? \n")
Taille_Pol_Tit = input('Taille de la police des titres: ')
Taille_Pol_norm = input('Taille de la police du texte: ')

#url_source_SL3 = "https://bestlightnovel.com/novel_888159695/chapter_"
#url_source_T = "https://bestlightnovel.com/novel_888120245/chapter_"

Remplacement = len(Origine)
pdf = FPDF() 
for k in arange(eval(dep),eval(arr),1):

	pdf.add_page() 
	pdf.set_font("Arial", size = 12) 

	reponse = requests.get(str(url2)+str(k))
	soup = bs4.BeautifulSoup(reponse.text, "html.parser")
	f = open('Script'+str(k)+'_0.txt','w', encoding='utf-8')
	f.write(soup.prettify() + '\n')
	f.close()
	
	def Trouver_ligne(fichier_txt, string_a_chercher):
	    """Donne la ligne du string (vecteur) string demandé"""
	    num_ligne = 0
	    resultat = []
	    with open(fichier_txt, 'r', encoding='utf-8') as fichier_lecture:
	        for ligne in fichier_lecture:
	            num_ligne += 1
	            if string_a_chercher in ligne:
	                resultat.append(num_ligne)
	    fichier_lecture.close()
	    return resultat
	
	def replace_line(file_name, line_num, text):
	    lines = open(file_name, 'r', encoding='utf-8').readlines()
	    lines[line_num] = text
	    out = open(file_name, 'w', encoding='utf-8')
	    out.writelines(lines)
	    out.close()

	def intersection_list(liste1,liste2):
		resultat = list(set(liste1).intersection(set(liste2)))
		return sorted(resultat)

	def union_list(liste1,liste2):
		resultat = list(set(liste1 + liste2))
		return sorted(resultat)

	
	titre = Trouver_ligne('Script'+str(k)+'_0.txt','<h1 class="name_chapter">')

	#Pour le titre du chapitre
	# Le traducteur
	# Post-traduction nom propre Titre
	ft = open('Script'+str(k)+'_0.txt','r', encoding='utf-8')
	Vect_nom = list(ft.readlines()[titre[0]])
	ft.close()
	Vect_nom = str(''.join(Vect_nom))
	translation = translator.translate(str(Vect_nom), dest="fr")
	titre_text = (f"{translation.text}")
	print(titre_text)

	# Ecrit le titre dans le pdf
	titre_text=titre_text.encode('latin-1', 'ignore').decode('latin-1')
	pdf.set_font(police_ec, 'B', size=eval(Taille_Pol_Tit))
	pdf.multi_cell(0, 6, txt = titre_text+'\n'+'\n', align = 'C') 
	pdf.set_font(police_ec, size=eval(Taille_Pol_norm))

	# Conserve que le texte et supprime le <br/>
	deb = Trouver_ligne('Script'+str(k)+'_0.txt','''<div class="vung_doc" id="vung_doc"''')
	fin = Trouver_ligne('Script'+str(k)+'_0.txt','''<div style="width:''')

	with open('Script'+str(k)+'_0.txt', 'r+', encoding='utf-8') as fp:
	    lines = fp.readlines()
	    fp.seek(0)
	    fp.truncate()
	    for number, line in enumerate(lines):
	        if number in range(deb[0],fin[0]-3):
	            fp.write(line.replace('  ','').replace('<br/>','').replace('<strong>',''))
	    fp.close()	

	Ligne_paragpraphe = Trouver_ligne('Script'+str(k)+'_0.txt', '''<p>''')
	
	#supprime les indentations 
	with open('Script'+str(k)+'_0.txt', 'r+', encoding='utf-8') as fp:
	    lines = fp.readlines()
	    fp.seek(0)
	    fp.truncate()
	    for number, line in enumerate(lines):
	        if number in Ligne_paragpraphe[0:-1]:
	            fp.write(line.replace('<p>',''))
	    fp.close()

	#Tentative d'ajout de saut de ligne
	with open('Script'+str(k)+'_0.txt', 'r+', encoding='utf-8') as fp:
		lines = fp.readlines()
		fp.seek(0)
		fp.truncate()
		Concatenation = []

		for number, line in enumerate(lines):
			Phrase_sup = list(line)
			Phrase_verif = list(lines[number-1])
			for i in range(len(list(line))):
				#indentation
				if Phrase_sup[0]==' ':
					Phrase_sup.insert(0,'   ')
				#Premier guillemet
				if Phrase_sup[i]=='“':
					Phrase_sup[i]='«'
					Phrase_sup.insert(i,'\n')
					Phrase_sup.insert(i,'\n')
				try:
					if Phrase_sup[i]=='”':
						Phrase_sup[i]='»'
						Phrase_sup.insert(i+1,'\n')
						Phrase_sup.insert(i+1,'\n')
				except IndexError:
					pass
				continue
				if not size(Phrase_sup)==1:
					if Phrase_sup[-2]=='”':
						Phrase_sup.extend('\n')
			Concatenation.extend(Phrase_sup)
		# Pour les trop de \n
		for j in range(len(Concatenation)):
			try:
				if Concatenation[j]=='\n':
					if Concatenation[j+1]=='   ':
						if Concatenation[j+2]==' ':
							if Concatenation[j+3]=='\n':
								if Concatenation[j+4]=='\n':
									del(Concatenation[j])
					if Concatenation[j+1]=='\n':
						if Concatenation[j+2]=='\n':
							del(Concatenation[j])
			except IndexError:
				pass
			continue
		for j in range(len(Concatenation)):
			#Grosses merdes d'anglais qui ne savent pas écrire
			try:
				if Concatenation[j]=='.':
					if Concatenation[j-1]==' ':
						del(Concatenation[j-1])
			except IndexError:
				pass
			continue
		fp.write(''.join(Concatenation))
	fp.close()

	# Le traducteur
	f = open('Script'+str(k)+'_0.txt','r', encoding='utf-8')
	with open('Script'+str(k)+'_1.txt', 'w', encoding='utf-8') as fp:
		translation = translator.translate(f.read(), dest="fr")
		fp.write(f"{translation.text}")
		fp.close()
	f.close()
	
	Remplacement = len(Origine)
	# Post-traduction nom propre
	for i in range(Remplacement):
		fin = open("Script"+str(k)+"_"+str(1+i)+".txt", "rt", encoding='utf-8')
		fout = open("Script"+str(k)+"_"+str(i+2)+".txt", "wt", encoding='utf-8')
		for ligne in fin:
			fout.write(ligne.replace(Origine[i], traduction[i]))
		fin.close()
		fout.close()
	
	for i in range(Remplacement+1):
		if os.path.exists("Script"+str(k)+"_"+str(i)+".txt"):
			os.remove("Script"+str(k)+"_"+str(i)+".txt")
		else:
			print("problème de suppression")


	# Ecrit dans le pdf le texte
	doc = open("Script"+str(k)+"_"+str(Remplacement+1)+".txt", "r", encoding='utf-8') 
	for g in doc: 
		g=g.encode('latin-1', 'ignore').decode('latin-1')
		pdf.multi_cell(0, 6, txt = g, align = 'L') 

doc.close()
for k in arange(eval(dep),eval(arr),1):
	if os.path.exists("Script"+str(k)+"_"+str(Remplacement+1)+".txt"):
		os.remove("Script"+str(k)+"_"+str(Remplacement+1)+".txt")
	else:
		print("problème de suppression")

if os.path.exists("Script0_0.txt"):
	os.remove("Script0_0.txt")

pdf.output(str(Titre_doc)+".pdf").encode('latin-1','ignore')
