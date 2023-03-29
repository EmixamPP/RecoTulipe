
from source.DataSet import DataSet
import numpy as np

class Whitening :
    """
    Classe pour faire un premier prétraitement des images en mettant en avant les différences
    au sein de chaque images

    """

    def __init__(self, Mat_X):
        """
        Mat_X :  est la matrice X d'un DataSet, qui est du type [#Images, pixel longuer, pixel largeur, #couleur]
        """
        self.epsilon = 0.1 # précision
        self.X = np.asarray(Mat_X,dtype=np.float16)  # du type [#Images, pixel longuer, pixel largeur, #couleur]

        self.constructionNewX()

    def constructionNewX (self):
        """
        fonction qui crée les nouvelles valeurs X
        """
        X_traitement = self.X.reshape(self.X.shape[0], self.nbrValeurDansUneImage())  # dimensionne chaque image en 1 vecteur
        X_traitement = X_traitement / 255  # mettre les valeurs sur la même échelle
        X_traitement = X_traitement  - X_traitement.mean(axis=0)  # centrer les valeur sur 0

        cov = np.cov(X_traitement, rowvar=False) # calcule de la matrice de covariance sur base des pixelles.

        U, S, V = np.linalg.svd(cov)  # U vecteurs propres, S valeur propre

        newX = U.dot(np.diag(1.0 / np.sqrt(S + self.epsilon))).dot(U.T).dot(X_traitement.T).T  # décorellé les données
        # la formule vient de https://www.freecodecamp.org/news/https-medium-com-hadrienj-preprocessing-for-deep-learning-9e2b9c75165c/
        newX = (newX - newX.min()) / (newX.max() - newX.min())   # remettre à la bonne échelle
        self.newX = np.reshape(newX, self.X.shape)
        # redimenssionner X comme initialement prévu [#Images, pixel longuer, pixel largeur, #couleur]

    def nbrValeurDansUneImage (self):
        """
        :return: le nbr de pixel multiplié par la couleur
        """
        nbrPixel = 1
        for i in range(1,len(self.X.shape)):
            nbrPixel *= self.X.shape[i]
        return nbrPixel

    def getNewX (self):
        return self.newX


if __name__ == "__main__":

    #    ds.resize(50,50)
    ds = DataSet("/home/dorian/Documents/BA3/projetDAnnée/RecoTulipe2021/ressource/realData/FlorwerResize100/", "jpg")

    whitening = Whitening(ds.getX())
    ds.setX(whitening.getNewX())
    ds.save("/home/dorian/Documents/BA3/projetDAnnée/RecoTulipe2021/ressource/realData/Resultat3")



