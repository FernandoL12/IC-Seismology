from obspy.clients.fdsn import Client
from obspy import Catalog

C = Client("http://10.110.0.135:18003/")

# Ler IDs
with open("cluster1.txt", "r") as f:
    id_list = f.read().split()

catalog = Catalog()

for evid in id_list:
    try:
        evp = C.get_events(
            eventid=evid,
            includeallorigins=True,
            includearrivals=True,
            includeallmagnitudes=True
        )
        catalog += evp
        print(f"OK: {evid}")

    except Exception as e:
        print(f"Erro em {evid}: {e}")

print(catalog)
catalog.plot(
    projection="local",
    resolution="i",
    show=True
)
