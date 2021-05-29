from datetime import datetime, date
import math
import json
import hashlib
from dateutil import parser
import random

# Konstanta, uporabljena za izpis, ko ni direktne povezave med dvema vozliščema
RELACIJA_NE_OBSTAJA = "Direktna relacija ne obstaja"


def dobi_vse_grafe():
    """
    Metoda, ki vrne vse grafe, ki so shranjeni v datoteki podatki_grafov.json
    Uporabljena v razredu Uporabnik.
    """
    return Model.iz_datoteke("podatki_grafov.json").grafi


def dobi_vse_tocke(grafi):
    """
    Metoda, ki iz danega slovarja grafi = {Key=stevilka_linije : Value=objekt_graf} vrne vse tocke,
    ki tem grafom pripadajo
    """
    vse_tocke = []
    for graf in grafi.values():
        vse_tocke += graf.tocke.keys()
    return vse_tocke


def dobi_minute_iz_casa(datum: datetime = datetime.now()):
    """ Helper k metodi Povezava.izracunaj_se() """
    return int(datum.strftime("%H")) * 60 + int(datum.strftime("%M"))


# 1 Model: N grafov

class Model:
    """ Krovni objekt, ki povezuje moj program."""

    def __init__(self, grafi=[]):
        self.grafi = {graf.stevilka_linije: graf for graf in grafi}

    def v_slovar(self):
        return {"grafi": [graf.v_slovar() for graf in self.grafi.values()]}

    @staticmethod
    def iz_slovarja(slovar):
        # return Model(grafi=[Graf.iz_slovarja(slovar_grafa) for slovar_grafa in slovar["grafi"]])
        return Model(grafi=[Graf.iz_slovarja(slovar_grafa) for slovar_grafa in slovar["grafi"]])

    def v_datoteko(self, ime_datoteke="podatki_grafov.json"):
        """ Funkcija uporabljena za zapis podatkov graf v datoteko. """
        with open(ime_datoteke, "w") as datoteka:
            json.dump(self.v_slovar(), datoteka, ensure_ascii=False, indent=4)

    @staticmethod
    def iz_datoteke(ime_datoteke="podatki_grafov.json"):
        """ Funkcija, uporabljena za branje in konstruiranje grafov iz datoteke. """
        with open(ime_datoteke, "r") as datoteka:
            slovar = json.load(datoteka)
            return Model.iz_slovarja(slovar)

    def dodaj_nov_graf(self, graf):
        """
        Doda nov graf v seznam self.grafi.
        Če točko tak graf obstaja, vrne obstoječi graf.
        Sicer: Ta nov objekt doda v naš seznam self.grafi ter ta objekt vrne.
        """
        if graf in self.grafi.values():  # Če točko tak objekt že obstaja, ga vrni
            return graf
        self.grafi[graf.stevilka_linije] = graf  # Sicer, ga dodaj v self.grafi
        return self.grafi[graf.stevilka_linije]  # In ga vrni.

    def vrni_grafe(self, vozlisce_ime):
        """
        Vrne nam mnozico grafov, ki vsebujejo ime tega vozlisca.
        Helper metoda k Model.vozlisci_isti_graf()
        """
        return {graf for graf in self.grafi.values() if graf.tocka(vozlisce_ime)}

    def vozlisci_isti_grafQ(self, vozlisce1_ime, vozlisce2_ime):
        """ 
        Vrne nam presek (množico) grafov, ki vsebujejo tako vozlisce pod imenom vozlisce1_ime kot vozlisce2_ime. 
        Uporabljena v metodi dobi_zmagovalno_iskanje(...).
        """
        return self.vrni_grafe(vozlisce1_ime).intersection(self.vrni_grafe(vozlisce2_ime))

    def dobi_zmagovalno_iskanje(self, vozlisce1_ime, vozlisce2_ime):
        """
        Funkcija, ki iz imen dveh vozlišč najprej ugotovi, če obstaja direktna povezava.
        Če ne obstaja, vrne izpis, da taka direktna relacija ne obstaja, kar bo potem prikazano v spletnem vmesniku.
        Sicer pa nam program poišče vse možno direktne povezave od kraja "vozlisce1_ime" do "vozlisce2_ime",
        izračuna vse cene iskanj ter nato vrne najcenejše iskanje. Tega imenujem zmagovalno_iskanje
        """
        skupni_grafi = self.vozlisci_isti_grafQ(vozlisce1_ime, vozlisce2_ime)
        zmagovalno_iskanje = None
        if skupni_grafi != set():
            # Lahko je v tem preseku več grafov. Izmed teh grafov mi iščemo tistega, po katerem je trenutno najcenejša pot.
            for trenuten_graf in skupni_grafi:
                trenutno_iskanje = trenuten_graf.dijkstra(
                    trenuten_graf.tocka(vozlisce1_ime),
                    trenuten_graf.tocka(vozlisce2_ime)
                )
                if not zmagovalno_iskanje:
                    zmagovalno_iskanje = trenutno_iskanje
                else:
                    if trenutno_iskanje.cena_potovanja < zmagovalno_iskanje.cena_potovanja:
                        zmagovalno_iskanje = trenutno_iskanje
        else:
            zmagovalno_iskanje = Iskanje(
                vozlisce1=Vozlisce(vozlisce1_ime),
                vozlisce2=Vozlisce(vozlisce2_ime),
                cas_vpogleda=datetime.now(),
                cena_potovanja=-1,
                najkrajsa_pot=[Vozlisce(RELACIJA_NE_OBSTAJA, frekvenca_obiskov=-1)],
                stevilka_linije=-1
            )
        return zmagovalno_iskanje


