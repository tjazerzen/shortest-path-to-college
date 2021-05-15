from datetime import datetime, date
import math
import json
import hashlib


def zasifriraj_geslo(geslo_v_cistopisu):
    h = hashlib.blake2b()
    h.update(geslo_v_cistopisu.encode(encoding="utf-8"))
    return h.hexdigest()


# 1 Model: N tranportnih linij = grafov
# TODO: Ustvari funkcijo, ki se iz modela sprehodi po vseh grafih, znotraj njega po vseh uporabnikih ter potem vrne
#       najbolj popularna iskanja
class Model:
    ''' Krovni objekt, ki povezuje moj program.'''

    def __init__(self, grafi=[]):
        # Pozorni čitalec bo opazil, da se model inicializira z seznamom, razredna spremenljivka pa je slovar.
        self.grafi = {graf.stevilka_linije: graf for graf in grafi}

    def v_slovar(self):
        return {"grafi": [graf.v_slovar() for graf in self.grafi.values()]}

    @staticmethod
    def iz_slovarja(slovar):
        return Model(grafi=[Graf.iz_slovarja(graf) for graf in slovar["grafi"]])

    def v_datoteko(self, ime_datoteke="podatki_grafov.json"):
        ''' Funkcija uporabljena za zapis podatkov graf v datoteko. '''
        with open(ime_datoteke, "w") as datoteka:
            json.dump(self.v_slovar(), datoteka, ensure_ascii=False, indent=4)

    @staticmethod
    def iz_datoteke(ime_datoteke="podatki_grafov.json"):
        ''' Funkcija, uporabljena za branje in konstruiranje grafov iz datoteke. '''
        with open(ime_datoteke, "r") as datoteka:
            slovar = json.load(datoteka)
            return Model.iz_slovarja(slovar)

    def dodaj_nov_graf(self, graf):
        ''' Doda nov graf v seznam self.grafi. Če točko tak graf obstaja, vrne obstoječi graf, sicer pa nov objekt doda v naš seznam self.grafi ter ta objekt vrne.'''
        if graf in self.grafi.values():  # Če točko tak objekt že obstaja, ga vrni
            return graf
        self.grafi[graf.stevilka_linije] = graf  # Sicer, ga dodaj v self.grafi
        return self.grafi[graf.stevilka_linije]  # In ga vrni.


# 1 Graf: V vozlišč
class Vozlisce:
    def __init__(self, ime):
        self.ime = ime

    def __str__(self):
        return self.ime


# 1 Graf: E povezav
class Povezava:
    ''' 
    Konstruira novo usmerjeno povezavo od vozlisce1 do vozlisce2.
    Za ustvarjanje neusmerjene povezave bom ustvaril dva enosmerna objekta. 
    '''

    def __init__(self, vozlisce1: Vozlisce, vozlisce2: Vozlisce, utez=-1):
        # vozlisce1 je zacetek povezave, vozlisce2 je konec povezave.
        self.vozlisce1 = vozlisce1
        self.vozlisce2 = vozlisce2
        if utez == -1:
            self.fiksna_utez = False  # fiksna_utez == False --> Ceno povezave JE treba izračunati vedno znova.
        else:
            self.fiksna_utez = True  # fiksna_utez == True --> Cene povezave NI treba izračunati vedno znova.
        ''' 
        fiksna_utez nam pove, če bo čas potovanja odvisen od časa vpogleda.
        Ta atribut imajo tiste povezave, po katerih se lahko sprehajamo/ vozimo s kolesom.
        če je fiksna_utez = False, bo objekt povezave skonstruiran z specificirano utezjo. Sicer je utež = -1. 
        '''
        self.utez = utez

    def v_slovar(self):
        return {"zacetek_povezave": self.vozlisce1.ime, "konec_povezave": self.vozlisce2.ime, "utez": self.utez}

    def izracunaj_se(self, cas_vpogleda: datetime = datetime.now()):
        ''' 
        Izračuna utež na grafu v odvisnosti od časa. Če je povezava fiksna, bo cena vedno ista.
        Sicer: Pošči čas od cas_vpogleda do naslednjega odhoda avtobusa ter nastavi ceno povezave na <cas do odhoda> + <cas voznje>.
        '''
        if self.fiksna_utez:
            return self

        minute = self.dobi_minute_iz_casa(cas_vpogleda)
        ime_datoteke = self.vozlisce1.ime + "-" + self.vozlisce2.ime + ".txt"  # Vse tekstovne datoteke imajo isto sintakso, vsa vozlišča pa tako ime, da je ime datoteke brez težav skonstruirati
        with open("./PodatkiOdhodov/" + ime_datoteke, "r") as input_file:
            for line in input_file.readlines():
                trenutna_vrsta = [int(data.strip()) for data in line.split()]
                trenutni_odhod, trenutni_prihod = trenutna_vrsta[0], trenutna_vrsta[1]
                if trenutni_odhod > minute:
                    self.utez = trenutni_prihod - minute
                    return self
            # Ura je preveč, da bi peljal še kakšen avtobus. Kar počakat na prvega naslednji dan ;)
            # print(input_file.readlines())
            self.utez = 24 * 60 - minute + 300  # TODO: Tole 300 spremeni na čas odhoda prvega avtobusa ta dan.
            return self

            # TODO: Pazi, da to še vedno deluje pri branju iz datotek

    @staticmethod
    def dobi_minute_iz_casa(datum: datetime = datetime.now()):
        return int(datum.strftime("%H")) * 60 + int(datum.strftime("%M"))

    def __str__(self):
        return f"Začetek povezave: {self.vozlisce1}; Konec povezave: {self.vozlisce2}; Fiksna: {self.fiksna_utez}; utez: {self.utez}"


