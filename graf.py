from datetime import datetime
import math
# 1.: Definicija razredov Vozlišče, Povezava in Graf.

class Vozlisce:
    
    def __init__(self, ime):
        self.ime = ime
    
    def __str__(self):
        return self.ime


class Povezava:
    ''' Konstruira novo usmerjeno povezavo od vozlisce1 do vozlisce2. Za ustvarjanje neusmerjene povezave bom ustvaril dva enosmerna objekta. '''
    def __init__(self, vozlisce1: Vozlisce, vozlisce2: Vozlisce, utez = -1):
        # vozlisce1 je zacetek povezave, vozlisce2 je konec povezave.
        self.vozlisce1 = vozlisce1
        self.vozlisce2 = vozlisce2
        if utez == -1:
            self.fiksna_utez = False # fiksna_utez == False --> Ceno povezave JE treba izračunati vedno znova.
        else:
            self.fiksna_utez = True # fiksna_utez == True --> Cene povezave NI treba izračunati vedno znova.
        ''' 
        fiksna_utez nam pove, če bo čas potovanja odvisen od časa vpogleda.
        Ta atribut imajo tiste povezave, po katerih se lahko sprehajamo/ vozimo s kolesom.
        če je fiksna_utez = False, bo objekt povezave skonstruiran z specificirano utezjo. Sicer je utež = -1. 
        '''
        self.utez = utez

    def izracunaj_se(self, cas_vpogleda: datetime = datetime.now()):
        ''' 
        Izračuna utež na grafu v odvisnosti od časa. Če je povezava fiksna, bo cena vedno ista.
        Sicer: Pošči čas od cas_vpogleda do naslednjega odhoda avtobusa ter nastavi ceno povezave na <cas do odhoda> + <cas voznje>.
        '''
        if self.fiksna_utez:
            return self
        
        minute = self.dobi_minute_iz_casa(cas_vpogleda)
        ime_datoteke = self.vozlisce1.ime + "-" + self.vozlisce2.ime + ".txt" # Vse tekstovne datoteke imajo isto sintakso, vsa vozlišča pa tako ime, da je ime datoteke brez težav skonstruirati
        with open("./PodatkiOdhodov/" + ime_datoteke, "r") as input_file:
            for line in input_file.readlines():
                trenutna_vrsta = [int(data.strip()) for data in line.split()]
                trenutni_odhod, trenutni_prihod = trenutna_vrsta[0], trenutna_vrsta[1]
                if trenutni_odhod > minute:
                    self.utez = trenutni_prihod - minute
                    return self
            # Ura je preveč, da bi peljal še kakšen avtobus. Kar počakat na prvega naslednji dan ;)
            self.utez = 24*60 - minute + input_file.readlines().split()[0].strip()
            return self 
        
    @staticmethod
    def dobi_minute_iz_casa(datum: datetime = datetime.now()):
        return int(datum.strftime("%H")) * 60 + int(datum.strftime("%M"))

    def __str__(self):
        return f"Začetek povezave: {self.vozlisce1}; Konec povezave: {self.vozlisce2}; Fiksna: {self.fiksna_utez}; utez: {self.utez}"


