from model import *

model = Model.iz_datoteke(ime_datoteke="podatki_grafov.json")

bled = Vozlisce("Bled")
bohinjska_bistrica = Vozlisce("BohinjskaBistrica")
kranj = Vozlisce("KranjAP")
ljubljana_tivoli = Vozlisce("LjubljanaTivoli")
fmf = Vozlisce("PostajaJadranska")
tolmin = Vozlisce("Tolmin")
kobarid = Vozlisce("Kobarid")

graf2 = Graf(2)

graf2.dodaj_tocke([bled, bohinjska_bistrica, kranj, ljubljana_tivoli, fmf, tolmin, kobarid])

graf2.dodaj_neusmerjeno_povezavo(bled, bohinjska_bistrica)
graf2.dodaj_neusmerjeno_povezavo(bled, ljubljana_tivoli)
graf2.dodaj_neusmerjeno_povezavo(bled, kranj)
graf2.dodaj_neusmerjeno_povezavo(kranj, ljubljana_tivoli)
graf2.dodaj_neusmerjeno_povezavo(ljubljana_tivoli, tolmin)
graf2.dodaj_neusmerjeno_povezavo(tolmin, kobarid)
graf2.dodaj_neusmerjeno_povezavo(ljubljana_tivoli, fmf)

print(graf2.dijkstra(tolmin, fmf), "\n")

print(graf2)

model.dodaj_nov_graf(graf2)

model.v_datoteko()