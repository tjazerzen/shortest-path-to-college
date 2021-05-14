from model import Model, Uporabnik
from graf1 import graf1 as g1

#moj_model = Model.iz_datoteke("podatki_grafov.json")

#for graf in moj_model.grafi.values():
#    print(graf)


prvi_uporabnik = Uporabnik("Tjaž Eržen")
pripadajoc_graf = prvi_uporabnik.dodaj_novo_linijo(1)
#prvi_uporabnik.dodaj_iskanje("BritofKR", "KranjAP", 1)


print(prvi_uporabnik)



#for value in prvi_uporabnik.dobi_grafe_iz_stevilk_linij().values():
#    print(value)
