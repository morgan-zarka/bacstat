import geojson, geopandas
import pandas as pd
import plotly.express as px
import plotly.io as pio
import os

def create_popup_html(dpt_name, dpt_number, candidats, admitted, success_rate, year, m_rate, f_rate):
    df_mini = pd.DataFrame({
        "Genre": ["H", "F"],
        "Taux": [m_rate, f_rate],
        "Couleur": ["#3030ED", "#910059"]
    })

    fig = px.bar(df_mini, x="Genre", y="Taux", color="Genre",
        color_discrete_map={"H": "#3030ED", "F": "#910059"})

    fig.update_layout(
        width=180, height=200,
        paper_bgcolor='#000091', plot_bgcolor='#000091',
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        yaxis=dict(visible=False, range=[0, 110]),
        xaxis=dict(tickfont=dict(color='white', size=14), title=None)
    )
    fig.update_traces(texttemplate='%{y:.1f}%', textposition='outside', textfont=dict(color='white'))

    graph_html = pio.to_html(fig, full_html=False, include_plotlyjs='cdn', config={'displayModeBar': False})

    html = f"""
    <div style="font-family: 'marianne', sans-serif; width: 480px; background-color: #000091; border-radius: 10px; color: #FFFFFF; padding: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            
            <div style="width: 240px; border-right: 1px solid rgba(255,255,255,0.3); padding-right: 15px;">
                <p style="margin: 0;">Département {dpt_number}</p>
                <h3 style="margin-bottom: 15px; font-size: 1.5rem; margin-top: 5px;">{dpt_name}</h3>
                
                <h4 style="font-size: 1.5rem; margin-bottom: 0; margin-top: 10px;">Chiffres</h4>
                <ul style="margin-left: -20px; margin-top: 5px; font-size: 1.15rem; line-height: 1.5;">
                    <li>{candidats:,} candidats</li>
                    <li>{admitted:,} admis</li>
                    <li>{success_rate:.1f}% de réussite</li>
                </ul>
            </div>

            <div style="width: 200px; display: flex; flex-direction: column; align-items: center; margin-left: 10px;">
                <div style="width: 100%;">
                    {graph_html}
                </div>
                
                <div style="width: 100%; margin-top: 10px; font-size: 0.9rem;">
                    <div style="display: flex; align-items: center; margin-bottom: 5px;">
                        <div style="width: 15px; height: 15px; background-color: #3030ED; margin-right: 10px; border: 1px solid white;"></div>
                        <span>Hommes ({m_rate:.1f}%)</span>
                    </div>
                    <div style="display: flex; align-items: center;">
                        <div style="width: 15px; height: 15px; background-color: #910059; margin-right: 10px; border: 1px solid white;"></div>
                        <span>Femmes ({f_rate:.1f}%)</span>
                    </div>
                </div>
            </div>
        </div>

        <a href="https://data.education.gouv.fr/explore/dataset/fr-en-baccalaureat-par-departement/information/?disjunctive.code_academie&disjunctive.academie&disjunctive.code_departement&disjunctive.departement&sort=session" target="_blank" style="margin-top: 20px; padding: 8px; background-color: #ECF0F1; border-radius: 4px; font-size: 12px; color: #000091; display: block; text-decoration: none; text-align: center;">
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

            candidats = year_data["Nombre de présents à l'examen"].sum()
            admitted = year_data["Nombre d'admis à l'examen"].sum()
            success_rate = (admitted / candidats * 100) if candidats > 0 else 0.0

            m_data = year_data[year_data['Genre'] == 'Masculin']
            m_pres = m_data["Nombre de présents à l'examen"].sum()
            m_rate = (m_data["Nombre d'admis à l'examen"].sum() / m_pres * 100) if m_pres > 0 else 0

            f_data = year_data[year_data['Genre'] == 'Féminin']
            f_pres = f_data["Nombre de présents à l'examen"].sum()
            f_rate = (f_data["Nombre d'admis à l'examen"].sum() / f_pres * 100) if f_pres > 0 else 0

            popup_html = create_popup_html(
                dpt['nom'],
                dpt_code,
                int(candidats),
                int(admitted),
                float(success_rate),
                year,
                m_rate,
                f_rate
            )
            dpt[f'popup_html_{year}'] = popup_html

        l.append(dpt)

    france_with_data = geopandas.GeoDataFrame(l)
    france_with_data.crs = france.crs

    os.makedirs("generated-datas", exist_ok=True)

    # écriture dans un fichier
    with open("generated-datas/france-departements-with-datas.geojson", "w") as f:
        geojson.dump(france_with_data, f)

if __name__ == '__main__':
    main()