# 1 Graf: V vozlišč
class Vozlisce:
    def __init__(self, ime, frekvenca_obiskov=0):
        self.ime = ime
        self.frekvenca_obiskov = frekvenca_obiskov

    def v_slovar(self):
        return {"ime": self.ime, "frekvenca_obiskov": self.frekvenca_obiskov}

    @staticmethod
    def iz_slovarja(slovar):
        return Vozlisce(ime=slovar["ime"], frekvenca_obiskov=int(slovar["frekvenca_obiskov"]))

    def obisk(self):
        """ V algoritmu dijkstra bo metoda poklicana, ko bo vozlišče obiskano. """
        self.frekvenca_obiskov += 1
        return self


# 1 Graf: E povezav
class Povezava:
    """ 
    Konstruira novo usmerjeno povezavo od vozlisce1 do vozlisce2.
    Za ustvarjanje neusmerjene povezave bom ustvaril dva enosmerna objekta. 
    """

    def __init__(self, vozlisce1: Vozlisce, vozlisce2: Vozlisce, utez=-1):
        """
        vozlisce1 je zacetek povezave, vozlisce2 je konec povezave.
        fiksna_utez nam pove, če bo čas potovanja odvisen od časa vpogleda.
        Ta atribut imajo tiste povezave, po katerih se lahko sprehajamo/ vozimo s kolesom.
        če je fiksna_utez = False, bo objekt povezave skonstruiran z specificirano utezjo. Sicer je utež = -1.
        fiksna_utez == False --> Ceno povezave JE treba izračunati vedno znova.
        fiksna_utez == True --> Cene povezave NI treba izračunati vedno znova.
        """
        self.vozlisce1 = vozlisce1
        self.vozlisce2 = vozlisce2
        if utez == -1:
            self.fiksna_utez = False
        else:
            self.fiksna_utez = True
        self.utez = utez

    def v_slovar(self):
        return {"zacetek_povezave": self.vozlisce1.ime, "konec_povezave": self.vozlisce2.ime, "utez": self.utez}

    def izracunaj_se(self, cas_vpogleda: datetime = datetime.now()):
        """ 
        Izračuna utež na grafu v odvisnosti od časa. Če je povezava fiksna, bo cena vedno ista.
        Sicer:  (1): Pošči čas od cas_vpogleda do naslednjega odhoda avtobusa;
                (2): nastavi ceno povezave na <cas do odhoda> + <cas voznje>.
        """
        if self.fiksna_utez:
            return self
        minute = dobi_minute_iz_casa(cas_vpogleda)
        ime_datoteke = self.vozlisce1.ime + "-" + self.vozlisce2.ime + ".txt"
        # Vse tekstovne datoteke imajo isto sintakso, vsa vozlišča pa tako ime, da je ime datoteke brez težav skonstruirati
        with open("./PodatkiOdhodov/" + ime_datoteke, "r") as input_file:
            for line in input_file.readlines():
                trenutna_vrsta = [int(data.strip()) for data in line.split()]
                trenutni_odhod, trenutni_prihod = trenutna_vrsta[0], trenutna_vrsta[1]
                if trenutni_odhod > minute:
                    self.utez = trenutni_prihod - minute
                    return self
            # Ura je preveč, da bi peljal še kakšen avtobus. 
            # Kar počakat na prvega naslednji dan ob 05:00 --> to je 300 min od polnoči
            self.utez = 24 * 60 - minute + 300
            return self  # Vrne sebe, ker bo ta metoda poklicana v objektu Graf.


