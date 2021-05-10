from datetime import datetime

# 1.: Definicija razredov Vozlišče, Povezava in Graf.

class Vozlisce:
    
    def __init__(self, ime):
        self.ime = ime
    
    def __str__(self):
        return self.ime


class Povezava:
    ''' Konstruira novo usmerjeno povezavo od vozlisce1 do vozlisce2. Za ustvarjanje neusmerjene povezave bom ustvaril nova dva objekta. '''
    def __init__(self, vozlisce1: Vozlisce, vozlisce2: Vozlisce, utez = -1):
        # vozlisce1 je zacetek povezave, vozlisce2 je konec povezave.
        self.vozlisce1 = vozlisce1
        self.vozlisce2 = vozlisce2
        if utez == -1:
            self.fiksna_utez = False # fiksna_utez == True --> Ceno povezave JE treba izračunati vedno znova.
        else:
            self.fiksna_utez = True # fiksna_utez == False --> Cene povezave NI treba izračunati vedno znova.
        ''' 
        fiksna_utez nam pove, če bo čas potovanja odvisen od časa vpogleda.
        Ta atribut imajo tiste povezave, po katerih se lahko sprehajamo/ vozimo s kolesom.
        če je fiksna_utez = False, bo objekt povezave skonstruiran z specificirano utezjo. Sicer je utež = -1. 
        '''
        self.utez = utez

    def izracunaj_se(self, cas_vpogleda = datetime.now()):
        # TODO: Iz casa vpogleda dobi zapis na minute natančen
        pass

    def __str__(self):
        return f"Začetek povezave: {self.vozlisce1}; Konec povezave: {self.vozlisce2}; Fiksna: {self.fiksna_utez}; utez: {self.utez}"


class Graf:
    
    def __init__(self):
        self.tocke = {} # {Key: Točka; Value: list povezav iz te točke}
    
    def tocka(self, ime):
        ''' Vrne točko z danim imenom. Če v grafu takega imena ni, vrne None. '''
        for tocka in self.tocke.keys():
            if tocka.ime == ime:
                return tocka
        return None

    def dodaj_tocko(self, tocka):
        ''' Doda eno novo točko v naš graf (brez sosedov). Vrne to točko. '''
        self.tocke[tocka] = set()
        return tocka
    
    def dodaj_tocke(self, tocke):
        ''' Doda nekaj novih točk v naš graf. Ne vrne ničesar. '''
        for tocka in tocke:    
            self.dodaj_tocko(tocka)
    
    def vrni_sosednja_vozlisca(self, tocka):
        ''' vrne vozlišča, ki so tej točki sosednja. Če take točke ni, vrne None. '''
        if tocka in self.tocke.keys():
            return [sosednja_povezava.vozlisce2 for sosednja_povezava in self.tocke[tocka]]
        return []
    
    def vrni_sosednje_povezave(self, tocka):
        ''' Vrne povezave, ki so tej točki sosednje. Če take točke ni, vrne None. '''
        if tocka in self.tocke.keys():
            return self.tocke[tocka]
        return []
    
    def dodaj_neusmerjeno_povezavo(self, vozlisce1: Vozlisce, vozlisce2: Vozlisce, utez_povezave):
        ''' 
        V graf doda neusmerjeno povezavo. 
        Ta ukaz bo generiral povezave za vožnjo s kolesom in hojo peš, kjer bo cena povezave v obe smeri enaka ter od časa vpogleda neodvisna. 
        Vse neusmerjene povezave bodo imele tudi fiksno ceno potovanja.
        '''
        if vozlisce1 == vozlisce2: return None # Trivivalen primer; zank ne bomo ustvarjali.
        self.tocke[vozlisce1].add(Povezava(vozlisce1, vozlisce2, utez = utez_povezave))
        self.tocke[vozlisce2].add(Povezava(vozlisce2, vozlisce1, utez = utez_povezave))
    
    def dodaj_usmerjeno_povezavo(self, vozlisce1: Vozlisce, vozlisce2: Vozlisce):
        ''' 
        V graf doda usmerjeno povezavo od vozlisce1 do vozlisce2.
        Ta ukaz bo generiral povezave za vožnjo s trolo in avtobusom, kjer cena povezave v eno in drugo smer ne bo enaka ter bo odvisna od časa vpogleda.
        Vsakič znova bo treba izračunati ceno povezave z metodo Povezava(...).izracunaj_se().
        Vse usmerjene povezave bodo imeli tudi nefiksno ceno potovanja.
        '''
        # Ustvarim nov objekt. Ker se bo utež vedno znova izračunala, je lahko karkoli. Tukaj jo postavim na -1.
        # Ker utež povezave ni fiksna, je fiksna = False.
        self.tocke[vozlisce1].add(Povezava(vozlisce1, vozlisce2, utez = -1))
    
    def __str__(self):
        ''' Izpiše nam podatke o našem grafu.'''
        izpis = ""
        for tocka in self.tocke.keys():
            izpis += tocka.ime + ": [" + "; ".join([sosednja_povezava.vozlisce2.ime + ": " + str(sosednja_povezava.utez) for sosednja_povezava in self.tocke[tocka]]) + "]\n"
        return izpis
        
    @staticmethod
    def dijkstra(vozlisce_start: Vozlisce, vozlisce_end: Vozlisce):
        # TODO: Razpiši algoritem.
        '''
        Poišče najkrajšo pot od start_vertex do vseh ostalih.
        Vrne najmanjšo ceno od start_vertex do end_vertex, 
        zraven pa skonstruira še našo pot potovanja.
        Output je oblike (<cena sprehoda>, <pot sprehoda>).
        '''
        return 104, [1, 6, 42]


# 2.: Konstrukcija grafa

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