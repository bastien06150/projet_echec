# Gestionnaire de Tournois d'Échecs

Ce projet est une application en ligne de commande permettant de gérer des tournois d'échecs en suivant l'architecture MVC.  
Les données sont sauvegardées dans des fichiers JSON. L'utilisateur peut créer des joueurs, des tournois, saisir les résultats et générer des rapports.

---

## Fonctionnalités

- Ajout de joueurs avec identifiant unique
- Création de tournois avec tours et matchs
- Génération automatique des paires (pas de rematchs)
- Saisie manuelle des résultats
- Affichage des scores et désignation du gagnant
- Sauvegarde automatique dans des fichiers JSON
- Interface console intuitive

---

## Installation

### Windows

```bash
# Crée un environnement virtuel
python -m venv env

# Active l’environnement virtuel
env\Scripts\activate

# Installe les dépendances
pip install -r requirements.txt
```

# macOS / Linux

```bash

# Crée un environnement virtuel
python3 -m venv env

# Active l’environnement virtuel
source env/bin/activate

# Installe les dépendances
pip install -r requirements.txt
```
