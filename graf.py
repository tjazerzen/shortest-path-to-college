from datetime import datetime


class Vozlisce:
    
    def __init__(self, ime):
        self.sosedi = []
        self.ime = ime
    
    def dodaj_soseda(self, nov_sosed):
        self.sosedi.append(nov_sosed)
        return nov_sosed
    
    def izpisi_se(self):
        return self.ime + ": " + ", ".join([sosed.ime for sosed in self.sosedi]) + "\n"


class Povezava:

    def __init__(self, vozlisce1: Vozlisce, vozlisce2: Vozlisce, fiksna_utez: bool, utez):
        self.vozlisce1 = vozlisce1
        self.vozlisce2 = vozlisce2
        self.fiksna_utez = fiksna_utez 
        ''' fiksna_utez nam pove, ce bo cas potovanja odvisen od voznje avtobusov ali ne
         Ta atribut imajo tiste povezave, po katerih se lahko sprehajamo/ vozimo s kolesom.
         ce je fiksna_utez = False, bo objekt povezave skonstruiran z specificirano utezjo. Sicer je utez = 0. '''
        vozlisce1.dodaj_soseda(vozlisce2)
        vozlisce2.dodaj_soseda(vozlisce1)
        self.utez = utez

    def izracunaj_se(self, cas_vpogleda: datetime = datetime.now()):
        '''
        Nastavi utez na vozlisce v odvisnosti od casa, ob katerem hocemo povezavo prehoditi.
        ce je utez fiksna, je to neodvisno od casa. Sicer pa pregledamo tekstovne datoteke.
        '''


class Graf:
    
    def __init__(self):
        self.tocke = {} 
    
    def tocka(self, ime):
        ''' Vrne tocko z danim imenom. Če v grafu takega imena ni, vrne None. '''
        if ime in self.tocke.keys():
            return self.tocke[ime]
        return None

    def dodaj_tocko(self, tocka):
        ''' Doda eno novo točko v naš graf. Vrne to točko. '''
        self.tocke[tocka.ime] = tocka
        return tocka

    def dodaj_tocke(self, tocke):
        ''' Doda nekaj novih točk v naš graf. Ne vrne ničesar. '''
        for tocka in tocke:    
            self.dodaj_tocko(tocka)
    
    def dodaj_povezavo(self, vozlisce1: Vozlisce, vozlisce2: Vozlisce, fiksna = False, utez = -1):
        ''' Doda novo povezavo v naš Graf (če sta točki različni). Skonstruira nov objekt razreda Povezava in ga vrne.
            Če je fiksna == True, bo utez izračunana z metodo Tocka().izracunaj_se() v odvisnosti od časa poizvedbe.
        '''
        if vozlisce1 != vozlisce2:
            return Povezava(vozlisce1, vozlisce2, fiksna, utez)
        return None
    
    def __str__(self):
        ''' Izpiše nam podatke o našem grafu. '''
        izpis = ""
        for tocka in self.tocke.values():
            izpis += tocka.izpisi_se()
        return izpis
        

    @staticmethod
    def dijkstra(vozlisce_start: Vozlisce, vozlisce_end: Vozlisce):
        '''
    
        Poišče najkrajšo pot od start_vertex do vseh ostalih.
        Vrne najmanjšo ceno od start_vertex do end_vertex, 
        zraven pa skonstruira še našo pot potovanja.
        '''
        return 104, [1, 6, 42]



britof_kr = Vozlisce("BritofKR")
kranj_ap = Vozlisce("KranjAP")
ljubljana_tivoli = Vozlisce("LjubljanaTivoli")
postaja_jadranska = Vozlisce("PostajaJadranska")
fmf = Vozlisce("FMF")
ljubljana_zelezniska = Vozlisce("LjubljanaZelezniska")
kranj_zelezniska =Vozlisce("KranjZelezniska")

graf = Graf()

graf.dodaj_tocke(
    [britof_kr, kranj_ap, ljubljana_tivoli, postaja_jadranska, fmf, ljubljana_zelezniska, kranj_zelezniska]
    )

graf.dodaj_povezavo(britof_kr, kranj_ap)
graf.dodaj_povezavo(kranj_ap, ljubljana_tivoli)
graf.dodaj_povezavo(ljubljana_tivoli, postaja_jadranska)
graf.dodaj_povezavo(ljubljana_tivoli, fmf, fiksna=True, utez=17)
graf.dodaj_povezavo(postaja_jadranska, fmf, fiksna=True, utez=2)
graf.dodaj_povezavo(ljubljana_zelezniska, fmf, fiksna=True, utez = 20)
graf.dodaj_povezavo(ljubljana_zelezniska, kranj_zelezniska)
graf.dodaj_povezavo(kranj_zelezniska, britof_kr)
graf.dodaj_povezavo(postaja_jadranska, ljubljana_zelezniska)

print(graf)