import bottle
from datetime import date
from model import Model, Uporabnik, Vozlisce

IME_DATOTEKE = "podatki_grafov"
moj_model = Model.iz_datoteke(IME_DATOTEKE)

def nalozi_uporabnikovo_stanje():
    uporabnisko_ime = "Tjaž Eržen"
    if uporabnisko_ime:
        try:
            uporabnik = Uporabnik.iz_datoteke(uporabnisko_ime)
        except FileNotFoundError:
            print("Datoteke s takim imenom nisem našel.")