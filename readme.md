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