# 1 Graf: V vozlišč; 1 Graf: E povezav; N grafov: M uporabnikov
class Graf:
    """ Objekt, ki povezuje objekta Vozlisce in Povezave na eni strani, ter objekt Uporabnik na drugi. """

    def __init__(self, stevilka_linije, tocke={}, uporabniki={}, ):
        self.tocke = tocke  # {Key: Točka; Value: množica povezav z začetkom v tej točki}
        # vsak graf bo imel M uporabnikov. Toda tudi vsak uporabnik se lahko vozi po večih grafih.
        self.stevilka_linije = stevilka_linije

    def iz_slovarja_helper_metoda(ime_tocke, slovar):  # slovar: key --> objekt tocka; value --> {...}
        """ Točno to kar pove ime. ;)"""
        for tocka in slovar.keys():
            if tocka.ime == ime_tocke:
                return tocka
        return None

    @staticmethod
    def iz_slovarja(slovar):
        """ Konstruira graf iz "podslovarja" iz datoteke podatki_grafov.json """
        stevilka_linije = int(slovar["stevilka_linije"])
        vozlisca_grafa = [Vozlisce.iz_slovarja(slovar_vozlisca) for slovar_vozlisca in slovar["vozlisca"]]
        tocke = {vozlisce: set() for vozlisce in vozlisca_grafa}
        for slovar_povezave in slovar["povezave"]:
            vozlisce1 = Graf.iz_slovarja_helper_metoda(slovar_povezave["zacetek_povezave"], tocke)
            vozlisce2 = Graf.iz_slovarja_helper_metoda(slovar_povezave["konec_povezave"], tocke)
            utez = int(slovar_povezave["utez"])
            tocke[vozlisce1].add(Povezava(vozlisce1, vozlisce2, utez))
        return Graf(stevilka_linije, tocke=tocke)

    def dobi_ime_linije(self):
        return f"LINIJA{self.stevilka_linije}"

    def izpis_linije(self):
        """ Funkcija, ki nam bo služila v front-endu. Izpiše nam vse povezave v tem grafu"""
        return f"{self.dobi_ime_linije()}: {' - '.join([tocka.ime for tocka in self.tocke.keys()])}"

    def v_slovar(self):
        """ Funkcija, uporabljena za zapis informacij grafa v slovar. """
        vse_povezave = []
        for mnozica_povezav in self.tocke.values():
            vse_povezave += list(mnozica_povezav)
        return {
            "stevilka_linije": self.stevilka_linije,
            "vozlisca": [vozlisce.v_slovar() for vozlisce in self.tocke.keys()],
            "povezave": [povezava.v_slovar() for povezava in vse_povezave]
        }

    def tocka(self, ime):
        """ Vrne točko z danim imenom. Če v grafu takega imena ni, vrne None. """
        for tocka in self.tocke.keys():
            if tocka.ime == ime:
                return tocka
        return None

    def dodaj_tocko(self, tocka):
        """ Doda eno novo točko v naš graf (brez sosedov). Vrne to točko. """
        self.tocke[tocka] = set()
        return tocka

    def vrni_sosednje_povezave(self, tocka):
        """ Vrne povezave, ki so tej točki sosednje. Če take točke ni, vrne None. """
        if tocka in self.tocke.keys():
            return self.tocke[tocka]
        return []

    def dodaj_neusmerjeno_povezavo(self, vozlisce1: Vozlisce, vozlisce2: Vozlisce, utez_povezave=-1):
        """ 
        V graf doda neusmerjeno povezavo med vozliščema 1 in 2. 
        Ta ukaz bo generiral povezave za vožnjo s kolesom in hojo peš,
        kjer bo cena povezave v obe smeri enaka ter od časa vpogleda neodvisna. 
        Vse neusmerjene povezave bodo imele tudi fiksno ceno potovanja.
        """
        if vozlisce1 == vozlisce2: return None  # Trivivalen primer; zank ne bomo ustvarjali.
        return (self.dodaj_usmerjeno_povezavo(vozlisce1, vozlisce2, utez=utez_povezave),
                self.dodaj_usmerjeno_povezavo(vozlisce2, vozlisce1, utez=utez_povezave)
                )

    def dodaj_usmerjeno_povezavo(self, vozlisce1: Vozlisce, vozlisce2: Vozlisce, utez=-1):
        """ 
        V graf doda usmerjeno povezavo od vozlisce1 do vozlisce2.
        Ta ukaz bo generiral povezave za vožnjo s trolo in avtobusom, 
        kjer cena povezave v eno in drugo smer ne bo enaka ter bo odvisna od časa vpogleda.
        Vsakič znova bo treba izračunati ceno povezave z metodo Povezava(...).izracunaj_se().
        Vse usmerjene povezave bodo imeli tudi nefiksno ceno potovanja.
        """
        # Ustvarim nov objekt. Ker se bo utež vedno znova izračunala, je lahko karkoli. 
        # Tukaj jo postavim na -1.
        # Ker utež povezave ni fiksna, je fiksna = False.
        return self.tocke[vozlisce1].add(Povezava(vozlisce1, vozlisce2, utez))

    def nastavi_vse_povezave(self, cas_vpogleda: datetime = datetime.now()):
        """ 
        Posodobi vrednosti uteži vseh povezav. 
        Sprehodi se po vseh povezavah ter
        na vsaki posebi pokliče metodo za nastavitev uteži, definirano na objektu Povezava. 
        """
        for vozlisce, seznam_povezav in self.tocke.items():
            self.tocke[vozlisce] = {povezava.izracunaj_se(cas_vpogleda) for povezava in seznam_povezav}
        return self.tocke

    def dijkstra(self, vozlisce_start: Vozlisce, vozlisce_end: Vozlisce, cas_iskanja=datetime.now()):
        """
        Poišče najkrajšo pot od start_vertex do vseh ostalih. 
        Vrne nov objekt Iskanje, ki drži informacije o začetnem in končnem vozlišču,
        casu vpogleda, ceni sprehoda v grafu ter končni poti v grafu.
        """
        # Najprej posodobi uteži na povezavah
        self.tocke = self.nastavi_vse_povezave(cas_vpogleda=cas_iskanja)
        # Definiraj slovarja poti in povezav. 
        # # Namesto slovarja vozlišč sem uporabil seznam povezav, 
        # ker v mojem programu objekt povezava drži večjo vlogo in več informacij kot vozlišče.
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

        najkrajsa_pot = self.dobi_pot_iz_povezav(slovar_povezav[vozlisce_end])
        Graf.posodobi_frekvenco(najkrajsa_pot)  # Posodobi frekvenco za vse uporabnike
        najkrajsa_pot = [vozlisce.obisk() for vozlisce in najkrajsa_pot]  # Posodobi frekvenco za trenutnega uporabnika
        return Iskanje(
            vozlisce1=vozlisce_start,
            vozlisce2=vozlisce_end,
            cas_vpogleda=cas_iskanja,
            cena_potovanja=najkrajsa_pot_do_vozlisca[vozlisce_end],
            najkrajsa_pot=najkrajsa_pot,
            stevilka_linije=self.stevilka_linije
        )

    @staticmethod
    def dobi_pot_iz_povezav(seznam_povezav):
        """ 
        Iz seznama prepotovanih poti vrne seznam imen prepotovanih vozlišč. 
        Helper funkcija k outputu za funkcijo dikstra 
        """
        return [seznam_povezav[0].vozlisce1] + [povezava.vozlisce2 for povezava in seznam_povezav]

    @staticmethod
    def posodobi_frekvenco(seznam_vozlisc):
        """ 
        Statična metoda, ki nam bo pomagala beležiti frekvenco ustavljanj na nekek postajališču (vozlišču)
        Podatke (zagotovo) preberemo iz frekvenca_obiskov.json ter nato posodobimo frekvenco, kjer je to pač treba
        """
        imena_vozlisc = [vozlisce.ime for vozlisce in seznam_vozlisc]
        IME_DATOTEKE = "frekvenca_obiskov.json"

        with open(IME_DATOTEKE, "r") as datoteka:
            slovar = json.load(datoteka)

        for index, slovar_vozlisca in enumerate(slovar["vse_tocke"]):
            if slovar_vozlisca["ime"] in imena_vozlisc:
                nova_frekvenca = int(slovar_vozlisca["frekvenca_obiskov"]) + 1
                slovar["vse_tocke"][index]["frekvenca_obiskov"] = nova_frekvenca

        with open(IME_DATOTEKE, "w") as datoteka:
            json.dump(slovar, datoteka, ensure_ascii=False, indent=4)

    @staticmethod
    def dobi_popularna_vozlisca_vseh():
        """ 
        Funkcija nam vrne seznam petih najbolj popularnih vozlišč
        po padajočem vrnstnem redu glede na parameter frekvenca obiskov
        """
        IME_DATOTEKE = "frekvenca_obiskov.json"

        with open(IME_DATOTEKE, "r") as datoteka:
            slovar = json.load(datoteka)

        lst = []
        vsota_frekvenc = 0
        for index, slovar_vozlisca in enumerate(slovar["vse_tocke"]):
            vozlisce = Vozlisce.iz_slovarja(slovar_vozlisca)
            frekvenca = vozlisce.frekvenca_obiskov
            lst.append((frekvenca, vozlisce))
            vsota_frekvenc += frekvenca

        return [val2 for (_, val2) in sorted(lst, reverse=True, key=lambda x: x[0]) if
                val2.ime != RELACIJA_NE_OBSTAJA], vsota_frekvenc