# 1 Graf: V vozlišč; 1 Graf: E povezav; N grafov: M uporabnikov
# TODO: Ustvari več tekstovnih datotek in več grafov.
class Graf:
    ''' Objekt, ki povezuje objekta Vozlisce in Povezave na eni strani, ter objekt Uporabnik na drugi. '''

    def __init__(self, stevilka_linije, tocke={}, uporabniki={}, ):
        self.tocke = tocke  # {Key: Točka; Value: množica povezav z začetkom v tej točki}
        self.uporabniki = uporabniki  # SLOVAR --> Key: Ime; Value: <Objekt Uporabnik>
        # vsak graf bo imel M uporabnikov. Toda tudi vsak uporabnik se lahko vozi po večih grafih.
        self.stevilka_linije = stevilka_linije

    @staticmethod
    def iz_slovarja(slovar):
        ''' Konstruira graf iz "podslovarja" iz datoteke podatki_grafov.json '''
        tocke = {Vozlisce(ime_vozlisca): set() for ime_vozlisca in slovar["vozlisca"]}
        for povezava_slovar in slovar["povezave"]:
            povezava = Povezava(
                vozlisce1=Graf.vrni_vozlisce_s_tem_imenom(povezava_slovar["zacetek_povezave"], tocke),
                vozlisce2=Graf.vrni_vozlisce_s_tem_imenom(povezava_slovar["konec_povezave"], tocke),
                utez=int(povezava_slovar["utez"])
            )
            tocke[povezava.vozlisce1].add(povezava)
        return Graf(stevilka_linije=int(slovar["stevilka_linije"]), tocke=tocke, uporabniki={})

    def dobi_ime_linije(self):
        return f"Linija{self.stevilka_linije}".upper()
    
    def izpis_linije(self):
        ''' Funkcija, ki nam bo služila v front-endu. Izpiše nam vse povezave v tem grafu'''
        return f"{self.dobi_ime_linije()}: {' - '.join([str(_) for _ in self.tocke.keys()])}"

    def v_slovar(self):
        ''' Funkcija, uporabljena za zapis informacij grafa v slovar. '''
        vse_povezave = []
        for mnozica_povezav in self.tocke.values():
            vse_povezave += list(mnozica_povezav)
        return {
            "stevilka_linije": self.stevilka_linije,
            "vozlisca": [vozlisce.ime for vozlisce in self.tocke.keys()],
            "povezave": [povezava.v_slovar() for povezava in vse_povezave]
        }

    @staticmethod
    def vrni_vozlisce_s_tem_imenom(iskano_ime, slovar):
        ''' 
        Helper metoda k Graf.iz_datoteke().
        Poišče vozliščom z iskanim imenom v našem slovarju.
        Če vozlišča s takim imenom ni, vrne none
         '''
        # Slovar v argumentu funkcije je oblike: Key - <Objekt točka>; Value - nima veze
        for vozlisce in slovar.keys():
            if vozlisce.ime == iskano_ime:
                return vozlisce
        return None

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
        ''' Doda nekaj novih točk v naš graf. Ne vrne ničesar. Definirano zgolj zavoljo lažje konstrukcije grafa. '''
        for tocka in tocke:
            self.dodaj_tocko(tocka)

    def vrni_sosednja_vozlisca(self, tocka):
        ''' vrne vozlišča, ki so tej točki sosednja. Če take točke ni, vrne None. Skliče se že na obstoječo funkcijo vrni_sosednje_povezave '''
        return [sosednja_povezava.vozlisce2 for sosednja_povezava in list(self.vrni_sosednje_povezave(tocka))]

    def vrni_sosednje_povezave(self, tocka):
        ''' Vrne povezave, ki so tej točki sosednje. Če take točke ni, vrne None. '''
        if tocka in self.tocke.keys():
            return self.tocke[tocka]
        return []

    def dodaj_neusmerjeno_povezavo(self, vozlisce1: Vozlisce, vozlisce2: Vozlisce, utez_povezave=-1):
        ''' 
        V graf doda neusmerjeno povezavo med vozliščema 1 in 2. 
        Ta ukaz bo generiral povezave za vožnjo s kolesom in hojo peš, kjer bo cena povezave v obe smeri enaka ter od časa vpogleda neodvisna. 
        Vse neusmerjene povezave bodo imele tudi fiksno ceno potovanja.
        '''
        if vozlisce1 == vozlisce2: return None  # Trivivalen primer; zank ne bomo ustvarjali.
        return self.dodaj_usmerjeno_povezavo(vozlisce1, vozlisce2, utez=utez_povezave), self.dodaj_usmerjeno_povezavo(
            vozlisce2, vozlisce1, utez=utez_povezave)

    def dodaj_usmerjeno_povezavo(self, vozlisce1: Vozlisce, vozlisce2: Vozlisce, utez=-1):
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
        ''' Izpiše nam podatke o našem grafu. Definirano za lažje programersko testiranje. '''
        izpis = f"Ime grafa: " + self.dobi_ime_linije() + "\n"
        for tocka in self.tocke.keys():
            izpis += tocka.ime + ": [" + "; ".join(
                [sosednja_povezava.vozlisce2.ime + ": " + str(sosednja_povezava.utez) for sosednja_povezava in
                 self.tocke[tocka]]) + "]\n"
        return izpis

    def nastavi_vse_povezave(self, cas_vpogleda: datetime = datetime.now()):
        ''' 
        Posodobi vrednosti uteži vseh povezav. 
        Sprehodi se po vseh povezavah ter na vsaki posebi pokliče metodo za nastavitev uteži, definirano na objektu Povezava. 
        '''
        for vozlisce, seznam_povezav in self.tocke.items():
            self.tocke[vozlisce] = {povezava.izracunaj_se(cas_vpogleda) for povezava in seznam_povezav}
        return self.tocke

    def dijkstra(self, vozlisce_start: Vozlisce, vozlisce_end: Vozlisce, cas_iskanja=datetime.now()):
        '''
        Poišče najkrajšo pot od start_vertex do vseh ostalih.
        Vrne nov objekt Iskanje, ki drži informacije o začetnem in končnem vozlišču, casu vpogleda, ceni sprehoda v grafu ter končni poti v grafu.
        '''
        # Najprej posodobi uteži na povezavah
        self.tocke = self.nastavi_vse_povezave(cas_vpogleda=cas_iskanja)
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

        # return najkrajsa_pot_do_vozlisca[vozlisce_end], slovar_povezav[vozlisce_end]
        return Iskanje(
            vozlisce1=vozlisce_start,
            vozlisce2=vozlisce_end,
            cas_vpogleda=cas_iskanja,
            cena_potovanja=najkrajsa_pot_do_vozlisca[vozlisce_end],
            najkrajsa_pot=self.dobi_pot_iz_povezav(slovar_povezav[vozlisce_end])
        )

    @staticmethod
    def dobi_pot_iz_povezav(seznam_povezav):
        ''' Iz seznama prepotovanih poti vrne seznam imen prepotovanih vozlišč. Helper funkcija k outputu za funkcijo dikstra '''
        return [seznam_povezav[0].vozlisce1] + [povezava.vozlisce2 for povezava in seznam_povezav]


