import folium
import pandas as pd
import branca
import json

def main():    
    with open("generated-datas/france-departements-with-datas.geojson", 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)


    bac_results = pd.read_csv("datas/bac-results.csv", encoding='utf-8', delimiter=';')
    years = bac_results['Session'].unique()

    for year in years:
        coords = (46.539758, 2.430331)
        map = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=6)
        
        sf = lambda x: {'fillColor': "#77A8D6", 'fillOpacity': 0.5, 'color': '#000091', 'weight': 1, 'opacity': 1}


        for feature in geojson_data['features']:
            properties = feature['properties']
            
            popup_html = properties.get(f'popup_html_{year}', '<p>Pas de données</p>')
            
            iframe = branca.element.IFrame(html=popup_html, width=700, height=425)
            popup = folium.Popup(iframe, max_width=700)
            
            folium.GeoJson(
                data=feature,
                style_function=sf,
                popup=popup,
                popup_keep_highlighted=True,
            ).add_to(map)

        map.save(outfile=f'maps/{year}.html')

    return None

if __name__ == '__main__':
    main()