# 1 Uporabnik: N iskanj
class Uporabnik:

    def __init__(self, ime, zasifrirano_geslo, prejsna_iskanja=[], stevilke_linij=[]):
        self.ime = ime
        self.prejsna_iskanja = prejsna_iskanja  # Evidenca iskanj. Kronološko urejene. Vsak element je objekt razreda iskanje.
        self.stevilke_linij = stevilke_linij  # Pove nam, po katerih omrežjih se fura uporabnik
        self.zasifrirano_geslo = zasifrirano_geslo
        self.vsi_grafi = dobi_vse_grafe()
        self.vsi_uporabnikovi_grafi = self.dobi_grafe_iz_stevilk_linij()
        self.vse_tocke = dobi_vse_tocke(self.vsi_uporabnikovi_grafi)

    def v_slovar(self):
        return {
            "zasifrirano_geslo": self.zasifrirano_geslo,
            "stevilke_linij": self.stevilke_linij,
            "ime": self.ime,
            "prejsna_iskanja": [iskanje.v_slovar() for iskanje in self.prejsna_iskanja]
        }

    @staticmethod
    def iz_slovarja(slovar):
        return Uporabnik(
            ime=slovar["ime"],
            zasifrirano_geslo=slovar["zasifrirano_geslo"],
            prejsna_iskanja=[Iskanje.iz_slovarja(prejsno_iskanje) for prejsno_iskanje in slovar["prejsna_iskanja"]],
            stevilke_linij=[int(stevilka_linije) for stevilka_linije in slovar["stevilke_linij"]]
        )

    def v_datoteko(self):
        """ Uporabnikove podatke shrani v datoteko. """
        # Ime datoteke se ne zahteva, 
        # saj ima vsak uporabnik rezervirano svojo datoteko pod imenom "<njegovo/njeno ime>.json"

        with open(Uporabnik.dobi_ime_datoteke(self.ime), "w") as datoteka:
            json.dump(self.v_slovar(), datoteka, ensure_ascii=False, indent=4)

    @staticmethod
    def dobi_ime_datoteke(ime):
        return f"{ime}.json"

    @staticmethod
    def iz_datoteke(ime):
        """ Uporabnikove podatke prebere iz datoteke. """
        # Ime datoteke se ne zahteva, 
        # saj ima vsak uporabnik rezervirano svojo datoteko pod imenom "<njegovo/njeno ime>.json"
        try:
            with open(Uporabnik.dobi_ime_datoteke(ime)) as datoteka:
                slovar = json.load(datoteka)
                return Uporabnik.iz_slovarja(slovar)
        except FileNotFoundError:
            return None

    def preveri_geslo(self, geslo_v_cistopisu):
        sol, _ = self.zasifrirano_geslo.split("$")
        return self.zasifrirano_geslo == Uporabnik._zasifriraj_geslo(geslo_v_cistopisu, sol)

    def dodaj_novo_linijo(self, stevilka_linije):
        """ 
        Doda novo linijo za uporabnika. Vrne pripadajoči graf s to številko 
        Če se uporabnik po tej liniji že vozi, vrne to linijo (graf).
        """
        if stevilka_linije in self.stevilke_linij:  # Če se po tej liniji že vozimo
            return self.vsi_uporabnikovi_grafi[
                stevilka_linije]  # Če taka linija obstaja, a se do sedaj po njej še nismo vozili
        self.stevilke_linij.append(stevilka_linije)
        self.vsi_uporabnikovi_grafi[stevilka_linije] = self.vsi_grafi[stevilka_linije]
        return self.vsi_uporabnikovi_grafi[stevilka_linije]

    def dobi_grafe_iz_stevilk_linij(self):
        """ Vrne nam podmnozico slovarja vsi_grafi --> samo tiste, po katerih se naš uporabnik vozi """
        # Key - številka linije; Value - Objekt graf
        return {graf.stevilka_linije: graf for graf in self.vsi_grafi.values() if
                graf.stevilka_linije in self.stevilke_linij}

    def dobi_popularna_vozlisca_uporabnika(self):
        """ """
        with open(Uporabnik.dobi_ime_datoteke(self.ime)) as datoteka:
            slovar = json.load(datoteka)
        prejsna_iskanja = slovar["prejsna_iskanja"]
        lst = []
        slovar_frekvenc = {tocka.ime: 0 for tocka in self.vse_tocke if tocka.ime != RELACIJA_NE_OBSTAJA}
        vsota_frekvenc = 0
        for prejsno_iskanje in prejsna_iskanja:
            najkrajsa_pot = prejsno_iskanje["najkrajsa_pot"]
            for slovar_vozlisca in najkrajsa_pot:
                try:
                    frekvenca = int(slovar_vozlisca["frekvenca_obiskov"])
                    slovar_frekvenc[slovar_vozlisca["ime"]] += frekvenca
                    vsota_frekvenc += frekvenca
                except KeyError:
                    pass

        lst = [(value, Vozlisce(ime=key, frekvenca_obiskov=value)) for key, value in slovar_frekvenc.items()]
        return [val2 for (_, val2) in sorted(lst, reverse=True, key=lambda x: x[0])], vsota_frekvenc

    @staticmethod
    def prijava(uporabnisko_ime, geslo_v_cistopisu):
        uporabnik = Uporabnik.iz_datoteke(uporabnisko_ime)
        if uporabnik is None:
            raise ValueError("Uporabniško ime ne obstaja")
        elif uporabnik.preveri_geslo(geslo_v_cistopisu):
            return uporabnik
        else:
            raise ValueError("Geslo je napačno")

    @staticmethod
    def registracija(uporabnisko_ime, geslo_v_cistopisu):
        if Uporabnik.iz_datoteke(uporabnisko_ime) is not None:
            raise ValueError("Uporabniško ime že obstaja")
        else:
            zasifrirano_geslo = Uporabnik._zasifriraj_geslo(geslo_v_cistopisu)
            uporabnik = Uporabnik(uporabnisko_ime, zasifrirano_geslo)
            uporabnik.v_datoteko()
            return uporabnik

    def _zasifriraj_geslo(geslo_v_cistopisu, sol=None):
        if sol is None:
            sol = str(random.getrandbits(32))
        posoljeno_geslo = sol + geslo_v_cistopisu
        h = hashlib.blake2b()
        h.update(posoljeno_geslo.encode(encoding="utf-8"))
        return f"{sol}${h.hexdigest()}"


