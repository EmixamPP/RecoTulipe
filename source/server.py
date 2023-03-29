import logging
import os
import ssl
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import tempfile

import requests
import termcolor

import NeuralNet

try:
    from ressource.tradFlower import *
except:  # fix un bug étrange avec le Raspberry
    sys.path.insert(1, "./ressource/")
    from tradFlower import *

octaviusComplet = NeuralNet.loadNerualNet("./ressource/savedNetwork/resNetOctavius")
octaviusReduit = NeuralNet.loadNerualNet("./ressource/savedNetwork/resNetOctaviusReduit")
ID = 0
mutex = threading.Lock()

tempDir = tempfile.gettempdir()
count = 0


class HandlerHTTP(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_POST(self):
        global count
        print("Requête numéro {}".format(count))
        count+=1
        try:
            img, networkMode, imgType = self.readBody()

            if imgType == b'local':  # l'image est présente sur le serveur (choisie depuis le site)
                # indice du deuxième "/" en parant de la gauche qui indique le dossier contenant l'image
                i = img.rfind(b"/", 0, img.rfind(b"/"))
                imageName = "./webApp/assets/img" + img[i:].decode('ASCII')

            elif imgType == b'byte':  # img est une suite de byte
                # réservation d'un nom de fichier
                global ID, mutex
                mutex.acquire()
                imageName = os.path.join(tempDir, str(ID) + ".jpeg")
                ID = (ID + 1) % 10000
                mutex.release()

                # créer fichier contenant l'image
                #print(img)
                file = open(imageName, "wb")
                file.write(img)
                file.close()
            else:
                raise Exception("Type de requête inconnu")

            #  prédiction
            image = NeuralNet.Image(imageName, "")

        except:
            res = "Un problème est survenu avec l'image envoyée"

        else:
            if networkMode == b'complet':
                prediction = octaviusComplet.predict(image)
            else:
                prediction = octaviusComplet.predict(image)

            res = tradFlower[prediction[0][0]][0] + " avec une certitude de " + str(
                int(prediction[0][1] * 100)) + "%" + "<br />" + "<a href='" + tradFlower[prediction[0][0]][
                      1] + "' target='_blank' >page Wikipedia ici</a>"
            if prediction[0][1] < 0.71:
                res += "<br />" + "ou une " + prediction[1][0] + " avec une certitude de " + str(
                    int(prediction[1][1] * 100)) + "%" + "<br />" + "<a href='" + tradFlower[prediction[1][0]][
                           1] + "' target='_blank' >page Wikipedia ici</a>"

            #supprime l'image
            if imgType == b'byte' and os.path.exists(imageName):
                os.remove(imageName)
            elif imgType == b'byte':
                print(termcolor.colored("The file " + str(imageName) + " does not exist", "red"))

        self._set_response()
        self.wfile.write(res.encode('utf-8'))

    def readBody(self):
        """
        Extrait les informations du body :return: 3-uple (byte string correspondant à l'image, byte sting du mode
        choisit : performance ou qualité, byte string du type de l'image : url ou image)
        """
        content_length = int(self.headers['Content-Length'])  # longueur du body
        body = []
        length = 0
        while length < content_length:
            line = self.rfile.readline()
            length += len(line)
            body.append(line)

        imgType = body[3][:-2]
        networkMode = body[7][:-2]
        img = b''.join(body[12:-1]) if imgType == b'byte' else body[11][:-2]

        return img, networkMode, imgType


def run(server_class=HTTPServer, handler_class=HandlerHTTP, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.socket = ssl.wrap_socket(httpd.socket, keyfile='./ressource/privkey.pem', certfile='./ressource/cert.pem', server_side=True)
    logging.info(termcolor.colored(" Starting httpd ...", "blue"))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info(termcolor.colored(" Stoppping httpd ...", "blue"))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        run(port=int(sys.argv[1]))
    else:
        run()
