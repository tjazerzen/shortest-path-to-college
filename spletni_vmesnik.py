import bottle
from datetime import date
from model import Model, Uporabnik, Vozlisce

IME_DATOTEKE = "podatki_grafov"
moj_model = Model.iz_datoteke(IME_DATOTEKE)



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