# Globalna spremenljivka ki drži informacije o vseh možnih grafih.
global vsi_grafi
vsi_grafi = Model.iz_datoteke("podatki_grafov.json").grafi.values()

global vse_tocke
vse_tocke = []
for graf in vsi_grafi:
    vse_tocke += graf.tocke.keys()


#global vsi_grafi_dict
#vsi_grafi_dict = {graf.stevilka_linije : graf for graf in vsi_grafi}


# 1 Uporabnik: N iskanj
class Uporabnik:

    # TODO: Ugotovi, če res potrebuješ spremenljivki prejsna_iskanja ter stevilke_linij
    def __init__(self, ime, zasifrirano_geslo, prejsna_iskanja=[], stevilke_linij=[]):
        self.ime = ime
        self.prejsna_iskanja = prejsna_iskanja  # Evidenca iskanj. Kronološko urejene. Vsak element je objekt razreda iskanje.
        self.stevilke_linij = stevilke_linij  # Pove nam, po katerih omrežjih se fura uporabnik
        # Pozoren gledalec opazi, da to vsi_grafi niso argument v funkciji inicializacije, temveč globalna spremenljivka 10 vrstic višje
        self.vsi_grafi = vsi_grafi
        self.zasifrirano_geslo = zasifrirano_geslo
        self.vse_tocke = vse_tocke

    def v_slovar(self):
        return {
            "zasifrirano_geslo": self.zasifrirano_geslo,
            "stevilke_linij": self.stevilke_linij,
            "ime": self.ime,
            "prejsna_iskanja": [iskanje.v_slovar() for iskanje in self.prejsna_iskanja]
        }

    def __str__(self):
        return f"Ime: {self.ime}; Prejsna Iskanja: {'  '.join([str(_) for _ in self.prejsna_iskanja])}; Številke Linij: {' '.join([str(_) for _ in self.stevilke_linij])}"

    @staticmethod
    def iz_slovarja(slovar):
        return Uporabnik(
            ime=slovar["ime"],
            zasifrirano_geslo=slovar["zasifrirano_geslo"],
            prejsna_iskanja=[Iskanje.iz_slovarja(prejsno_iskanje) for prejsno_iskanje in slovar["prejsna_iskanja"]],
            stevilke_linij=[int(stevilka_linije) for stevilka_linije in slovar["stevilke_linij"]]
        )

    def v_datoteko(self):
        ''' 
        Uporabnikove podatke shrani v datoteko. 
        Ime datoteke se ne zahteva, saj ima vsak uporabnik rezervirano svojo datoteko pod imenom "<njegovo/njeno ime>.json"
        '''
        with open(Uporabnik.dobi_ime_datoteke(self.ime), "w") as datoteka:
            json.dump(self.v_slovar(), datoteka, ensure_ascii=False, indent=4)

    @staticmethod
    def dobi_ime_datoteke(ime):
        return f"{ime}.json"

    @staticmethod
    def iz_datoteke(ime):
        ''' 
        Uporabnikove podatke prebere iz datoteke. 
        Ime datoteke se ne zahteva, saj ima vsak uporabnik rezervirano svojo datoteko pod imenom "<njegovo/njeno ime>.json"
        '''
        print("Preusmerjen na funkcijo Uporabnik.iz_datoteke()")
        with open(Uporabnik.dobi_ime_datoteke(ime)) as datoteka:
            slovar = json.load(datoteka)
            return Uporabnik.iz_slovarja(slovar)

    def preveri_geslo(self, geslo_v_cistopisu):
        return self.zasifrirano_geslo == zasifriraj_geslo(geslo_v_cistopisu)

    def nastavi_geslo(self, geslo_v_cistopisu):
        self.zasifrirano_geslo = zasifriraj_geslo(geslo_v_cistopisu)

    def dodaj_iskanje(self, start_vozlisce_ime, end_vozlisce_ime, stevilka_linije, cas_vpogleda=datetime.now()):
        ''' 
        Doda nov objekt Iskanje v odvisnosti od zgornjih parametrov.
        Z argumentom stevilka_linije dostopamo do specifičnega grafa, potem pa na tem grafu samo pokličemo algoritem dijkstra s preostalimi parametri.
        Vrne objekt Iskanje
        '''
        graf = self.dodaj_novo_linijo(stevilka_linije)
        if not graf: return  # Če nam zgornja funkcija vrne None --> Če linije s tako številko ni
        start_vozlisce, end_vozlisce = graf.tocka(start_vozlisce_ime), graf.tocka(end_vozlisce_ime)
        return self.prejsna_iskanja.append(graf.dijkstra(start_vozlisce, end_vozlisce, cas_iskanja=cas_vpogleda))

    def dodaj_novo_linijo(self, stevilka_linije):
        ''' 
        Doda novo linijo za uporabnika. Vrne pripadajoči graf s to številko 
        Če se uporabnik po tej liniji že vozi, vrne to linijo (graf).
        Če take številke linije ni, vrne None
        '''
        if stevilka_linije in self.stevilke_linij:  # Če se po tej liniji že vozimo
            return self.vsi_grafi[stevilka_linije]
        if stevilka_linije in self.vsi_grafi.keys():  # Če taka linija obstaja, a se do sedaj po njej še nismo vozili
            self.stevilke_linij.append(stevilka_linije)
            return self.vsi_grafi[stevilka_linije]
        return None  # Sicer, taka linija kar ne obstaja.

    def dobi_grafe_iz_stevilk_linij(self):
        ''' Vrne nam podmnozico slovarja vsi_grafi --> samo tiste, po katerih se naš uporabnik vozi '''
        # Key - številka linije; Value - Objekt graf
        return {graf.stevilka_linije: graf for graf in self.vsi_grafi if graf.stevilka_linije in self.stevilke_linij}
    
    def dobi_svoje_sezname_grafov(self):
        return [graf for graf in self.vsi_grafi if graf.stevilka_linije in self.stevilke_linij]


