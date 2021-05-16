from model import *

model = Model.iz_datoteke(ime_datoteke="podatki_grafov.json")

andrej = Uporabnik.iz_datoteke("Andrej Jamar")

print(andrej)

andrej.v_datoteko()