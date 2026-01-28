from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import os

data = pd.read_csv('./datas/bac-results.csv', encoding='utf-8', delimiter=';')

app = Dash(__name__, title="BacStat - Analyse des résultats du Baccalauréat")

app.layout = [
    html.Header(
        children=[
            html.Img(
                src='/assets/img/logo.png',
                style={'height': '40px'}
            ),
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
                    ),
                    dcc.Graph(id='gender-comparison-bar-chart'),
                ]
            ),
            html.Div(
                children=[
                    html.P(
                        id='comparison-description',
                    ),
                    html.P(
                        "Cette année :"
                    ),
                    html.Ul(
                        children=[
                            html.Li(
                                children=[
                                    html.Span(id='male-pass-rate', style={'fontSize': '3rem', 'fontWeight': '800', 'lineHeight': '1'}),
                                    html.Br(),
                                    html.Span(" des hommes", style={'fontSize': '1.5rem', 'fontWeight': '400'})
                                ],
                                style={'color': '#000091'}
                            ),
                            html.Li(
                                children=[
                                    html.Span(id='female-pass-rate', style={'fontSize': '3rem', 'fontWeight': '800', 'lineHeight': '1'}),
                                    html.Br(),
                                    html.Span(" des femmes", style={'fontSize': '1.5rem', 'fontWeight': '400'})
                                ],
                                style={'color': '#910059'}
                            ),
                        ],
                        style={'listStyleType': 'none', 'display': 'flex', 'gap': '20px'}
                    ),
                    html.P(
                        "ont obtenu leur Bac. La tendance reste similaire à travers les années. Nous constatons une légère supériorité des femmes dans les taux de réussite.",
                    )
                ],
            )
        ],
        style={'display': 'flex', 'justifyContent': 'space-between', 'padding': '40px 100px', 'marginTop': '40px'}
    ),
    html.Div(
        children=[
            html.Img(
                src='/assets/img/logo.png',
                style={'height': '40px'}
            ),
            html.H2(
                children='Mentions légales',
                style={'fontWeight': '800', 'fontSize':'1.5rem'}
            ),
            html.P(children=[
                "©Morgan ZARKA & Ines TEMMAR",
                html.Br(),
                html.Br(),
                "Ce site à été créé et édité par Morgan ZARKA (morgan.zarka@edu.esiee.fr) et Ines TEMMAR (ines.temmar@edu.esiee.fr) dans le cadre d'un projet scolaire au sein de ESIEE Paris.",
                html.Br(),
                html.Br(),
                "Voici les différentes sources utilisées pour la création de ce site :",
                html.Ul(children=[
                    html.Li(children=[html.A("Résultats du Baccalauréat par département - data.education.gouv.fr", href="https://data.education.gouv.fr/explore/dataset/fr-en-baccalaureat-par-departement"), "- ", html.A("Licence etalab-2.0", href="https://github.com/etalab/licence-ouverte/blob/master/LO.md")]),
                    html.Li(children=[html.A("Tracés des départements de France - Grégoire David", href="https://github.com/gregoiredavid/france-geojson/blob/master/departements-avec-outre-mer.geojson"), "- ", html.A("Licence ouverte", href="https://alliance.numerique.gouv.fr/")]),
                ]),
                "Le présent site ne traitant aucune données personnalisés, le RGPD ne s'applique pas."
            ])
        ],
        className='footer',
    ),
]

@callback(
    [Output('map-iframe', 'src'), Output('map-description', 'children'), Output('comparison-description', 'children'), Output('male-pass-rate', 'children'), Output('female-pass-rate', 'children')],
    Output('gender-comparison-bar-chart', 'figure'),Input('dropdown-selection', 'value')
)
def update_map(selected_year):
    map_description = f"Voici une carte des départements de France, avec les résultats du Bac pour l'année {selected_year}. En cliquant sur un département, vous pouvez voir les taux de réussite et les différences entre femmes et hommes."
    comparison_description = f"Cet histogramme permet de comparer les taux de réussite des femmes et des hommes au Bac en {selected_year}."
    
    year_data = data[data['Session'] == selected_year]

    fig = px.bar(
        year_data, 
        x="Département", 
        y="Taux de réussite à l'examen", 
        color="Genre", 
        barmode="group",
        color_discrete_map={'Masculin': '#000091', 'Féminin': '#910059'}, # On garde tes couleurs
        title="Taux de réussite par département et par genre"
    )

    male_data = year_data[year_data['Genre'] == 'Masculin']
    male_total_present = male_data['Nombre de présents à l\'examen'].sum()
    male_total_admis = male_data['Nombre d\'admis à l\'examen'].sum()
    male_pass_rate = (male_total_admis / male_total_present) * 100 if male_total_present > 0 else 0

    female_data = year_data[year_data['Genre'] == 'Féminin']
    female_total_present = female_data['Nombre de présents à l\'examen'].sum()
    female_total_admis = female_data['Nombre d\'admis à l\'examen'].sum()
    female_pass_rate = (female_total_admis / female_total_present) * 100 if female_total_present > 0 else 0

    return f'/assets/maps/{selected_year}.html', map_description, comparison_description, f"{male_pass_rate:.1f}%", f"{female_pass_rate:.1f}%", fig

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