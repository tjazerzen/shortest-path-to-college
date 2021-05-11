from graf import Povezava
from graf import graf as g2
from graf import ljubljana_tivoli, fmf, britof_kr, postaja_jadranska

# Izpis grafa
print(g2, "\n")

print(Povezava.dobi_minute_iz_casa(), "\n")

cena, pot_povezav = g2.dijkstra(britof_kr, fmf)
print(cena, g2.dobi_pot_iz_povezav(pot_povezav))