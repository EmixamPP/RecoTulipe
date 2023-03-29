# np.random.seed(456)
# np.random.seed(456)
import pickle
import random

import numpy as np


class Network:
    def __init__(self):
        self.w = []  # w[i] -> matrice des poids entre la couche i et i+1 -> w[i][j][k] = poid du lien entre le j ème neurone de la caouche  i+1 et le k ème neurone de la couche i
        self.b = []
        self.n_couche = 0

        self.average_accuracy = 0
        self.learning_rate = 0
        self.initial_learning_rate = 0


    def initNetwork(self, listSize):
        #listSize= liste des tailles des différentes couches
        self.n_couche=len(listSize)
        self.w = []#w[i] -> matrice des poids entre la couche i et i+1 -> w[i][j][k] = poid du lien entre le j ème neurone de la caouche  i+1 et le k ème neurone de la couche i
        self.b = []
        ecart_type=1/(listSize[0]**0.5)
        for i in range(len(listSize)):
            if i<len(listSize)-1:
                #self.b.append(np.random.normal(0, ecart_type, (listSize[i+1],1))) #5x3
                self.b.append(np.random.randn(listSize[i+1],1)) #5x3
                #self.w.append(np.random.normal(0, ecart_type, (listSize[i+1],listSize[i])))
                self.w.append(np.random.randn(listSize[i+1],listSize[i]))

    def forwardPassForBackpropagation(self, input):
        """
        forwardPass qui sauvegarde toutes les données z et a pour chaque couche pour un input donné
        return a,z
        a = liste de vecteur tel que a[i] est le vecteur des neurones de la couche i
        z = liste de vecteur tel que a[i] est le vecteur des z de la couche i-1
        """
        z = []
        a = [input]
        for i in range(1,self.n_couche):
            z.append(np.dot(self.w[i-1], a[i-1])+self.b[i-1])
            a.append(self.activation(z[-1]))
        return a,z

    def forwardPass(self, input):
        """
        renvoie et calcul la dernière couche du réseau de neurone pour un input donné
        """
        a = input
        for i in range(1,self.n_couche):
            a = self.activation(np.dot(self.w[i-1], a)+self.b[i-1])
        return a

    def activation(self,x):
        #return (np.exp(x)-np.exp(-x))/((np.exp(x)+np.exp(-x)))
        #return np.maximum(0,x)#fonction ReLu
        return 1/(1 + np.exp(-x))

    def d_activation(self,x):
        #return 4/(np.exp(x)+np.exp(-x))**2
        #return (x>0).astype(int)
        return np.exp(-x)/(1+np.exp(-x))**2

    def load(self, filename):
        with open(filename, 'rb') as f:
            self.w, self.b = pickle.load(f)
            self.n_couche=len(self.b)+1

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump([self.w, self.b], f)

    def train(self, datas, batch_size, epochs=0, initial_learning_rate=1, decrease_rate=0 , training_set=None):
        """
        entraine le réseau

        datas: liste de tuple de 2 vecteur colonne
            le premier est la première chouche du réseau de neurone
            le deuxième est dernière couche souhaitée
        batch_size: taille d'un batch d'entrainement
        learning_rate: learning rate
        decrease_rate: valeur entre 0-1. Plus il est proche de 1, plus le learning_rate aura tendence à diminuer facilement
        training_set: même forme que datas, le réseau testera son efficacité sur le training_set après chaque batch d'entrainement
            None pour ne pas tester l'efficacité
        """
        self.initial_learning_rate=initial_learning_rate
        self.learning_rate=initial_learning_rate
        self.average_accuracy=0

        for j in range(epochs):
            self.epoch_accuracy=0
            random.shuffle(datas)
            for i in range(0,len(datas),batch_size):
                k = min(len(datas),i+batch_size)
                self.trainBatch(datas[i:k], decrease_rate)

            if training_set != None:
                accuracy = self.testAccuracy(training_set)
                percent = round(accuracy*100,2)
                print("epoch: "+str(j+1)+ " --> "+ str(percent)+"%")

            #mise à jour de la moyenne de la précision du réseau
            self.epoch_accuracy /= len(datas)
            self.average_accuracy = (1-decrease_rate)*self.average_accuracy + decrease_rate * self.epoch_accuracy
            if self.average_accuracy==0:
                self.average_accuracy=self.epoch_accuracy
            if self.epoch_accuracy < self.average_accuracy:
                self.learning_rate /= 2
                #self.learning_rate -= (self.average_accuracy-batch_accuracy)*self.learning_rate
                print("Reduce learning rate to", self.learning_rate)
                self.average_accuracy=0

    def trainBatch(self, batch, decrease_rate):
        """
        entraine un batch de donnée
        batch: sous liste de datas
        """

        delta_w = [np.zeros(np.shape(self.w[i])) for i in range(len(self.w))]#delta_w[i][j][k] -> dérivée partielle de la fonction cout par rapport au poid entre le neurone j de la couche i+1 et le neurone k de la couche i
        #delta_w2 = [np.zeros(np.shape(self.w[i])) for i in range(len(self.w))]#delta_w[i][j][k] -> dérivée partielle de la fonction cout par rapport au poid entre le neurone j de la couche i+1 et le neurone k de la couche i
        delta_b = [np.zeros(np.shape(self.b[i])) for i in range(len(self.b))]#delta_b[i][j] -> dérivée partielle de la fonction cout par rapport au biai du j ème neurone de la couche i
        #delta_b2 = [np.zeros(np.shape(self.b[i])) for i in range(len(self.b))]#delta_b[i][j] -> dérivée partielle de la fonction cout par rapport au biai du j ème neurone de la couche i

        for data in batch:
            a, z = self.forwardPassForBackpropagation(data[0])
            temp_d_w, temp_d_b = self.backpropagation(a , z, data[1])
            for i in range(len(self.w)):
                delta_w[i] += temp_d_w[i]

            for i in range(len(self.b)):
                delta_b[i] += temp_d_b[i]

            #mise à jour de la moyenne de la précision du réseau sur le batch
            n_attendu = np.unravel_index(data[1].argmax(), data[1].shape)[0]#indice du neurone avec la valeur maximale
            n_detect = np.unravel_index(a[-1].argmax(), a[-1].shape)[0]#indice du neurone avec la valeur maximale
            self.epoch_accuracy += int(n_attendu==n_detect)

        #mise à jour des poids et biais
        for i in range(len(self.w)):
            self.w[i] -= self.learning_rate*delta_w[i]/len(batch)
        for i in range(len(self.b)):
            self.b[i] -= self.learning_rate*delta_b[i]/len(batch)

    def backpropagation(self, a, z, wantedRes):
        """
        renvoie les matrices des dérivées pour un entrainement précisé
        """
        #vecteur colonne wantedRes -> résultat attendu
        d_w = [[] for i in range(len(self.w))]
        d_b = [[] for i in range(len(self.b))]

        d_a = 2*(a[-1]-wantedRes) #vecteur des dérivés de la fct cout par rapport aux neurones de la couche i

        for i in range(len(self.w)-1,-1,-1): #parcourt couches de poids dans l'ordre décroissant
            d_b[i]=d_a
            #calcul des dérivées partielle de la fonction cost en fonction des poid entre les couches i et i+1
            n = len(self.w[i])
            m = len(self.w[i][0])

            c = np.array([np.transpose(a[i])[0]]*n) # ligne a[i] dupliquée n fois
            d = np.transpose([self.d_activation(z[i]),])[0]# f'(z[i]) en vecteur colonne
            e = np.transpose([d_a,])[0] # d_a en vecteur colonne
            d_w[i] = c * d * e #tel que d_w[i][j][k] = a[i][k] * f'(z[i][j]) * d_a[i][j]

            d_a = np.dot(np.transpose(self.w[i]), self.d_activation(z[i])*d_a)

        return d_w, d_b

    def testAccuracy(self, datas):
        """
        methode qui test la précision du réseau de neurone
        datas: liste de tuple de 2 vecteur colonne
        return l'efficacité du réseau entre 0 et 1
        """
        n_reussite = 0
        for data in datas:
            n_attendu = np.unravel_index(data[1].argmax(), data[1].shape)[0]#indice du neurone avec la valeur maximale
            a=self.forwardPass(data[0])
            n_detect = np.unravel_index(a.argmax(), a.shape)[0]#indice du neurone avec la valeur maximale
            if(n_attendu == n_detect):
                n_reussite+=1

        return float(n_reussite)/float(len(datas))
