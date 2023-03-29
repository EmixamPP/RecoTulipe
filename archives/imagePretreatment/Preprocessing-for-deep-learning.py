

import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.datasets import cifar10


def plotImage(X):
    plt.figure(figsize=(1.5, 1.5))
    plt.imshow(X.reshape(32,32,3))
    plt.show()
    plt.close()

def afficher_cheval():

	(X_train, y_train), (X_test, y_test) = cifar10.load_data()

	X_train.shape
	X = X_train[:1000]
	X = X.reshape(X.shape[0], X.shape[1]*X.shape[2]*X.shape[3])

	plotImage(X[12, :])


def calculateCovariance(X):

    meanX = np.mean(X, axis = 0)
    lenX = X.shape[0]
    X = X - meanX
    covariance = X.T.dot(X)/lenX

    return covariance

def center(X):

    newX = X - np.mean(X, axis = 0)

    return newX

def standardize(X):

    newX = center(X)/np.std(X, axis = 0)

    return newX

def decorrelate(X):

    newX = center(X)
    cov = X.T.dot(X)/float(X.shape[0])
    # Calculate the eigenvalues and eigenvectors of the covariance matrix
    eigVals, eigVecs = np.linalg.eig(cov)
    # Apply the eigenvectors to X
    decorrelated = X.dot(eigVecs)

    return decorrelated

def whiten(X):

    newX = center(X)
    cov = X.T.dot(X)/float(X.shape[0])
    # Calculate the eigenvalues and eigenvectors of the covariance matrix
    eigVals, eigVecs = np.linalg.eig(cov)
    # Apply the eigenvectors to X
    decorrelated = X.dot(eigVecs)
    # Rescale the decorrelated data
    whitened = decorrelated / np.sqrt(eigVals + 1e-5)

    return whitened


def plotImage(X):

    plt.figure(figsize=(1.5, 1.5))
    plt.imshow(X.reshape(32,32,3))
    plt.show()
    plt.close()

def white_horse():

	(X_train, y_train), (X_test, y_test) = cifar10.load_data()

	X = X_train[:1000]
	X = X.reshape(X.shape[0], X.shape[1]*X.shape[2]*X.shape[3])

	X_norm = X / 255
	X_norm = X_norm - X_norm.mean(axis=0)


	cov = np.cov(X_norm, rowvar=False)
	U,S,V = np.linalg.svd(cov)

	epsilon = 0.1
	X_ZCA = U.dot(np.diag(1.0/np.sqrt(S + epsilon))).dot(U.T).dot(X_norm.T).T
	X_ZCA_rescaled = (X_ZCA - X_ZCA.min()) / (X_ZCA.max() - X_ZCA.min())
	plotImage(X[12, :])
	plotImage(X_ZCA_rescaled[12, :])

white_horse()