from model import *

model = Model.iz_datoteke(ime_datoteke="podatki_grafov.json")

graf4 = Graf(stevilka_linije=4)

koper = Vozlisce("Koper")
piran = Vozlisce("Piran")
izola = Vozlisce("Izola")
portoroz = Vozlisce("Portoroz")
ljubljana_tivoli = Vozlisce("LjubljanaTivoli")
fmf = Vozlisce("PostajaJadranska")

graf4.dodaj_tocke([koper, piran, izola, portoroz, ljubljana_tivoli, fmf])

graf4.dodaj_neusmerjeno_povezavo(koper, piran, utez_povezave=43)
graf4.dodaj_neusmerjeno_povezavo(piran, izola, utez_povezave=20)
graf4.dodaj_neusmerjeno_povezavo(izola, portoroz, utez_povezave=13)
graf4.dodaj_neusmerjeno_povezavo(portoroz, piran, utez_povezave=7)
graf4.dodaj_neusmerjeno_povezavo(piran, ljubljana_tivoli, utez_povezave=130)
graf4.dodaj_neusmerjeno_povezavo(ljubljana_tivoli, portoroz, utez_povezave=180)
graf4.dodaj_neusmerjeno_povezavo(izola, fmf, utez_povezave=153)
graf4.dodaj_neusmerjeno_povezavo(ljubljana_tivoli, fmf)

print(graf4.dijkstra(piran, fmf))

print(graf4)

model.dodaj_nov_graf(graf4)

model.v_datoteko()