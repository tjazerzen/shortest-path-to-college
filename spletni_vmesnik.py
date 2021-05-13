import bottle

@bottle.get("/")
def osnova_stran():
    if "ime_racuna" in bottle.request.query:
        print(bottle.request.query["ime_racuna"])

    return bottle.template(
        "osnovna_stran.html", 
        nerazporejeno = -1, 
        racuni = [i for i in range(10)]
        )

@bottle.get("/dodaj-racun/")
def dodaj_racun():
    print(bottle.request.query.getunicode("ime_racuna"))
    bottle.redirect("/uspesno-dodajanje-racuna/")
    

@bottle.get("/uspesno-dodajanje-racuna/")
def uspesno_dodajanje_racuna():
    return "Uspešno si dodal račun"

@bottle.get("/pozdravi/<ime>/")
def pozdravi(ime):
    return f"Živjo, {ime}!"

bottle.run(reloader=True, debug=True) 