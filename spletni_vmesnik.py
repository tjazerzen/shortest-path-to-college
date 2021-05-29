import bottle
from model import Model, Uporabnik, Graf

PISKOTEK_UPORABNISKO_IME = "uporabnisko_ime"
SKRIVNOST = "to je ena skrivnost"

moj_model = Model.iz_datoteke()


def shrani_stanje(uporabnik):
    uporabnik.v_datoteko()


def trenutni_uporabnik():
    uporabnisko_ime = bottle.request.get_cookie(
        PISKOTEK_UPORABNISKO_IME, secret=SKRIVNOST
    )
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


@bottle.get("/registracija/")
def registracija_get():
    return bottle.template("registracija.html", napaka=None)


@bottle.post("/registracija/")
def registracija_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo_v_cistopisu = bottle.request.forms.getunicode("geslo")
    if not uporabnisko_ime:
        return bottle.template("registracija.html", napaka="Vnesi uporabniško ime!")
    try:
        Uporabnik.registracija(uporabnisko_ime, geslo_v_cistopisu)
        bottle.response.set_cookie(
            PISKOTEK_UPORABNISKO_IME, uporabnisko_ime, path="/", secret=SKRIVNOST
        )
        bottle.redirect("/")
    except ValueError as e:
        return bottle.template(
            "registracija.html", napaka=e.args[0]
        )


@bottle.get("/prijava/")
def prijava_get():
    return bottle.template("prijava.html", napaka=None)


@bottle.post("/prijava/")
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo_v_cistopisu = bottle.request.forms.getunicode("geslo")
    if not uporabnisko_ime:
        return bottle.template("registracija.html", napaka="Vnesi uporabniško ime!")
    try:
        Uporabnik.prijava(uporabnisko_ime, geslo_v_cistopisu)
        bottle.response.set_cookie(
            PISKOTEK_UPORABNISKO_IME, uporabnisko_ime, path="/", secret=SKRIVNOST
        )
        bottle.redirect("/")
    except ValueError as e:
        return bottle.template(
            "prijava.html", napaka=e.args[0]
        )


@bottle.post("/odjava/")
def odjava():
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
    nova_linija = int(bottle.request.forms["priljubljena_linija"])
    uporabnik.dodaj_novo_linijo(nova_linija)
    shrani_stanje(uporabnik)
    bottle.redirect("/")


@bottle.post("/isci/")
def isci():
    uporabnik = trenutni_uporabnik()
    vozlisce1_ime = bottle.request.forms["kraj_zacetka"]
    vozlisce2_ime = bottle.request.forms["kraj_konca"]
    zmagovalno_iskanje = moj_model.dobi_zmagovalno_iskanje(vozlisce1_ime, vozlisce2_ime)

    for povezava in zmagovalno_iskanje.najkrajsa_povezava:
        print(povezava.vozlisce1.ime, povezava.vozlisce2.ime)

    uporabnik.prejsna_iskanja.insert(0, zmagovalno_iskanje)
    shrani_stanje(uporabnik)
    bottle.redirect("/")


@bottle.get("/analiza-postajalisc/")
def analiziraj_postajalisca():
    uporabnik = trenutni_uporabnik()
    popularna_vozlisca_uporabnika, vsota_frekvenc_uporabnika = uporabnik.dobi_popularna_vozlisca_uporabnika()
    popularna_vozlisca_vseh, vsota_frekvenc_vseh = Graf.dobi_popularna_vozlisca_vseh()
    stevilo_prikazov = min(len(popularna_vozlisca_vseh), len(popularna_vozlisca_uporabnika), 5)
    return bottle.template(
        "analiza-postajalisc.html",
        popularna_vozlisca_vseh=popularna_vozlisca_vseh[:stevilo_prikazov],
        popularna_vozlisca_uporabnika=popularna_vozlisca_uporabnika[:stevilo_prikazov],
        stevilo_prikazov=stevilo_prikazov,
        vsota_frekvenc_uporabnika=vsota_frekvenc_uporabnika,
        vsota_frekvenc_vseh=vsota_frekvenc_vseh,
        uporabnik=uporabnik
    )


@bottle.get("/dodatne-informacije/")
def dodatne_informacije():
    uporabnik = trenutni_uporabnik()
    return bottle.template("dodatne-informacije.html")


@bottle.get("/najkrajsa_voznja/isci/<zacetek_iskanja>-<konec_iskanja>/")
def prikazi_podrobnosti(zacetek_iskanja, konec_iskanja):
    uporabnik = trenutni_uporabnik()
    iskanje = uporabnik.najdi_to_iskanje(zacetek_iskanja, konec_iskanja)
    return bottle.template(
        "informacije_iskanja.html",
        zacetek_iskanja=zacetek_iskanja,
        konec_iskanja=konec_iskanja,
        iskanje=iskanje)


bottle.run(debug=True, reloader=True)
