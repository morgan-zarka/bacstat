import geojson, geopandas

# lecture du fichier global
france = geopandas.read_file("datas/france-departements.geojson", encoding='utf-8')

l = []

for idx, dpt in france.iterrows():
    dpt['displayed_name'] = f"{dpt['code']} : {dpt['nom']}"
    l.append(dpt)

# construction de la GeoDataFrame correspondante
france_with_data = geopandas.GeoDataFrame(l)
france_with_data.crs = france.crs

# écriture dans un fichier
with open("generated-datas/france-departements-with-datas.geojson", "w") as f:
    geojson.dump(france_with_data, f)