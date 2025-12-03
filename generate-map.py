import folium

def main():      
    coords = (46.539758, 2.430331)
    map = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=6)
    popup = folium.GeoJsonPopup(fields=["displayed_name"], aliases=[""])

    sf = lambda x :{'fillColor':"#28B463", 'fillOpacity':0.5, 'color':'#E84000', 'weight':1, 'opacity':1}

    folium.GeoJson(
      data="generated-datas/france-departements-with-datas.geojson",
      name="france",
      style_function= sf,
      popup=popup,
      popup_keep_highlighted=True,
    ).add_to(map)


    map.save(outfile='map.html')
    return None

if __name__ == '__main__':
    main()