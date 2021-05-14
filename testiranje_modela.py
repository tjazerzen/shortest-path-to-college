from model import Model
from graf1 import graf1 as g1

moj_model = Model.iz_datoteke()

for graf in moj_model.grafi:
    print(graf)