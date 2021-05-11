import bottle

@bottle.get("/")
def osnova_stran():
    return bottle.template("osnovna_stran.html")


bottle.run(reloader=True) 