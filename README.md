Re-upload de projet archivé 2020-2021.

# RecoTulipe2021
Reconnaiscance des plantes via classification supervisée à l'aide du deep learning pour le Printemps des Science 2021 de l'ULB par Maxime Dirksen, Simon Renard, Emma Dupuis, Dorian Cayphas, Guillaume Teboul-Tornezy.

# Librairies Python3.8 nécéssaires
:bangbang: Installer sur un Python3.8 vierge (faites un pyenv si nécéssaire), l'ordre est important :bangbang:
1. tensorflow-cpu (ou tensroflow-gpu)
2. keras
3. scikit-image

# Run le site web et le serveur
Le serveur : `python3.8 source/server.py` 
Commentez la ligne `httpd.socket = ssl.wrap_socket(...)` du fichier pour ne pas utiliser de certificat ssl.
Par défaut le serveur s'éxécute sur le port 8080. Le script accepte en paramètre un port personnalisé, mais n'oubliez pas de le changer dans les deux fichier `upload_image.js` et `click_image.js` du site. Dans ces deux fichiers, pensez à redirer la requête vers l'adresse de votre serveur python (en local ou ailleurs).

Pour le site web : ouvrez le fichier `web/index.html` dans le navigateur de votre choix.
Le git est configurer pour exécuter le site dans un container [Heroku](https://heroku.com).
Ce site a été developé en Boostrap4 à l'aide de [BootstrapStudio](https://bootstrapstudio.io) dont l'archive est disponnible dans le dossier `web`. 

# Data set des images utilisé
* https://www.kaggle.com/msheriey/104-flowers-garden-of-eden
