import folium

def main():    
    years = [2023, 2024]

    coords = (46.539758, 2.430331)
    map = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=6)
    sf = lambda x :{'fillColor':"#28B463", 'fillOpacity':0.5, 'color':'#E84000', 'weight':1, 'opacity':1}

    for year in years:

      popup = folium.GeoJsonPopup(fields=["displayed_name", f"candidats_{year}", f"admitted_{year}", f"successRate_{year}"], aliases=["", "Nombre de candidats", "Nombre d'admis", "Taux de réussite (%)"], max_width=300)

      folium.GeoJson(
        data="generated-datas/france-departements-with-datas.geojson",
        name="france",
        style_function= sf,
        popup=popup,
        popup_keep_highlighted=True,
      ).add_to(map)


      map.save(outfile=f'maps/{year}.html')

    return None

if __name__ == '__main__':
    main()