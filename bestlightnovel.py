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

#████████████████████████████████████████████████████
#████████████████████████████████████████████████████
#|				                      				|
#|				POUR BESTLIGHTNOVEL 				|
#|		                            				|
#████████████████████████████████████████████████████
#████████████████████████████████████████████████████

def Bestlightnovel(k,url2,Origine,traduction):
	translator = Translator()
	Remplacement = len(Origine)
		
	'''Récupère les le code html à l'url2 au chapitre k'''
	reponse = requests.get(str(url2)+str(k))
	soup = bs4.BeautifulSoup(reponse.text, "html.parser")
	f = open('Script'+str(k)+'_0.txt','w', encoding='utf-8')
	f.write(soup.prettify() + '\n')
	f.close()

	Remplacement=len(Origine)
	'''On a ici les lignes spécifiques à bestlightnovel'''
	titre = Trouver_ligne('Script'+str(k)+'_0.txt','<h1 class="name_chapter">')				# Donne le titre du chapitre
	ft = open('Script'+str(k)+'_0.txt','r', encoding='utf-8')
	Vect_nom = list(ft.readlines()[titre[0]])
	titre = str(''.join(Vect_nom))

	titre_text = str(titre)
	if titre_text.find(' - ')!=-1:
		ind = titre_text.find(' - '); Alter = list(titre_text[ind+len(list(' - ')):-1])
		titre_text = str(''.join(Alter))
	if titre_text.find(' – ')!=-1:
		ind = titre_text.find(' – '); Alter = list(titre_text[ind+len(list(' – ')):-1])
		titre_text = str(''.join(Alter))
	else:
		Alter = list(titre_text)
		j=0
		while (Alter[j] in ['1','2','3','4','5','6','7','8','9','0']==False):
			j+=1
		while Alter[j] in ['1','2','3','4','5','6','7','8','9','0']==True:
			j+=1
		try:
			titre_text = str(''.join(Alter[j+1:-1]))
		except IndexError:
			titre_text = ''
	for i in range(Remplacement-1):
		if titre_text == Origine[i]:
			titre_text = traduction[i]

	ft.close()

	deb = Trouver_ligne('Script'+str(k)+'_0.txt','''<div class="vung_doc" id="vung_doc"''') # Début du script qui nous intéresse
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

	with open('Script'+str(k)+'_0.txt', 'r+', encoding='utf-8') as fp:
		lines = fp.readlines()
		fp.seek(0)
		fp.truncate()
		for number, line in enumerate(lines):
			if number in Ligne_paragpraphe[0:-1]:
				fp.write(line.replace('<p>',''))
		fp.close()

	with open('Script'+str(k)+'_0.txt', 'r+', encoding='utf-8') as fp:
		lines = fp.readlines()
		fp.seek(0)
		fp.truncate()
		for number, line in enumerate(lines):
			if number in Ligne_paragpraphe[0:-1]:
				fp.write(line.rstrip('\n'))
		fp.close()

	'''Ici se fait la mise en page du roman'''
	'''Ici se fait la mise en page du roman'''
	'''Ici se fait la mise en page du roman'''
	'''Ici se fait la mise en page du roman'''

	texte_traite = []
	with open('Script'+str(k)+'_0.txt', 'r+', encoding='utf-8') as fp:
		lines = fp.readlines()
		fp.seek(0)
		fp.truncate()
		for number, line in enumerate(lines):
			texte = list(line)
			for i in range(len(line)):
				if texte[i]=='“' or texte[i]=='“':
					texte[i]='«'
					texte.insert(i,'\n')
					texte.insert(i,'\n')
				try:
					if texte[i]=='”' or texte[i]=='”':
						texte[i]='»'
						texte.insert(i+1,'\n')
						texte.insert(i+1,'\n')
				except IndexError:
					pass
				continue
			texte_traite.extend(texte)
		for i in range(len(texte_traite)):
			try:
				if texte_traite[i] == '\n':
					if texte_traite[i+1] == '\n':
						if texte_traite[i+2] == ' ':
							if texte_traite[i+3] == '\n':
								del(texte_traite[i+1])
			except IndexError:
				pass
			continue
		for i in range(len(texte_traite)):
			try:
				if texte_traite[i] == '\n':
					if texte_traite[i+1] == ' ':
						if texte_traite[i+2] == '\n':
							if texte_traite[i+3] == '\n':
								del(texte_traite[i])
			except IndexError:
				pass
			continue
		for i in range(len(texte_traite)):
			try:
				if texte_traite[i] == '\n':
					if texte_traite[i+1] == ' ':
							del(texte_traite[i+1])
			except IndexError:
				pass
			continue
		for i in range(len(texte_traite)):
			try:
				if texte_traite[i] == '\n':
					if texte_traite[i+1] == '\n':
						if texte_traite[i+2] == '\n':
							del(texte_traite[i])
			except IndexError:
				pass
			continue
		for i in range(len(texte_traite)):
			try:
				if texte_traite[i] == '\n':
					if texte_traite[i+1] == '\n':
						if texte_traite[i+2] == '\n':
							del(texte_traite[i])
			except IndexError:
				pass
			continue
		for i in range(len(texte_traite)):
			try:
				if texte_traite[i] == '\n':
					if texte_traite[i+1] == ',':
						if texte_traite[i+2] == '\n':
							del(texte_traite[i+1])
			except IndexError:
				pass
			continue
		fp.write(''.join(texte_traite))
	fp.close()

	f = open('Script'+str(k)+'_0.txt','r', encoding='utf-8')
	with open('Script'+str(k)+'_1.txt', 'w', encoding='utf-8') as fp:
		translation = translator.translate(f.read(), dest="fr")
		fp.write(f"{translation.text}")
		fp.close()
	f.close()
		
	# Post-traduction nom propre
	for i in range(Remplacement):
		fin = open("Script"+str(k)+"_"+str(1+i)+".txt", "rt", encoding='utf-8')
		fout = open("Script"+str(k)+"_"+str(i+2)+".txt", "wt", encoding='utf-8')
		for ligne in fin:
			fout.write(ligne.replace(Origine[i], traduction[i]))
		fin.close()
		fout.close()
	return titre_text


