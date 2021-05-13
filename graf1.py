# Datoteka, ki generira naš prvi graf. Objekt graf1 je nadaljno uporabljen v datoteki model.py

britof_kr = Vozlisce("BritofKR")
kranj_ap = Vozlisce("KranjAP")
ljubljana_tivoli = Vozlisce("LjubljanaTivoli")
postaja_jadranska = Vozlisce("PostajaJadranska")
fmf = Vozlisce("FMF")
ljubljana_zelezniska = Vozlisce("LjubljanaZelezniska")
kranj_zelezniska = Vozlisce("KranjZelezniska")

graf1 = graf1()

graf1.dodaj_tocke([britof_kr, kranj_ap, ljubljana_tivoli, postaja_jadranska, fmf, ljubljana_zelezniska, kranj_zelezniska])

graf1.dodaj_usmerjeno_povezavo(britof_kr, kranj_ap)
graf1.dodaj_usmerjeno_povezavo(kranj_ap, britof_kr)

graf1.dodaj_usmerjeno_povezavo(kranj_zelezniska, britof_kr)
graf1.dodaj_usmerjeno_povezavo(britof_kr, kranj_zelezniska)

graf1.dodaj_usmerjeno_povezavo(kranj_ap, ljubljana_tivoli)
graf1.dodaj_usmerjeno_povezavo(ljubljana_tivoli, kranj_ap)

graf1.dodaj_usmerjeno_povezavo(ljubljana_tivoli, postaja_jadranska)
graf1.dodaj_usmerjeno_povezavo(postaja_jadranska, ljubljana_tivoli)

graf1.dodaj_neusmerjeno_povezavo(ljubljana_tivoli, fmf, 17)
graf1.dodaj_neusmerjeno_povezavo(postaja_jadranska, fmf, 2)
graf1.dodaj_neusmerjeno_povezavo(ljubljana_zelezniska, fmf, 20)

graf1.dodaj_usmerjeno_povezavo(ljubljana_zelezniska, kranj_zelezniska)
graf1.dodaj_usmerjeno_povezavo(postaja_jadranska, ljubljana_zelezniska)