import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.datasets import cifar10


class Preprocessing :
    """
    Classe pour faire un premier prétraitement des images en mettant en avant les différences
    au sein de chaque images

    """

    def __init__(self):
        (self.X_train, self.y_train), (self.X_test, self.y_test) = cifar10.load_data()

        """
        la c'est juste un préprocessing sur les 1000 première image de X_train
        """
        self.X = self.X_train[:1000]
        self.X = self.X.reshape(self.X.shape[0], self.X.shape[1] * self.X.shape[2] * self.X.shape[3])

        X_norm = self.X / 255
        X_norm = X_norm - X_norm.mean(axis=0)
        cov = np.cov(X_norm, rowvar=False)
        U, S, V = np.linalg.svd(cov)
        epsilon = 0.1
        X_ZCA = U.dot(np.diag(1.0 / np.sqrt(S + epsilon))).dot(U.T).dot(X_norm.T).T
        self.X_ZCA_rescaled = (X_ZCA - X_ZCA.min()) / (X_ZCA.max() - X_ZCA.min())

    def plotImage(self, Image):
        plt.figure(figsize=(1.5, 1.5))
        plt.imshow(Image.reshape(32, 32, 3))
        plt.show()
        plt.close()


test = Preprocessing()
test.plotImage(test.X[12, :])
test.plotImage(test.X_ZCA_rescaled[12, :])