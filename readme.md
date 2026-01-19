# Projet BacStat - Morgan ZARKA & Ines TEMMAR

## User guide

Pour exécuter l'application BacStat localement, suivez les étapes ci-dessous :
1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/morgan-zarka/bacstat.git
   cd bacstat
   ```

2. **Installer les dépendances** :
   Assurez-vous d'avoir Python installé, puis installez les dépendances requises :
   ```bash
   pip install -r requirements.txt
   ```

   ou avec conda :
   ```bash
    conda install --file requirements.txt
    ```

3. **Générez les données et les cartes** :
   Exécutez les scripts de génération pour préparer les données et les cartes :
   ```bash
    python generate-all.py
   ```

   Cette commande exécutera les scripts `generate-datas.py` et `generate-maps.py` pour créer les fichiers nécessaires à l'application.
   Vous pouvez également exécuter ces scripts individuellement si nécessaire :
   ```bash
    python generators/generate-datas.py
    python generators/generate-maps.py
   ```

4. **Lancer l'application** :
   Démarrez l'application Dash :
   ```bash
   python app.py
   ```

5. **Accéder à l'application** :
   Ouvrez votre navigateur web et allez à l'adresse suivante :
   ```bash
   http://127.0.0.1:8050
   ```

## Data sources
Les données utilisées dans ce projet proviennent de sources publiques, fiables et pour lesquelles les droits d'utilisation sont respectés :
- Résultats du Baccalauréat par département - [data.education.gouv.fr](https://data.education.gouv.fr/explore/dataset/fr-en-baccalaureat-par-departement) - [Licence etalab-2.0](https://github.com/etalab/licence-ouverte/blob/master/LO.md)
<br>Ces données sont fournies par le Ministère de l'Éducation nationale et de la Jeunesse et sont mises à disposition sous licence etalab-2.0.

- Tracés des départements de France - [Grégoire David](https://github.com/gregoiredavid/france-geojson/blob/master/departements-avec-outre-mer.geojson) - [Licence ouverte](https://alliance.numerique.gouv.fr/)
<br>Grégoire David a compilé ces données à partir de sources gouvernementales (IGN et INSEE) et les a mises à disposition sous licence ouverte.

## Developer guide
Voici la structure du projet BacStat pour les développeurs souhaitant contribuer ou comprendre le code :

```
bacstat/
├── .gitignore                  # Fichier listant les fichiers et dossiers à ignorer par Git
├── assets/                     # Dossier contenant les ressources statiques (images, styles, cartes)
│   ├── fonts/                      # Dossier des polices personnalisées
│   ├── img/                        # Dossier des images (logos, icônes)
│   ├── maps/                       # Dossier des fichiers HTML des cartes interactives statiques
│   ├── favicon.ico                 # Fichier favicon de l'application
│   └── styles.css                  # Fichier CSS pour le style personnalisé de l'application
├── datas/                      # Dossier contenant les données brutes
│   ├── bac-results.csv             # Fichier CSV des résultats du baccalauréat par département, par année et par sexe
│   └── departements.geojson        # Fichier GeoJSON des départements de France
├── generated-datas/            # Dossier contenant les fichiers de données générés
├── generators/                 # Dossier contenant les scripts de génération de données et de cartes
│   ├── generate-datas.py           # Script pour générer un fichier geojson des départements, en ajoutant les données de résultats du bac
│   └── generate-maps.py            # Script pour générer les fichiers HTML des cartes interactives par année
├── maps/                       # Dossier contenant les fichiers HTML des cartes interactives générées
├── generate-all.py             # Script pour générer les fichiers ayant besoin d'être prégénérés
├── main.py                     # Fichier principal de l'application Dash
├── readme.md                   # Guide d'utilisation et informations sur le projet
└── requirements.txt            # Fichier listant les dépendances Python
```

Le dashboard a été pensé comme un site one-page. Il n'y a donc qu'un seul fichier principal `main.py` qui contient toute la logique de l'application. L'arborescence n'a pas été pensée pour permettre la création de pages supplémentaires.

Les données brutes sont stockées dans le dossier `datas/`. Les scripts de génération dans le dossier `generators/` permettent de créer les fichiers nécessaires à l'application, qui sont ensuite stockés dans les dossiers `generated-datas/` et `maps/`.

Les informations présentes dans les popups des cartes interactives sont générées au sein du fichier `generate-datas.py`, qui inclue le code HTML de ces popups.

Lors de l'execution de main.py, une copie statique des cartes interactives est générée dans le dossier `assets/maps/` pour être utilisée dans l'application Dash.

## Rapport d'analyse
Une fois le projet finalisé, nous avons utilisé notre application pour analyser les résultats du baccalauréat en France métropolitaine et dans les départements d'outre-mer. Voici un résumé des principales observations :
1. **Taux de réussite global** :
   - Le taux de réussite au baccalauréat a montré une tendance à la hausse au fil des années, avec des variations selon les départements.
2. **Disparités des genres** :
   - Les femmes ont généralement un taux de réussite plus élevé que les hommes, avec des écarts plus prononcés dans certains départements.
3. **Variations régionales** :
   - Certains départements, notamment ceux des zones urbaines, ont bien plus de participants comparés aux départements ruraux.

## Copyright
Nous déclarons sur l’honneur que le code fourni a été produit par nous même (Morgan ZARKA et Ines TEMMAR), à l’exception du fichier generate-all.py qui a été en grande partie générée à l'aide de l’outil GitHub Copilot.

Cet outil a d'ailleurs été utilisé pour débugger certaines parties du code au sein de l'intégralité du projet. Cependant, nous avons veillé à comprendre et à valider chaque ligne de code produite par cet outil avant de l’intégrer dans notre projet. De plus, nous avons apporté des modifications au code généré pour l’adapter à nos besoins spécifiques.

Github copilot a été utilisé comme un simple assistant de programmation, en mode "Ask", et non comme un outil de génération automatique de code sans intervention humaine (ou d'auto-complétion).

Nous sommes conscients que l’absence ou l’omission de déclaration de source sera considéré comme du plagiat.