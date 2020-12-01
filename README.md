### P2_WebScrapping

Script permettant la récupération d'informations pour chaque livres référencés dans le site https://books.toscrape.com/.

Pour chaque livre, il récuperent : 
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

Le script créera un dossier pour chaque catégorie de livre, contenant un fichier **"categorie".csv** et un dossier **image**.
Dans le fichier **"categorie".cvs**, seront stockées les informations de chaque livre de cette catégorie et le dossier **image** contiendra les images pour chaque livre de cette catégorie, renommées avec le titre du livre.


### Utilisation
Veuillez à bien avoir installer les librairies citées dans le fichier **"requirements.text"**.

Exemple : ``` pip install Beautifullsoup```

Pour utiliser le programme, soit double-cliquer dessus, soit dan l'invite de commande taper : ``` poython P2_
