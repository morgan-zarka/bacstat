import geojson, geopandas
import pandas as pd
import os

def create_popup_html(dpt_name, dpt_number, candidats, admitted, success_rate, year):    
    html = f"""
    
    <div style="font-family: Arial, sans-serif; width: 300px; background-color: #000091; border-radius: 10px; color: #FFFFFF; padding: 16px 24px; font-family: sans-serif;">
        <p style="margin: 0;">Département {dpt_number}</p>
        <h3 style="margin-bottom: 15px; font-size: 1.5rem; margin-top: 5px;">{dpt_name}</h3>
        <hr style="border: 1px solid #BDC3C7;">
        
        <h4 style="font-size: 1.5rem; margin-bottom: 0; margin-top: 10px;">Chiffres</h4>
        <ul style="margin-left: -20px; margin-top: 5px; font-size: 1.15rem; line-height: 1.5;">
            <li>{candidats:,} candidats</li>
            <li>{admitted:,} admis</li>
            <li>{success_rate:.1f}% de réussite</li>
        </ul>

        <h4 style="font-size: 1.5rem; margin-bottom: 0; margin-top: 10px;">Légende</h4>

        <div style="display: flex; align-items: center; margin-top: 15px;">
            <div style="width: 50px; height: 20px; background-color: #3030ED; margin-right: 10px; border: 1px solid #FFFFFF;"></div>
            <p style="margin: 0;">Hommes</p>
        </div>

        <div style="display: flex; align-items: center; margin-top: 15px;">
            <div style="width: 50px; height: 20px; background-color: #910059; margin-right: 10px; border: 1px solid #FFFFFF;"></div>
            <p style="margin: 0;">Femmes</p>
        </div>

        <a href="https://data.education.gouv.fr/explore/dataset/fr-en-baccalaureat-par-departement/information/?disjunctive.code_academie&disjunctive.academie&disjunctive.code_departement&disjunctive.departement&sort=session" target="_blank" style="margin-top: 15px; padding: 8px; background-color: #ECF0F1; border-radius: 4px; font-size: 12px; color: #000091; display: block; text-decoration: none; text-align: center;">
            Données Baccalauréat {year}
        </a>
    </div>
    """
    return html

def main():
    france = geopandas.read_file("datas/france-departements.geojson", encoding='utf-8')
    bac_results = pd.read_csv("datas/bac-results.csv", encoding='utf-8', delimiter=';')
    years = bac_results['Session'].unique()

    bac_results['Code département'] = bac_results['Code département'].astype(str).str.zfill(2)

    l = []

    for idx, dpt in france.iterrows():
        dpt_code = dpt['code']

        dpt_code = '620' if dpt_code == '2A' else dpt_code
        dpt_code = '720' if dpt_code == '2B' else dpt_code

        for year in years:
            year_data = bac_results.query("Session == @year and `Code département` == @dpt_code")

            candidats = year_data['Nombre de présents à l\'examen'].sum()
            admitted = year_data['Nombre d\'admis à l\'examen'].sum()
            success_rate = (admitted / candidats * 100) if candidats > 0 else 0.0

            popup_html = create_popup_html(
                dpt['nom'],
                dpt_code,
                int(candidats),
                int(admitted),
                float(success_rate),
                year
            )
            dpt[f'popup_html_{year}'] = popup_html

        l.append(dpt)

    # construction de la GeoDataFrame correspondante
    france_with_data = geopandas.GeoDataFrame(l)
    france_with_data.crs = france.crs

    os.makedirs("generated-datas", exist_ok=True)

    # écriture dans un fichier
    with open("generated-datas/france-departements-with-datas.geojson", "w") as f:
        geojson.dump(france_with_data, f)


if __name__ == '__main__':
    main()