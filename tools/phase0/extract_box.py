import zipfile, csv, io, os, sys
PORTS = {"lalb": (33.40,33.85,-118.60,-118.00), "houston": (29.20,29.85,-95.35,-94.55)}
z, date = sys.argv[1], sys.argv[2]
zf = zipfile.ZipFile(z)
member = [n for n in zf.namelist() if n.lower().endswith(".csv")][0]
files, writers, counts = {}, {}, {p:0 for p in PORTS}
for p in PORTS: files[p] = open(f"{p}_{date}.csv","w",newline="",encoding="utf-8")
with zf.open(member) as raw:
    rdr = csv.reader(io.TextIOWrapper(raw, encoding="utf-8", errors="replace", newline=""))
    header = next(rdr)
    for p in PORTS:
        writers[p] = csv.writer(files[p]); writers[p].writerow(header)
    ilat, ilon = header.index("LAT"), header.index("LON")
    for row in rdr:
        try: la=float(row[ilat]); lo=float(row[ilon])
        except (ValueError, IndexError): continue
        for p,(a,b,c,d) in PORTS.items():
            if a<=la<=b and c<=lo<=d:
                writers[p].writerow(row); counts[p]+=1; break
for f in files.values(): f.close()
print("  kept: " + "  ".join(f"{p}={n:,}" for p,n in counts.items()), flush=True)
