from graf import Graf, Vozlisce, Povezava

# TODO: Ugotovi, kako v drugo datoteko uvoziš spremenljivko
# TODO: Ugotovi, kako uporabljaš orodje replace

britof_kr = Vozlisce("BritofKR")
kranj_ap = Vozlisce("KranjAP")
ljubljana_tivoli = Vozlisce("LjubljanaTivoli")
postaja_jadranska = Vozlisce("PostajaJadranska")
fmf = Vozlisce("FMF")
ljubljana_zelezniska = Vozlisce("LjubljanaZelezniska")
kranj_zelezniska =Vozlisce("KranjZelezniska")

graf = Graf()

graf.dodaj_tocke([britof_kr, kranj_ap, ljubljana_tivoli, postaja_jadranska, fmf, ljubljana_zelezniska, kranj_zelezniska])

graf.dodaj_usmerjeno_povezavo(britof_kr, kranj_ap)
graf.dodaj_usmerjeno_povezavo(kranj_ap, britof_kr)

graf.dodaj_usmerjeno_povezavo(kranj_ap, ljubljana_tivoli)
graf.dodaj_usmerjeno_povezavo(ljubljana_tivoli, kranj_ap)

graf.dodaj_usmerjeno_povezavo(ljubljana_tivoli, postaja_jadranska)
graf.dodaj_usmerjeno_povezavo(postaja_jadranska, ljubljana_tivoli)

graf.dodaj_neusmerjeno_povezavo(ljubljana_tivoli, fmf, 17)
graf.dodaj_neusmerjeno_povezavo(postaja_jadranska, fmf, 2)
graf.dodaj_neusmerjeno_povezavo(ljubljana_zelezniska, fmf, 20)

graf.dodaj_usmerjeno_povezavo(ljubljana_zelezniska, kranj_zelezniska)
graf.dodaj_usmerjeno_povezavo(kranj_zelezniska, britof_kr)
graf.dodaj_usmerjeno_povezavo(postaja_jadranska, ljubljana_zelezniska)


# Testiranje izpisa za točko
print(graf.tocka(fmf.ime)) # Vrne objekt točka
print(graf.tocka("Točke s tem imenom ni v grafu."))
print("")

# Testiranje izpisa za povezavo
for povezava in graf.tocke[fmf]:
    print(povezava)
print("")

# Testiranje izpisa za graf
print(graf)
print("")

# Testiranje funkcije vrni_sosednja_vozlisca
for sosednje_vozlisce in graf.vrni_sosednja_vozlisca(fmf):
    print(sosednje_vozlisce)
for sosednje_vozlisce in graf.vrni_sosednja_vozlisca("fmf"):
    print(sosednje_vozlisce)
print("")

# Testiranje funkcije vrni_sosednje_povezave
for sosednja_povezava in graf.vrni_sosednje_povezave(fmf):
    print(sosednja_povezava)
print("")