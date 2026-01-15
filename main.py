from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import os

data = pd.read_csv('./datas/bac-results.csv', encoding='utf-8', delimiter=';')

app = Dash(__name__)

app.layout = [
    html.Header(
        children=[
            html.H1(children='Statistiques Baccalauréat par Département', style={'textAlign':'center'}),
            dcc.Dropdown(
                options=[{'label': str(year), 'value': year} for year in sorted(data['Session'].unique())],
                value=2024, 
                clearable=False,
                id='dropdown-selection',
                style={'width': '75px', 'margin': '20px auto'}
            )
        ]
    ),
    html.Div(
        children=[
            html.Div(
                children=[
                    html.H1(
                        children=[
                            html.Span(
                                children="Femmes",
                                style={'color': '#910059'}
                            ),
                            " ou ",
                            html.Span(
                                children="hommes",
                                style={'color': '#000091'}
                            ),
                            " : qui domine le Bac ?"
                        ],
                        style={'fontWeight': '800', 'fontSize':'3.25rem'}
                    ),
                    html.P("Dans cette analyse, nous avons exploré les données publiques du ministère pour comparer la réussite au Bac au sein des départements, et entre les hommes et les femmes."),
                    html.A(
                        children="Voir plus",
                        href="#departments-map-title",
                        style={'display': 'inline-block', 'backgroundColor': '#000091', 'color': 'white', 'padding': '10px 25px', 'borderRadius': '50px', 'textDecoration': 'none', 'fontSize': '1.15rem', 'marginTop': '25px'}
                    )
                ],
                style={'padding': '75px', 'maxWidth': '700px', 'margin': '0', 'marginTop': '250px', 'marginRight': 'auto'}
            ),
            html.Img(
                src='/assets/img/hero_img.jpg',
                style={'width': '500px', 'height': '100vh', 'display': 'block', 'margin': '0', 'objectFit': 'cover', 'objectPosition': '85% center'}
            )
        ],
        style={'display': 'flex', 'justifyContent': 'center'}
    ),
    html.Div(
        children=[
            html.H2(
                children=['Carte par ',html.Span(
                    children='département', style={'color': '#000091'}
                )],
                style={'textAlign':'center', 'fontWeight': '800', 'fontSize':'3rem', 'marginBottom': '20px'},
                id='departments-map-title'
            ),
            html.P(
                id='map-description',
                children="",
                style={'margin': '0 auto', 'marginBottom': '25px', 'textAlign': 'center'}
            ),
            html.Iframe(
                id='map-iframe',
                src='/assets/maps/2024.html',
                width='80%',
                height='600px',
            )
        ],
        style={'padding': '60px 130px'}
    ),
    html.Div(
        children=[
            html.Div(
                children=[
                    html.P(
                        children='Hommes/femmes',
                        style={'fontSize': '0.85rem', 'color': '#000091', 'margin': '0'}
                    ),
                    html.H2(
                        children='Comparaison',
                        style={'fontWeight': '800', 'fontSize':'2.5rem', 'marginTop': '0'}
                    )
                ]
            ),
            html.Div(
                children=[
                    html.P(
                        children="",
                        id='comparison-description',
                    ),
                ],
            )
        ],
        style={'display': 'flex', 'justifyContent': 'space-between', 'padding': '40px 100px', 'marginTop': '40px'}
    )
]

@callback(
    [Output('map-iframe', 'src'), Output('map-description', 'children'), Output('comparison-description', 'children')],
    Input('dropdown-selection', 'value')
)
def update_map(selected_year):
    map_description = f"Voici une carte des départements de France, avec les résultats du Bac pour l'année {selected_year}. En cliquant sur un département, vous pouvez voir les taux de réussite et les différences entre filles et garçons."
    comparison_description = f"Cet histogramme permet de comparer les taux de réussite des filles et des garçons au Bac en {selected_year}."
    return f'/assets/maps/{selected_year}.html', map_description, comparison_description

if __name__ == '__main__':
    assets_maps_dir = 'assets/maps'
    if os.path.exists(assets_maps_dir):
        import shutil
        shutil.rmtree(assets_maps_dir)

    os.makedirs(assets_maps_dir)

    import shutil
    for file in os.listdir('maps/'):
        if file.endswith('.html'):
            shutil.copy(f'maps/{file}', f'{assets_maps_dir}/{file}')

    app.run(debug=True)