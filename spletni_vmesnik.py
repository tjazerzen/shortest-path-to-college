from datetime import date
import bottle
from model import *

IME_DATOTEKE = "podatki_grafov.json"
try:
    moj_model = Model.iz_datoteke(ime_datoteke=IME_DATOTEKE)
except FileNotFoundError:
    moj_model = Model()

PISKOTEK_UPORABNISKO_IME = "uporabnisko_ime"
SKRIVNOST = "to je ena skrivnost"  # To naj bi bilo vsem uporabnikom skrito


def shrani_stanje(uporabnik):
    uporabnik.v_datoteko()


def trenutni_uporabnik():
    print("preusmerjen na funkcijo trenutni uporabnik")
    uporabnisko_ime = bottle.request.get_cookie(PISKOTEK_UPORABNISKO_IME, secret=SKRIVNOST)
    if uporabnisko_ime:
        # print("Piškotek sem si zapomnil")
        return podatki_uporabnika(uporabnisko_ime)
    else:
        #print("Piškotka si nisem zapomnil.")
        bottle.redirect("/prijava/")


def podatki_uporabnika(uporabnisko_ime):
    #print("preusmerjen na funkcijo podatki uporabnika")
    try:
        return Uporabnik.iz_datoteke(uporabnisko_ime)
    except FileNotFoundError:
        return bottle.redirect("/prijava/")


@bottle.get("/")
def zacetna_stran():
    #print("Sem na začetni strani")
    bottle.redirect("/najkrajsa_voznja/")


@bottle.get("/prijava/")
def prijava_get():
    #print("Preusmerjen na funkcijo prijava_get()")
    return bottle.template("prijava.html", napaka=None)


@bottle.post("/prijava/")
def prijava_post():
    #print("Preusmerjen na funkcijo prijava_post()")
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo_v_cistopisu = bottle.request.forms.getunicode("geslo")
    if uporabnisko_ime:
        #print("Uporabnisko ime je uspešno sprejeto.")
        try:
            uporabnik = Uporabnik.iz_datoteke(uporabnisko_ime)
        except FileNotFoundError:
            # Take datoteke še ni --> Naredi objekt Uporabnik ter to zapiši v datoteko
            uporabnik = Uporabnik(uporabnisko_ime, zasifriraj_geslo(geslo_v_cistopisu))
            uporabnik.v_datoteko()
        if uporabnik.preveri_geslo(geslo_v_cistopisu):
            #print("Geslo je pravilno")
            bottle.response.set_cookie(
                PISKOTEK_UPORABNISKO_IME, uporabnisko_ime, path="/", secret=SKRIVNOST
            )
            bottle.redirect("/")
        else:
            #print("Geslo ni pravilno")
            return bottle.template(
                "prijava.html", napaka="Podatki za prijavo so napačni!"
            )
    else:
        #print("Uporabnisko ime ni bilo uspešno sprejeto.")
        return bottle.template("prijava.html", napaka="Vnesi uporabniško ime!")


@bottle.post("/odjava/")
def odjava():
    bottle.response.delete_cookie(PISKOTEK_UPORABNISKO_IME, path="/")
    bottle.redirect("/")


@bottle.get("/najkrajsa_voznja/")
def bodoca_osnovna_stran():
    #print("Sem na strani najkrajsa_voznja")
    uporabnik = trenutni_uporabnik()
    return bottle.template(
        "najkrajsa_voznja.html", uporabnik=uporabnik
    )


bottle.run(debug=True, reloader=True)
