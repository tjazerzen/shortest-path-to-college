from model import *

model = Model.iz_datoteke(ime_datoteke="podatki_grafov.json")

luka = Uporabnik.iz_datoteke("Luka")

luka.dodaj_iskanje("BritofKR", "PostajaJadranska", 1)
luka.dodaj_iskanje("Kobarid", "PostajaJadranska", 2)


luka.v_datoteko()

print(luka)