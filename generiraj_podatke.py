import os
import random

def ignoriraj(ime):
    return ime == "untracked" or ime[0] in [".", "_"]

lst = []

def izpisi_vsebino_imenika(pot_imenika, zamik=0):
    for ime in sorted(os.listdir(pot_imenika)):
        polno_ime = os.path.join(pot_imenika, ime)
        if zamik == 2:
            print(polno_ime)
            lst.append(polno_ime)
        if os.path.isdir(polno_ime) and not ignoriraj(ime):
            izpisi_vsebino_imenika(polno_ime, zamik=zamik + 2)

izpisi_vsebino_imenika(".")

def vpisi_podatke(od_kdaj, do_kdaj, cas_voznje, korak):
    s = ""
    stevilo_vozenj = (do_kdaj - od_kdaj) // korak
    for stevilka_avtobusa in range(0, stevilo_vozenj):
        current_zacetek = od_kdaj + stevilka_avtobusa*korak
        current_pribitek = random.randint(-3, 3)
        if (600 < current_zacetek and 750 > current_zacetek) or (840 < current_zacetek and 1080 > current_zacetek):
            current_pribitek += 3
        s += f"{current_zacetek} {current_zacetek+cas_voznje+current_pribitek}\n"
    return s


print("ali to dela")

for full_path in lst:
    with open(full_path, "w") as f:
        if "BritofKR-KranjAP" in full_path:
            od_kdaj = 300
            do_kdaj = 1320
            cas_voznje = 15
            korak = 40
        elif "BritofKR-KranjZelezniska" in full_path:
            od_kdaj = 300
            do_kdaj = 1320
            cas_voznje = 20
            korak = 40
        elif "KranjAP-BritofKR" in full_path:
            od_kdaj = 300
            do_kdaj = 1320
            cas_voznje = 15
            korak = 50
        elif "KranjAP-LjubljanaTivoli" in full_path:
            od_kdaj = 240
            do_kdaj = 1380
            cas_voznje = 55
            korak = 15
        elif "KranjZelezniska-BritofKR" in full_path:
            od_kdaj = 295
            do_kdaj = 1320
            cas_voznje = 20
            korak = 50
        elif "KranjZelezniska-LjubljanaZelezniska" in full_path:
            od_kdaj = 240
            do_kdaj = 1440
            cas_voznje = 40
            korak = 60
        elif "LjubljanaTivoli-KranjAP" in full_path:
            od_kdaj = 240
            do_kdaj = 1380
            cas_voznje = 55
            korak = 15
        elif "LjubljanaTivoli-PostajaJad" in full_path:
            od_kdaj = 300
            do_kdaj = 1380
            cas_voznje = 13
            korak = 10
        elif "LjubljanaZelezniska-KranjZelezniska" in full_path:
            od_kdaj = 240
            do_kdaj = 1440
            cas_voznje = 40
            korak = 60
        elif "LjubljanaZelezniska-PostajaJad" in full_path:
            od_kdaj = 300
            do_kdaj = 1380
            cas_voznje = 17
            korak = 10
        elif "PostajaJadranska-LjubljanaZele" in full_path:
            od_kdaj = 300
            do_kdaj = 1380
            cas_voznje = 17
            korak = 10
        elif "PostajaJadranska-LjubljanaTivo" in full_path:
            od_kdaj = 300
            do_kdaj = 1380
            cas_voznje = 13
            korak = 10

        elif "Bled-BohinjskaBistrica" in full_path:
            od_kdaj = 330
            do_kdaj = 1260
            cas_voznje = 40
            korak = 45
        elif "BohinjskaBistrica-Bled" in full_path:
            od_kdaj = 330
            do_kdaj = 1260
            cas_voznje = 40
            korak = 45
        elif "Bled-LjubljanaTivoli" in full_path:
            od_kdaj = 330
            do_kdaj = 1260
            cas_voznje = 90
            korak = 30
        elif "LjubljanaTivoli-Bled" in full_path:
            od_kdaj = 330
            do_kdaj = 1260
            cas_voznje = 90
            korak = 30
        elif "Bled-Kranj" in full_path:
            od_kdaj = 330
            do_kdaj = 1260
            cas_voznje = 45
            korak = 30
        elif "Kranj-Bled" in full_path:
            od_kdaj = 330
            do_kdaj = 1260
            cas_voznje = 45
            korak = 30
        elif "Tolmin-LjubljanaTivoli" in full_path:
            od_kdaj = 330
            do_kdaj = 1260
            cas_voznje = 240
            korak = 100
        elif "LjubljanaTivoli-Tolmin" in full_path:
            od_kdaj = 330
            do_kdaj = 1260
            cas_voznje = 240
            korak = 100
        elif "Kobarid-Tolmin" in full_path:
            od_kdaj = 330
            do_kdaj = 1260
            cas_voznje = 20
            korak = 30
        elif "Tolmin-Kobarid" in full_path:
            od_kdaj = 330
            do_kdaj = 1260
            cas_voznje = 20
            korak = 30
        
        s = vpisi_podatke(od_kdaj, do_kdaj, cas_voznje, korak)
        f.write(s)