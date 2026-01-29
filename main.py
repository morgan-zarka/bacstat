from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
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
                    dcc.Graph(id='gender-comparison-bar-chart', style={'height': '500px'}),
                ],
                style={'flex': '1'}
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
                                    html.Span(id='male-pass-rate', style={'fontSize': '4rem', 'fontWeight': '800', 'lineHeight': '1'}),
                                    html.Br(),
                                    html.Span(" des hommes", style={'fontSize': '1.5rem', 'fontWeight': '400'})
                                ],
                                style={'color': '#000091'}
                            ),
                            html.Li(
                                children=[
                                    html.Span(id='female-pass-rate', style={'fontSize': '4rem', 'fontWeight': '800', 'lineHeight': '1'}),
                                    html.Br(),
                                    html.Span(" des femmes", style={'fontSize': '1.5rem', 'fontWeight': '400'})
                                ],
                                style={'color': '#910059'}
                            ),
                        ],
                        style={'listStyleType': 'none', 'display': 'flex', 'gap': '40px', 'padding': '0'}
                    ),
                    html.P(
                        "ont obtenu leur Bac. La tendance reste similaire à travers les années. Nous constatons une légère supériorité des femmes dans les taux de réussite.",
                        style={'fontSize': '1.2rem', 'marginTop': '20px'}
                    )
                ],
                style={'flex': '1'}
            )
        ],
        style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'padding': '80px 100px', 'gap': '60px'}
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
    [Output('map-iframe', 'src'), Output('map-description', 'children'), Output('comparison-description', 'children'), Output('male-pass-rate', 'children'), Output('female-pass-rate', 'children'), Output('gender-comparison-bar-chart', 'figure')],
    Input('dropdown-selection', 'value')
)
def update_map(selected_year):
    map_description = f"Voici une carte des départements de France, avec les résultats du Bac pour l'année {selected_year}."
    comparison_description = f"Comparaison globale des taux de réussite nationaux entre femmes et hommes en {selected_year}."
    
    year_data = data[data['Session'] == selected_year]

    male_data = year_data[year_data['Genre'] == 'Masculin']
    m_pres = male_data['Nombre de présents à l\'examen'].sum()
    m_adm = male_data['Nombre d\'admis à l\'examen'].sum()
    male_pass_rate = (m_adm / m_pres * 100) if m_pres > 0 else 0

    female_data = year_data[year_data['Genre'] == 'Féminin']
    f_pres = female_data['Nombre de présents à l\'examen'].sum()
    f_adm = female_data['Nombre d\'admis à l\'examen'].sum()
    female_pass_rate = (f_adm / f_pres * 100) if f_pres > 0 else 0

    summary_df = pd.DataFrame({
        "Genre": ["Masculin", "Féminin"],
        "Taux de réussite": [male_pass_rate, female_pass_rate]
    })

    fig = px.bar(
        summary_df, 
        x="Genre", 
        y="Taux de réussite", 
        color="Genre",
        text_auto='.1f',
        color_discrete_map={'Masculin': '#000091', 'Féminin': '#910059'},
        title=f"Taux de réussite national en {selected_year}"
    )

    fig.update_layout(
        showlegend=False, 
        yaxis_range=[0, 105],
        margin=dict(l=20, r=20, t=40, b=20)
    )
    fig.update_traces(textfont_size=18, textposition='outside')

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