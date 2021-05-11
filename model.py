from graf import Graf, Vozlisce, Povezava

class Model:
    
    def __init__(self):
        self.graf = Graf()
        self.uporabniki = {}
        self.stevec = 0


class Uporabnik: 
    
    def __init__(self, id_uporabnika):
        self.id_uporabnika = id_uporabnika
        self.prejsna_iskanja = []


class Iskanje:
    def __init__(self, kraj_zacetka, kraj_konca, cas_evidence):
        self.kraj_zacetka = kraj_zacetka
        self.kraj_konca = kraj_konca
        self.cas_evidence = cas_evidence
