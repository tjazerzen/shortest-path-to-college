from model import *

moj_model = Model.iz_datoteke("podatki_grafov.json")

#prvi_uporabnik = Uporabnik("Tjaž Eržen")
#pripadajoc_graf = prvi_uporabnik.dodaj_novo_linijo(1)
#prvi_uporabnik.dodaj_iskanje("BritofKR", "FMF", 1)
#prvi_uporabnik.dodaj_iskanje("KranjZelezniska", "LjubljanaTivoli", 1)
#print(prvi_uporabnik)
#prvi_uporabnik.v_datoteko()

try:
    prvi_uporabnik = Uporabnik.iz_datoteke("Tjaž Eržen")
    print(prvi_uporabnik)
except FileNotFoundError:
    print("Nisem našel datoteke pod imenom Tjaž Eržen")

#for value in prvi_uporabnik.dobi_grafe_iz_stevilk_linij().values():
#    print(value)