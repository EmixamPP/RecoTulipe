# Keras pour classifier des images

## Installations des libs
En toute honnêteté, je ne suis pas sur que ça va marcher.

Pour installer pip et le mettre à jour:
```
sudo apt install python3-pip
pip3 install --upgrade pip
```


Installation des librairies:

```
pip3 install --user tensorflow-cpu --use-feature=2020-resolver
pip3 install keras
```

La commande devrait installer toutes les dépendences qui ne sont pas encore satifaites. Il est également possible d'utiliser la version gpu de tensorflow. Cependant, je n'ai pas réussi (en plus j'ai pas de gpu sur mon portable donc...).

Je ne garantie en aucun cas la réussite de cette installation. En cas de problème, vous pouvez vous référer à internet.

## Premier pas

Dans le fichier [firstStep.py](firstStep.py), il y a un simple modèle pour reconnaître les chiffres. Cet exemple est basé sur les tutos par défaut disponibles.

Avec cette solution, il est facile d'atteindre une efficacité avoisinant les 99%.

## Plus loin et plus fort avec le transfer learning

Il existe des modèles de réseaux de neurones pré-entraînés qui permettent de diminuer le nombre d'entraînements nécessaires pour atteindre une bonne efficacité. Les tests avec ces réseaux pré-entraînés sont dans le fichier [preTrained.py](preTrained.py). Basé sur [ce tutoriel](https://machinelearningmastery.com/how-to-use-transfer-learning-when-developing-convolutional-neural-network-models/).

Les résultats obtenus sont intéressant. En utilisant le modèle pré-entraîné [ResNet50](https://keras.io/api/applications/resnet/#resnet50-function) et en modifiant ces entrées et sa couche de sortie (le modèle initial est classer 1000 classes d'images), on obtient une efficacité de 50% en utilisant seulement 100 images. En comparaison, en utilisant un nouveau modèle (celui de [preTrained.py](preTrained.py) par exemple) avec le même nombre d'image d'entraînements, on obtient une efficacité de 23%. 
