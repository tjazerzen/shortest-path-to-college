from model import *
from datetime import datetime, date
from dateutil import parser

cas = datetime.now()
print(cas)

cas_iso = date.isoformat(datetime.now())
print(cas_iso)

cas_iz_iso = parser.parse(cas_iso)
print(str(cas_iz_iso).split(" "))


print("bla blaa blaaa".split(" "))