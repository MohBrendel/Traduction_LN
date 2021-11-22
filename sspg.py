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
    
def TRADUCTION(texte_a_traduire):
    translator = Translator()
    '''Traduit le texte, ou la variable qui lui est donné, qu'importe sont type'''
    translation = translator.translate(str(texte_a_traduire), dest="fr")
    return (f"{translation.text}")