# 1 Uporabnik: N iskanj
class Iskanje:

    def __init__(self, vozlisce1: Vozlisce, vozlisce2: Vozlisce, cas_vpogleda, cena_potovanja, najkrajsa_pot,
                 stevilka_linije):
        self.vozlisce1 = vozlisce1  # Od kod potujemo; input = objekt vozlisce
        self.vozlisce2 = vozlisce2  # Kam potujemo; input = objekt vozlisce
        self.cena_potovanja = cena_potovanja  # Cena sprehoda od "zacetek" od "konec" v nasem grafu
        self.cas_vpogleda = cas_vpogleda
        self.najkrajsa_pot = najkrajsa_pot  # Seznam objektov vozlisce
        self.stevilka_linije = stevilka_linije

    def v_slovar(self):
        return {
            "zacetek": self.vozlisce1.v_slovar(),
            "konec": self.vozlisce2.v_slovar(),
            "cas_evidence": date.isoformat(self.cas_vpogleda),
            "cena_potovanja": self.cena_potovanja,  # Enota so minute
            "najkrajsa_pot": [vozlisce.v_slovar() for vozlisce in self.najkrajsa_pot],
            "stevilka_linije": self.stevilka_linije
        }

    @staticmethod
    def iz_slovarja(slovar):
        return Iskanje(
            vozlisce1=Vozlisce.iz_slovarja(slovar["zacetek"]),
            vozlisce2=Vozlisce.iz_slovarja(slovar["konec"]),
            cas_vpogleda=parser.parse(slovar["cas_evidence"]),
            cena_potovanja=int(slovar["cena_potovanja"]),
            najkrajsa_pot=[Vozlisce.iz_slovarja(slovar_vozlisca) for slovar_vozlisca in slovar["najkrajsa_pot"]],
            stevilka_linije=(slovar["stevilka_linije"]
            )
        )
