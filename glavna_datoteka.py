import os
import html
import pandas as pd
from ekstrakcija_podatkov import *

def zazeni() :
    
    podatki = {} #slovar, ki bo imel podatke o vseh etapah posebej
    na_leto_zmagovalci = {} #slovar, ki bo imel podatke o zmagovalcih Tour de France, zmagovalcih naslova Le Roi des montagnes in zmagovalcih naslova najboljšega šprinterja po letih

    zacetno_leto = 1903
    koncno_leto = 2025 #1. Tour je bil leta 1903, za zadnjega pa lahko na srečo in zadovoljstvo (ker so vtisi še sveži) vzamemo Tour iz leta 2025!
    leta = list(range(zacetno_leto, koncno_leto + 1))
    for leto in leta:

        # ZA ZMAGOVALCE NA SPLOŠNO:

        podatki_leto = { #kot začetno stanje damo 'ni podatka', saj v nekaterih primerih ni podatkov pred sredino tridsetih let prejšnjega stoletja)
            'zmagovalec tdf': 'ni podatka',
            'zmagovalec tdf drzava':'ni podatka',
            'zmagovalec tdf starost': 'ni podatka',
            'zmagovalec specialty' : 'ni podatka'
            
        }

        #spletna stran in vsebina html datoteke za zmagovalca toura
        url_tdf = url_leto_tdf(leto)
        html_tdf = url_to_str(url_tdf)


        #pobiranje in razvrščanje podatkov za zmagovalca tdf:
        if html_tdf:
            match_tdf = vzorec_zmagovalec_tdf.search(html_tdf)

            if match_tdf:
                specialty = match_tdf.group(1).strip() if match_tdf.group(1) else 'ni podatka'
                starost = match_tdf.group(2) if match_tdf.group(2) else 'ni podatka'
                narodnost = match_tdf.group(3).upper() if match_tdf.group(3) else 'ni podatka'
                priimek = match_tdf.group(4) if match_tdf.group(4) else 'ni podatka'
                ime = match_tdf.group(5).strip() if match_tdf.group(5) else 'ni podatka'
                

                podatki_leto.update({
                    'zmagovalec tdf': f"{ime} {priimek}" if ime and priimek else 'ni podatka',
                    'zmagovalec tdf drzava': narodnost,
                    'zmagovalec specialty': specialty,
                    'zmagovalec tdf starost': starost
                })

        
       
        na_leto_zmagovalci[leto] = podatki_leto
        print(leto, podatki_leto)
    

        
                
        # ZA ETAPE:

        url = url_leto(leto)
        html = url_to_str(url)

        # na določena leta toura ni bilo, zato ustrezna spletna stran ne obstaja
        if html :
            hits = re.findall(vzorec_etapa, html)
            for hit in hits :
                #url etape
                etapa_url = glavna_stran + hit[0] 

                #stevilka etape
                etapa_st = hit[1]

                #html zapis strani za posamezno etapo
                etapa_html = url_to_str(etapa_url)
                etapa = (etapa_st, leto)

                podatki_etape = {
                    'razdalja': 'ni podatka', #glede razloga pri 'ni podatka' velja isto kot zgoraj
                    'težavnost': 'ni podatka',
                    'visinska_razlika': 'ni podatka',
                    'profil_etape': 'ni podatka',
                    'ime in priimek zmagovalca' : 'ni podatka',
                    'narodnost zmagovalca' : 'ni podatka',
                    'ekipa zmagovalca' : 'ni podatka',
                    'čas zmagovalca': 'ni podatka',
                    'povprecna_hitrost': 'ni podatka'
                    
                }
                #od tu naprej moramo dati pogoje, saj obstaja par etap, ki nimajo v html dokumentu napisanih nobenih teh podatkov
                
                #razdalja
                match_razdalja = re.search(vzorec_razdalja, etapa_html)
                if match_razdalja:
                    razdalja = match_razdalja.group(1) + ' km'
                    if razdalja != '0 km':  # Če je razdalja "0 km", preskočimo etapo (ker je verjetno napačen podatek)
                        podatki_etape['razdalja'] = razdalja

                # Povprečna hitrost
                match_hitr = re.search(vzorec_povpr_hitrost, etapa_html)
                if match_hitr:
                    podatki_etape['povprecna_hitrost'] = match_hitr.group(1) + ' km/h'

                # težavnost oz. Profile score (razložen v ekstrakcija_podatkov.py)
                match_profil = re.findall(vzorec_profile_score, etapa_html)
                if match_profil:
                    podatki_etape['težavnost'] = match_profil[0]  # 

                # Višinska razlika
                match_visinska = re.findall(vzorec_visinska, etapa_html)
                if match_visinska:
                    podatki_etape['visinska_razlika'] = match_visinska[0]

                
                # Klasifikacija oz. profil etape:
                #p1: ravninska etapa
                #p2: hribovita etapa z ravnim ciljem
                #p3: hribovita etapa z vzponopm na cilju
                #p4: gorska etapa z ravnim ciljem
                #p5: gorska etapa z vzponom na cilju
                match_klas =  vzorec_klasifikacija.findall(etapa_html)
                if match_klas:
                    if match_klas[0] == 'p1':
                        podatki_etape['profil_etape'] = 'ravninska etapa'
                    if match_klas[0] == 'p2':
                        podatki_etape['profil_etape'] = 'hribovita etapa z ravnim ciljem'
                    if match_klas[0] == 'p3':
                        podatki_etape['profil_etape'] = 'hribovita etapa z vzponopm na cilju'
                    if match_klas[0] == 'p4':
                        podatki_etape['profil_etape'] = 'gorska etapa z ravnim ciljem'
                    if match_klas[0] == 'p5':
                        podatki_etape['profil_etape'] = 'gorska etapa z vzponom na cilju'

                #Podatki o zmagovalcu posamezne etape:
                match_zmag = vzorec_zmagovalec.search(etapa_html)
                if match_zmag:
                    narodnost = match_zmag.group(1).upper()
                    priimek = match_zmag.group(2).strip()
                    ime = match_zmag.group(3).strip()
                    ekipa = match_zmag.group(4).strip() if match_zmag.group(4) else (match_zmag.group(5).strip() if match_zmag.group(5) else 'ni podatka')
                    
                    podatki_etape['ime in priimek zmagovalca'] = ime + ' ' + priimek
                    podatki_etape['ekipa zmagovalca'] = ekipa
                    čas = match_zmag.group(6).strip() if match_zmag.group(6) else 'ni podatka'
                    podatki_etape['čas zmagovalca'] = čas
                    podatki_etape['narodnost zmagovalca'] = narodnost
                    
                podatki[etapa] = podatki_etape
            
                
    

   
        else : 
            continue
    print(podatki)
    return podatki , na_leto_zmagovalci


