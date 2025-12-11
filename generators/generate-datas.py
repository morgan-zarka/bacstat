import geojson, geopandas
import pandas as pd

# lecture du fichier global
france = geopandas.read_file("datas/france-departements.geojson", encoding='utf-8')
bac_results = pd.read_csv("datas/bac-results.csv", encoding='utf-8', delimiter=';')
years = bac_results['Session'].unique()

bac_results['Code département'] = bac_results['Code département'].astype(str).str.zfill(2)

l = []

for idx, dpt in france.iterrows():
    dpt_code = dpt['code']

    dpt['displayed_name'] = f"{dpt_code} : {dpt['nom']}"

    dpt_code = '620' if dpt_code == '2A' else dpt_code
    dpt_code = '720' if dpt_code == '2B' else dpt_code

    for year in years:
        year_data = bac_results.query("Session == @year and `Code département` == @dpt_code")

        candidats = year_data['Nombre de présents à l\'examen'].sum()
        admitted = year_data['Nombre d\'admis à l\'examen'].sum()
        success_rate = (admitted / candidats * 100) if candidats > 0 else 0.0

        dpt[f'candidats_{year}'] = int(candidats)
        dpt[f'admitted_{year}'] = int(admitted)
        dpt[f'successRate_{year}'] = float(success_rate)

    l.append(dpt)

# construction de la GeoDataFrame correspondante
france_with_data = geopandas.GeoDataFrame(l)
france_with_data.crs = france.crs

# écriture dans un fichier
with open("generated-datas/france-departements-with-datas.geojson", "w") as f:
    geojson.dump(france_with_data, f)