import bottle
from datetime import date
from model import *

IME_DATOTEKE = "podatki_grafov"
moj_model = Model.iz_datoteke(IME_DATOTEKE)

def nalozi_uporabnikovo_stanje():
    uporabnisko_ime = "Tjaž Eržen" # TODO: Razvij funkcionalnost, da moj ime ne bo hardcodan v program
    if uporabnisko_ime:
        try:
            uporabnik = Uporabnik.iz_datoteke(uporabnisko_ime)
        except FileNotFoundError:
            print("Datoteke s takim imenom nisem našel.")
            uporabnik = Uporabnik("Uporabnik brez imena")
        return uporabnik
    else:
        bottle.redirect("/prijava/")

def shrani_uporabnika(uporabnik: Uporabnik):
    uporabnik.v_datoteko()

