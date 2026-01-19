import subprocess
import sys
import os

def run_script(script_path):
    try:
        print(f"Exécution de {script_path}...")
        result = subprocess.run(
            [sys.executable, script_path], 
            capture_output=True, 
            text=True, 
            check=True
        )
        print(f"{script_path} exécuté avec succès")
        if result.stdout:
            print(f"Sortie: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de {script_path}")
        print(f"Code d'erreur: {e.returncode}")
        print(f"Erreur: {e.stderr}")
        return False
    except FileNotFoundError:
        print(f"Fichier non trouvé: {script_path}")
        return False

def main():
    if not os.path.exists("generators"):
        print("Dossier 'generators' non trouvé. Assurez-vous d'être dans le répertoire racine du projet.")
        sys.exit(1)
    
    scripts = [
        "generators/generate-datas.py",
        "generators/generate-maps.py"
    ]
    
    success_count = 0
    
    for script in scripts:
        if os.path.exists(script):
            if run_script(script):
                success_count += 1
        else:
            print(f"Script non trouvé: {script}")
    
    if success_count == len(scripts):
        print("Tous les scripts ont été exécutés avec succès !")
        print("Vous pouvez maintenant lancer l'application avec: python main.py")
    else:
        print(f"{success_count}/{len(scripts)} scripts exécutés avec succès")
        sys.exit(1)

if __name__ == "__main__":
    main()