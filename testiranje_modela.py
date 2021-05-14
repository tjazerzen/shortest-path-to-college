from model import Model, Uporabnik
from graf1 import graf1 as g1

moj_model = Model([g1])

moj_model.v_datoteko()

prvi_uporabnik = Uporabnik.preberi_iz_datoteke("podatki_prvega_uporabnika.json")
print(prvi_uporabnik)