
# `Najkrajša-Do-Faksa`

Vse poti vodijo do faksa! :D

Bolj natančno, do postaje na Jadranski, toda vprašajmo se: 
- Kako še vseeno najhitreje priti od domače avtobusne postaje do iskanega avtobusnega postajališča? 
- Se do našega cilja sploh da priti z direktno povezavo kam hočemo? 
- Če se da, koliko časa bi potreboval in katera bi bila optimalna pot? 

Pričujoči projekt odgovarja na zgoraj zastavljena vprašanja ter vse to zapakira v lepo spletno storitev.

## `Back End`

Jasno je, da neki množici cestnih povezav ter postajališč lahko priredimo vozlišča ter obtežene povezave, le-tem pa priredimo obtežen `graf`. Zato je za iskanje najkrajše poti od enega postajališča dobra ideja shraniti podatke v obliki nekega grafa (datoteka podatki `grafov.json`), katerega uteži pa niso nujno neodvisne od časa iskanja po grafu.

Naloga tega projekta je najti optimalno pot med dvema vozliščema v grafu z več komponentami s postajališčem FMF kot edinim skupnim med temi vsemi. 

Po nekaterih povezavah se lahko sprehajamo oz. vozimo s kolesom, spet po drugih pa se vozimo z avtobusom. Zato svoje `povezave delim na 2 dela`: 

1. `Povezave, ki jim utež variira s časom` (v datoteki podatki_grafov so te shranjene z vrednostjo uteži -1). Ko bomo iskali najcenejšo pot, bo vsakič znova iz tekstovnih datotek (shranjenih v mapi PodatkiOdhodov) treba izračunati trenutno utež te povezave.
2. `Povezave s fiksno utežjo`, neodvisne od časa vpogleda (v datoteki podatki_grafov so shranjene s kakršno koli pozitivno vrednostjo)

V datoteki model.py sem se lotil programiranja objektov, ki v mojem programu nastopajo:
- `Model`: Krovni objekt, ki moj program povezuje. Sestavljen je iz posameznih grafov (voznih linij),
- `Vozlišče`, ki nam predstavlja postajališče,
- `Povezava`, ki povezuje dve vozlišči ter nam predstavlja neko povezavo med njima
- `Graf`, ki povezuje vozlišča in povezave,
- `Uporabnik`, ki je zadolžen za beleženje uporabnikovih prejšnih iskanj in njegovih (njenih) "priljubljenih relacij",
- `Iskanje`: Vsebuje podatke kraju odhoda ter prihoda, datumu iskanja, ceni optimalnega sprehoda, najcenejši poti v temu grafu (če iskani vozlišči ležita v isti komponenti. V spletni storitvi jih imenujem "linije").

## `Front End`

Za popestritev uporabniške izkušnje sem nato vsako vozlišče opremil s parametrom `frekvenca iskanj`, ki sem ga uporabil za `prikaz uporabnikovih najbolj priljubljenih vozlišč` (vozlišče je priljubljeno, če ga je že velikokrat obiskal). Isto sem naredil za vse uporabnike hkrati, nato pa rezultata primerjal pod sekcijo `najkrajsa-voznja/analiza-postajališč/`.

V front-endu sem poskrbel za `spletno storitev, ki podpira več uporabnikov`. Vsak uporabnik do svojega računa dostopa preko uporabniškega imena in gesla. Naj omenim še, da so vsi zgoraj omenjeni objekti opremljeni z metodami za shranjevanje in branje podatkov. Zato lahko uporabnik program zapre, se naslednji dan vrne ter še vedno vidi svoja prejšna iskanja. Tukaj mi je ogromno časa prihranila pythonova knjižnica bottle.py. User experience sem olepšal s HTML datotekami ter Bulminovem frameworku CSS datotek.

K uporabiku sem dodal spremenljivko imenovano `številke linij`, ki nam hrani informacije o posameznikov priljubljenih relacijah. Plan je bil, da posameznik lahko išče le po teh linijah, toda sem pri implementaciji na žalost izgubil tekmo s časom.

Naj omenim še, da program poženete tako, da poženete datoteko `spletni_vmesnik.py.`

## `Nadaljne raziskovanje`

Grafovski algoritmi se (na žalost) še ne obravnajo v 1. letniku, če pa koga zanima pa bi ga preusmeril na:
- [Algoritmska biblija](https://edutechlearners.com/download/Introduction_to_algorithms-3rd%20Edition.pdf)
- [Članek o algoritmu Dijskstra, ki je v tem programu tudi implementiran](https://www.programiz.com/dsa/dijkstra-algorithm)
- [Posnetek o Dijstrovem algoritmu](https://www.youtube.com/watch?v=GazC3A4OQTE)
- Kontakt za vprašanja o tem projektu: erzen.tjaz@gmail.com

## `Avtor`

Tjaž Eržen, študent 1. letnika finančne matematike.
