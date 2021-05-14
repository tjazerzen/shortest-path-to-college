import bottle
from datetime import date
from model import Model, Uporabnik, Vozlisce

IME_DATOTEKE = "podatki_grafov"
moj_model = Model.iz_datoteke(IME_DATOTEKE)

def nalozi_uporabnikovo_stanje():
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime")
    if uporabnisko_ime:
        try:
            uporabnik = Uporabnik.preberi_iz_datoteke(uporabnisko_ime)
        except FileNotFoundError:
            uporabnik = Uporabnik(ime="Brez imena")
        return uporabnik
    else:
        bottle.redirect("/prijava/")

def shrani_uporabnikovo_stanje(stanje):
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime")
    stanje.shrani_v_datoteko(uporabnisko_ime)

@bottle.get("/")
def osnovna_stran():
    return bottle.template(
        "osnovna_stran.html",
        stevilo_grafov=len(moj_model.grafi) + 4,
        indeks=6
    )


@bottle.get("/uspesno-dodajanje/")
def uspesno_dodajanje():
    return "Uspešno si dodXXXal"


bottle.run(reloader=True, debug=True)
