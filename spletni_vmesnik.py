from datetime import date
import bottle
from model import *


PISKOTEK_UPORABNISKO_IME = "uporabnisko_ime"
SKRIVNOST = "to je ena skrivnost"


def shrani_stanje(uporabnik):
    uporabnik.v_datoteko()


def trenutni_uporabnik():
    uporabnisko_ime = bottle.request.get_cookie(PISKOTEK_UPORABNISKO_IME, secret=SKRIVNOST)
    if uporabnisko_ime:
        return podatki_uporabnika(uporabnisko_ime)
    else:
        bottle.redirect("/prijava/")


def podatki_uporabnika(uporabnisko_ime):
    try:
        return Uporabnik.iz_datoteke(uporabnisko_ime)
    except FileNotFoundError:
        return bottle.redirect("/prijava/")


@bottle.get("/")
def zacetna_stran():
    bottle.redirect("/najkrajsa_voznja/")


@bottle.get("/prijava/")
def prijava_get():
    return bottle.template("prijava.html", napaka=None)


@bottle.post("/prijava/")
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo_v_cistopisu = bottle.request.forms.getunicode("geslo")
    if uporabnisko_ime:
        try:
            uporabnik = Uporabnik.iz_datoteke(uporabnisko_ime)
        except FileNotFoundError:
            uporabnik = Uporabnik(uporabnisko_ime, zasifriraj_geslo(geslo_v_cistopisu))
            shrani_stanje(uporabnik)
        if uporabnik.preveri_geslo(geslo_v_cistopisu):
            bottle.response.set_cookie(
                PISKOTEK_UPORABNISKO_IME, uporabnisko_ime, path="/", secret=SKRIVNOST
            )
            bottle.redirect("/")
        else:
            return bottle.template(
                "prijava.html", napaka="Podatki za prijavo so napačni!"
            )
    else:
        return bottle.template("prijava.html", napaka="Vnesi uporabniško ime!")


@bottle.get("/odjava/")
def prijava_get():
    bottle.response.delete_cookie(PISKOTEK_UPORABNISKO_IME, path="/")
    bottle.redirect("/")

@bottle.get("/najkrajsa_voznja/")
def najkrajsa_voznja():
    uporabnik = trenutni_uporabnik()
    return bottle.template(
        "najkrajsa_voznja.html", uporabnik=uporabnik
    )

@bottle.post("/dodaj-priljubljeno-relacijo/")
def dodaj_priljubljeno_linijo():
    uporabnik = trenutni_uporabnik()
    print(uporabnik)
    nova_linija = int(bottle.request.forms["priljubljena_linija"])
    uporabnik.dodaj_novo_linijo(nova_linija)
    print(uporabnik.stevilke_linij)
    shrani_stanje(uporabnik)
    bottle.redirect("/")


bottle.run(debug=True, reloader=True)
