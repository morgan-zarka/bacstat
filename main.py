from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import os

data = pd.read_csv('./datas/bac-results.csv', encoding='utf-8', delimiter=';')

app = Dash()

app.layout = [
    html.H1(children='Statistiques Baccalauréat par Département', style={'textAlign':'center'}),
    dcc.Dropdown(
        options=[{'label': str(year), 'value': year} for year in sorted(data['Session'].unique())],
        value=2024, 
        clearable=False,
        id='dropdown-selection',
        style={'width': '300px', 'margin': '20px auto'}
    ),
    html.Iframe(
        id='map-iframe',
        src='/assets/maps/2024.html',
        width='100%',
        height='600px',
        style={
            'border': '1px solid #ddd', 
            'margin-top': '20px',
            'border-radius': '5px'
        }
    )
]

@callback(
    Output('map-iframe', 'src'),
    Input('dropdown-selection', 'value')
)
def update_map(selected_year):
    return f'/assets/maps/{selected_year}.html'

if __name__ == '__main__':
    assets_maps_dir = 'assets/maps'
    if not os.path.exists(assets_maps_dir):
        os.makedirs(assets_maps_dir)
        import shutil
        for file in os.listdir('maps/'):
            if file.endswith('.html'):
                shutil.copy(f'maps/{file}', f'{assets_maps_dir}/{file}')
    
    app.run(debug=True)