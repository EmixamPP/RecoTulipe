from mnist import MNIST

from netwok import *

mndata = MNIST('./data/')
# images: liste des images. 1 image=une liste de tous ces pixels
images, labels = mndata.load_training()

datas = []
for i in range(len(images)):
    im=np.array(images[i])[:,np.newaxis]
    im = im.astype(np.float)
    im /= 255

    expected = np.zeros((10,1))
    expected[int(labels[i])]=1

    datas.append((im,expected))

random.shuffle(datas)


print("Transformation done")
print(len(datas))

couches = [784, 16, 16, 10]
learning_rate = 1

name=""

for c in couches:
    name += str(c)+"_"
name += "lr_"+str(learning_rate)+".pickle"
name = "./IA/"+name
print(name)

octavius = Network()
octavius.initNetwork(couches)
#octavius.load("./IA/newHope.pickle")

try:
    octavius.train(
        datas = datas[200:],
        batch_size=30,
        epochs=3,
        initial_learning_rate=learning_rate,
        training_set=datas[:200])
    octavius.save(name)
except KeyboardInterrupt:
    octavius.save("save.pickle")
