from graf import Graf, Vozlisce, Povezava

class Model:
    
    def __init__(self):
        self.graf = Graf()
        self.uporabniki = {} # {Key = userID; Value = objekt Uporabnik}
        self.stevec = 0
    
    def dodaj_uporabnika(self):
        ''' V model nam doda novega uporabnika. Novonastalega uporabnika funkcija vrne. '''
        while self.stevec in self.uporabniki.keys(): # Poskrbimo, da bo ID uporabnka enolično določen
            self.stevec += 1
        nov_uporabnik = Uporabnik(self.stevec)
        self.uporabniki[self.stevec] = nov_uporabnik
        return nov_uporabnik


class Uporabnik: 
    
    def __init__(self, id_uporabnika):
        self.id_uporabnika = id_uporabnika
        self.prejsna_iskanja = []
        # TODO: Ugotovi, kakšna podatkovna struktura bi bila najboljša za evidenco prejšnih iskanj.


class Potovanje:
    def __init__(self, kraj_zacetka, kraj_konca, cas_evidence):
        self.kraj_zacetka = kraj_zacetka
        self.kraj_konca = kraj_konca
        self.cas_evidence = cas_evidence
        # TODO: Poišči dober objekt za predstavljanje časa v Pythonu.