# 1 Uporabnik: N iskanj
class Iskanje:

    def __init__(self, vozlisce1: Vozlisce, vozlisce2: Vozlisce, cas_vpogleda, cena_potovanja, najkrajsa_pot):
        self.vozlisce1 = vozlisce1  # Od kod potujemo; input = objekt vozlisce
        self.vozlisce2 = vozlisce2  # Kam potujemo; input = objekt vozlisce
        self.cena_potovanja = cena_potovanja  # Cena sprehoda od "zacetek" od "konec" v nasem grafu
        self.cas_vpogleda = cas_vpogleda  # V isoformatu
        self.najkrajsa_pot = najkrajsa_pot  # Seznam objektov vozlisce

    def v_slovar(self):
        return {
            "zacetek": self.vozlisce1.ime,
            "konec": self.vozlisce2.ime,
            "cas_evidence": date.isoformat(self.cas_vpogleda),
            "cena_potovanja": self.cena_potovanja,  # Enota so minute
            "najkrajsa_pot": [vozlisce.ime for vozlisce in self.najkrajsa_pot]
        }

    # TODO: Ugotovi, kako deluje Pythonov ISO format. Primer uporabe imaš pri projektu Kuverte.
    @staticmethod
    def iz_slovarja(slovar):
        return Iskanje(
            vozlisce1=Vozlisce(slovar["zacetek"]),
            vozlisce2=Vozlisce(slovar["konec"]),
            cas_vpogleda=slovar["cas_evidence"],  # TODO: Za tole uporabi ISO format. Ugotovi, zakaj mi zdele ne dela.
            cena_potovanja=int(slovar["cena_potovanja"]),
            najkrajsa_pot=[Vozlisce(ime_vozlisca) for ime_vozlisca in slovar["najkrajsa_pot"]]
        )

    def __str__(self):
        ''' Sprinta nam podatke o uporabniku. Metoda, ki je prisotna zavoljo programerskih potreb. '''
        output1 = f"Začetno vozlišče: {self.vozlisce1.ime}; Končno vozlišče: {self.vozlisce2.ime}; Cas vpogleda {self.cas_vpogleda};"
        output2 = f"Cena sprehoda: {self.cena_potovanja}; Najkrajša pot: {' '.join([vozlisce.ime for vozlisce in self.najkrajsa_pot])}"
        return output1 + output2
