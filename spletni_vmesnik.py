import bottle
from datetime import date
from model import Model, Uporabnik, Vozlisce

IME_DATOTEKE = "podatki_grafov"
moj_model = Model.iz_datoteke(IME_DATOTEKE)