class Graf:
    ''' Graf združuje vozlišča in povezave. Njegove informacije hranim v spremenljivki self.tocke '''
    def __init__(self):
        self.tocke = {} # {Key: Točka; Value: množica povezav z začetkom v tej točki}
    
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
        V graf doda neusmerjeno povezavo med vozliščema 1 in 2. 
        Ta ukaz bo generiral povezave za vožnjo s kolesom in hojo peš, kjer bo cena povezave v obe smeri enaka ter od časa vpogleda neodvisna. 
        Vse neusmerjene povezave bodo imele tudi fiksno ceno potovanja.
        '''
        if vozlisce1 == vozlisce2: return None # Trivivalen primer; zank ne bomo ustvarjali.
        return self.dodaj_usmerjeno_povezavo(vozlisce1, vozlisce2, utez=utez_povezave), self.dodaj_usmerjeno_povezavo(vozlisce2, vozlisce1, utez=utez_povezave)
    
    def dodaj_usmerjeno_povezavo(self, vozlisce1: Vozlisce, vozlisce2: Vozlisce, utez = -1):
        ''' 
        V graf doda usmerjeno povezavo od vozlisce1 do vozlisce2.
        Ta ukaz bo generiral povezave za vožnjo s trolo in avtobusom, kjer cena povezave v eno in drugo smer ne bo enaka ter bo odvisna od časa vpogleda.
        Vsakič znova bo treba izračunati ceno povezave z metodo Povezava(...).izracunaj_se().
        Vse usmerjene povezave bodo imeli tudi nefiksno ceno potovanja.
        '''
        # Ustvarim nov objekt. Ker se bo utež vedno znova izračunala, je lahko karkoli. Tukaj jo postavim na -1.
        # Ker utež povezave ni fiksna, je fiksna = False.
        return self.tocke[vozlisce1].add(Povezava(vozlisce1, vozlisce2, utez))
    
    def __str__(self):

        ''' Izpiše nam podatke o našem grafu. '''
        izpis = ""
        for tocka in self.tocke.keys():
            izpis += tocka.ime + ": [" + "; ".join([sosednja_povezava.vozlisce2.ime + ": " + str(sosednja_povezava.utez) for sosednja_povezava in self.tocke[tocka]]) + "]\n"
        return izpis
    
    def nastavi_vse_povezave(self, cas_vpogleda: datetime = datetime.now()):
        ''' Posodobi vrednosti uteži vseh povezav. Sprehodi se po vseh povezavah ter na vsaki posebi pokliče metodo za nastavitev uteži, definirano na objektu Povezava. '''
        for vozlisce, seznam_povezav in self.tocke.items():
            self.tocke[vozlisce] = {povezava.izracunaj_se(cas_vpogleda) for povezava in seznam_povezav}
        return self.tocke
        
    def dijkstra(self, vozlisce_start: Vozlisce, vozlisce_end: Vozlisce):
        # TODO: Razpiši algoritem.
        '''
        Poišče najkrajšo pot od start_vertex do vseh ostalih.
        Vrne najmanjšo ceno od start_vertex do end_vertex, 
        zraven pa skonstruira še našo pot potovanja.
        Output je oblike (<cena sprehoda>, <pot sprehoda>).
        '''
        # Najprej posodobi uteži na povezavah
        self.tocke = self.nastavi_vse_povezave()
        # Definiraj slovarja poti in povezav. 
        # # Namesto slovarja vozlišč sem uporabil seznam povezav, ker v mojem programu objekt povezava drži večjo vlogo in več informacij kot vozlišče.
        slovar_razdalj = {vozlisce: math.inf for vozlisce in self.tocke.keys()}
        slovar_povezav = {vozlisce: [] for vozlisce in self.tocke.keys()}
        najkrajsa_pot_do_vozlisca = {}
        slovar_razdalj[vozlisce_start] = 0
        while slovar_razdalj:
            # Najdi in vrži ven najkrajšo pot.
            trenutno_vozlisce, razdalja_vozlisca = sorted(slovar_razdalj.items(), key=lambda x: x[1])[0]
            najkrajsa_pot_do_vozlisca[trenutno_vozlisce] = slovar_razdalj.pop(trenutno_vozlisce)
            # Sprehodi se po sosednjih povezavah.
            for sosednja_povezava in self.vrni_sosednje_povezave(trenutno_vozlisce):
                sosednje_vozlisce = sosednja_povezava.vozlisce2
                # Če za sosednje vozlišče še nismo našli najkrajše cene in poti
                if sosednje_vozlisce in slovar_razdalj:
                    nova_razdalja_do_vozlisca = razdalja_vozlisca + sosednja_povezava.utez
                    # Če je trenutna pot boljša kot tista, po kateri smo hodili prej, jo posodobi.
                    if slovar_razdalj[sosednje_vozlisce] > nova_razdalja_do_vozlisca:
                        slovar_razdalj[sosednje_vozlisce] = nova_razdalja_do_vozlisca
                        slovar_povezav[sosednje_vozlisce] = slovar_povezav[trenutno_vozlisce] + [sosednja_povezava]

        return najkrajsa_pot_do_vozlisca[vozlisce_end], slovar_povezav[vozlisce_end]

    @staticmethod
    def dobi_pot_iz_povezav(seznam_povezav):
        ''' Iz seznama prepotovanih poti vrne seznam imen prepotovanih vozlišč. Helper funkcija k outputu za funkcijo dikstra '''
        return [seznam_povezav[0].vozlisce1.ime] + [povezava.vozlisce2.ime for povezava in seznam_povezav]


# 2.: Konstrukcija grafa

britof_kr = Vozlisce("BritofKR")
kranj_ap = Vozlisce("KranjAP")
ljubljana_tivoli = Vozlisce("LjubljanaTivoli")
postaja_jadranska = Vozlisce("PostajaJadranska")
fmf = Vozlisce("FMF")
ljubljana_zelezniska = Vozlisce("LjubljanaZelezniska")
kranj_zelezniska = Vozlisce("KranjZelezniska")

graf = Graf()

graf.dodaj_tocke([britof_kr, kranj_ap, ljubljana_tivoli, postaja_jadranska, fmf, ljubljana_zelezniska, kranj_zelezniska])

graf.dodaj_usmerjeno_povezavo(britof_kr, kranj_ap)
graf.dodaj_usmerjeno_povezavo(kranj_ap, britof_kr)

graf.dodaj_usmerjeno_povezavo(kranj_zelezniska, britof_kr)
graf.dodaj_usmerjeno_povezavo(britof_kr, kranj_zelezniska)

graf.dodaj_usmerjeno_povezavo(kranj_ap, ljubljana_tivoli)
graf.dodaj_usmerjeno_povezavo(ljubljana_tivoli, kranj_ap)

graf.dodaj_usmerjeno_povezavo(ljubljana_tivoli, postaja_jadranska)
graf.dodaj_usmerjeno_povezavo(postaja_jadranska, ljubljana_tivoli)

graf.dodaj_neusmerjeno_povezavo(ljubljana_tivoli, fmf, 17)
graf.dodaj_neusmerjeno_povezavo(postaja_jadranska, fmf, 2)
graf.dodaj_neusmerjeno_povezavo(ljubljana_zelezniska, fmf, 20)

graf.dodaj_usmerjeno_povezavo(ljubljana_zelezniska, kranj_zelezniska)
graf.dodaj_usmerjeno_povezavo(postaja_jadranska, ljubljana_zelezniska)