import csv
def shrani_podatke_v_csv(podatki, filename='etape.csv'):
     # vsi columni
     fieldnames = ['leto', 'etapa']
     # dodamo še etapo in leto iz ključev
     if podatki:
         prvi_kljuc = next(iter(podatki))
         fieldnames.extend(kljuc for kljuc in podatki[prvi_kljuc].keys() if kljuc not in fieldnames)

     with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:  # utf-8-sig za Excel
         pisec = csv.DictWriter(csvfile, fieldnames=fieldnames)
         pisec.writeheader()
         for (etapa, leto), data in podatki.items():
             vrstica = {'leto': leto, 'etapa': etapa}
             vrstica.update(data)
             pisec.writerow(vrstica)

def shrani_zmagovalce_v_csv(na_leto_zmagovalci, filename='letni_zmagovalci.csv'):
     fieldnames = ['leto']
     if na_leto_zmagovalci:
         prvi_kljuc = next(iter(na_leto_zmagovalci))
         fieldnames.extend(kljuc for kljuc in na_leto_zmagovalci[prvi_kljuc].keys() if kljuc not in fieldnames)

     with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
         pisec = csv.DictWriter(csvfile, fieldnames=fieldnames)
         pisec.writeheader()
         for leto, data in na_leto_zmagovalci.items():
             vrstica = {'leto': leto}
             vrstica.update(data)
             pisec.writerow(vrstica)

if __name__=="__main__" :
    podatki, na_leto_zmagovalci = zazeni()
    shrani_podatke_v_csv(podatki)
    shrani_zmagovalce_v_csv(na_leto_zmagovalci)
    print("Naprintano")
