# Version Beta Web-scrapping Books Online

Script permettant la récupération d'informations pour chaque livres référencés dans le site https://books.toscrape.com/.

Pour chaque livre, il récupere : 
- url du livre,
- son code UPC,
- son titre,
- son prix TTC,
- son prix HT,
- le nombre d'exemplaire disponible,
- la description du livre,
- la catégorie du livre,
- le classement de ce livre,
- et l'url de l'image de la page du livre.

Le script créera un dossier pour chaque catégorie de livre, contenant un fichier **categorie.csv** et un dossier **images**.
Dans le fichier **categorie.cvs**, seront stockées les informations de chaque livre de cette catégorie et le dossier **images** contiendra les images pour chaque livre de cette catégorie, renommées avec le titre du livre.


## Utilisation du programme

### Récupération du code
  Deux options : 
   - Cloner le repository par le biais de git en entrant la commande suivante :
   ```bash 
   git clone https://github.com/libgit2/libgit2
   ```
   - Télécharger le code pour le biais de l'onglet **code** situé plus haut de la page et décompresser l'archive
   
Placer vous dans le dossier OC_P2_WebScrapping-main

### Installation environnement virtuel

Ouvrir un invite de commande et lancer la commande suivante :
```bash 
python -m venv env
```
Cela crée le dossier env contenant une copie de l'interpréteur Python, de la bibliothèque standard et quelques autres fichiers utiles.

### Activation de l'environnement virtuel

Sur Windows, lancez :
```bash
env\Scripts\activate.bat
```

Sur Unix et MacOS, lancez :
```bash
env/bin/activate
```
### Installation des modules requis

Pour installer les librairies requises, entrer dans l'invite de commande : 
```bash
pip install -r requirements.txt
```
### Utilisation  du programme

Pour utiliser le programme, soit double-cliquer dessus, soit dans l'invite de commande taper : 

```bash
python main.py
```

