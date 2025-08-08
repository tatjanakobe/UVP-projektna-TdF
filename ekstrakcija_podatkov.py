import re
import html
import os
import pandas as pd
from bs4 import BeautifulSoup as BS
import requests

#v tej datoteki so vzorci in par uporabnih pomožnih funkicij

glavna_stran = "https://www.procyclingstats.com/"

#spremeni url v niz vsebine html datoteke, do katere dostopamo s tem url-jem
def url_to_str(url) :
    return requests.get(url).text

#funkcije letu toura, ki nas zanima, priredijo ustrezno spletno stran glede na podatek, ki nas zanima:

def url_leto(leto) : #za razultate posamičnih etap v nekem letu 
    return f'https://www.procyclingstats.com/race/tour-de-france/{leto}/gc/result/result'

def url_leto_tdf(leto) : #za zmagovalca celotnega toura 
    return f'https://www.procyclingstats.com/race/tour-de-france/{leto}/gc'

def url_leto_kom(leto) : #za zmagovalca naslova 'king of the mountains'
    return f'https://www.procyclingstats.com/race/tour-de-france/{leto}/kom'

def url_leto_green(leto) : #za najboljšega šprinterja(ta ima oblečeno zeleno majico, zato je v nadaljnem kdaj, ko se nanaša na šprinterja, uporabljena spremenljivka z besedo 'green')
    return f'https://www.procyclingstats.com/race/tour-de-france/{leto}/points'


#VZORCI:

# na nekaterih tdf so etape razdeljene na a in b del, zato, da bi se izognili zmedi, v takih primerih izberemo le a del etape
vzorec_etapa = re.compile(r'<option value="(race/tour-de-france/\d+/stage-\d+(?:a)?/result/result)" ' + r'(?:selected)?' + '>Stage ' + r'(\d+)')

#za zmagovalca etape 
vzorec_zmagovalec = re.compile(
    r'<tr><td>1</td>.*?'  # matcha 1. vrstico tabele
    r'<td class="ridername\s*"[^>]*>.*?'
    r'<span class="flag\s+([a-z]{2})"></span>.*?'  # država kratica
    r'<a[^>]*><span class="uppercase">([^<]+)</span>\s*([^<]+)</a>.*?'  # priimek in ime
    r'(?:<div class="showIfMobile[^>]*>([^<]+)</div>.*?|'  
    r'<td class="cu600[^>]*><a[^>]*>([^<]+)</a>.*?)?'  # ekipa je le kdaj zapisana dvakrat, zato zadanemo oba za vsak slučaj
    r'<td class="time[^>]*><font>([^<]+)</font>',  # čas zmagovalca
    re.DOTALL
)


import re

vzorec_zmagovalec_tdf = re.compile(
    r'<td class="fs10 clr999 "[^>]*>.*?'  # začetek
    r'<td class="specialty "[^>]*>.*?<span class="fs10 clr999">([^<]+)</span>.*?'  # 1. specialnost
    r'<td class="age "[^>]*>(\d+)</td>.*?'  # 2. starost
    r'<span class="flag\s+([a-z]{2})"[^>]*>.*?'  # 3. narodnost
    r'<span class="uppercase">([^<]+)</span>\s*([^<]+)</a>.*?'  # 4. priimek, 5. ime
    r'(?:<div class="showIfMobile fs12 clr999"[^>]*>([^<]*)</div>.*?)?'  # 6. ekipa (mobile)
    r'(?:<a[^>]*data-bc="[^"]*"[^>]*>([^<]+)</a>.*?)?'  # 7. ekipa (link)
    r'(?:<td class="time ar "[^>]*><font>\s*([\d:]+)\s*</font>.*?)?',  # 8. čas 
    re.DOTALL | re.IGNORECASE
)



vzorec_povpr_hitrost = r'>Avg. speed winner: </div><div class=" value"\s*>([\d.]+)\s*km/h<'

vzorec_razdalja = r'>Distance: </div><div class=" value"\s*>([\d.]+)\s*km<'

#ProfileScore je lestvica, ki jo uporablja naša spletna stran, ki določi težavnost etape(profil). Višji, kot je ProfileScore, težja je etapa.Na spletni strani je razložen postopek oz. formula izračuna ProfileScore-a (povzeto po: https://www.procyclingstats.com/info/profile-score-explained):

#"we included three variables into our PCS ProfileScore formula:
#-Position of climb from finish
#-Steepness
#-Length of the climb
#
#First we compute the score for each individual climb in the stage by the following formula:
#([Steepness] / 2)^2 * [Length in KM]
#
#Then we multiply this score by a factor dependent of the distance from the finish line.""
#
vzorec_profile_score = r'ProfileScore:\s*</div>\s*<div class="[^"]*value[^"]*"\s*>(\d+)<'

vzorec_visinska = re.compile(r'Vertical meters:\s*</div>\s*<div\s+class="[^"]*value[^"]*"\s*>([\d.]+)\s*</div>')

#na spletni strani imajo namesto opisa, kakšna je etapa, slikico, ki opisuje težavnost in vrsto etape, vsaki slikici pa ustreza posebna oznaka v html datoteki, zato jih lahko preberemo in razvrstimo (na spletni strani je v angleščini naveden isti opis slikic kot spodaj):
#p1: ravninska etapa
#p2: hribovita etapa z ravnim ciljem
#p3: hribovita etapa z vzponopm na cilju
#p4: gorska etapa z ravnim ciljem
#p5: gorska etapa z vzponom na cilju
vzorec_klasifikacija = re.compile(r'class="[^"]*\bprofile\b[^"]*\b(p[1-5])\b')




       
        
        
       
       





    













