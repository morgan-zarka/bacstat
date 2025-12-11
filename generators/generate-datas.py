import geojson, geopandas
import pandas as pd

def create_popup_html(dpt_name, candidats, admitted, success_rate, year):    
    html = f"""
    <div style="font-family: Arial, sans-serif; width: 300px;">
        <h3 style="color: #2C3E50; margin-bottom: 10px; text-align: center;">{dpt_name}</h3>
        <hr style="border: 1px solid #BDC3C7;">
        
        <div style="margin: 10px 0;">
            <strong>👥 Candidats:</strong> 
            <span style="color: #3498DB; font-weight: bold;">{candidats:,}</span>
        </div>
        
        <div style="margin: 10px 0;">
            <strong>✅ Admis:</strong> 
            <span style="color: #27AE60; font-weight: bold;">{admitted:,}</span>
        </div>
        
        <div style="margin: 10px 0;">
            <strong>📊 Taux de réussite:</strong> 
            <span style="color: #E74C3C; font-weight: bold; font-size: 16px;">{success_rate:.1f}%</span>
        </div>

        <a href="https://data.education.gouv.fr/explore/dataset/fr-en-baccalaureat-par-departement/information/?disjunctive.code_academie&disjunctive.academie&disjunctive.code_departement&disjunctive.departement&sort=session" target="_blank" style="margin-top: 15px; padding: 8px; background-color: #ECF0F1; border-radius: 4px; font-size: 12px; color: #7F8C8D; text-align: center; display: block; text-decoration: none;">
            💡 Données Baccalauréat {year}
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

        display_name = f"{dpt_code} : {dpt['nom']}"

        dpt_code = '620' if dpt_code == '2A' else dpt_code
        dpt_code = '720' if dpt_code == '2B' else dpt_code

        for year in years:
            year_data = bac_results.query("Session == @year and `Code département` == @dpt_code")

            candidats = year_data['Nombre de présents à l\'examen'].sum()
            admitted = year_data['Nombre d\'admis à l\'examen'].sum()
            success_rate = (admitted / candidats * 100) if candidats > 0 else 0.0

            popup_html = create_popup_html(
                display_name,
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

    # écriture dans un fichier
    with open("generated-datas/france-departements-with-datas.geojson", "w") as f:
        geojson.dump(france_with_data, f)


if __name__ == '__main__':
    main()