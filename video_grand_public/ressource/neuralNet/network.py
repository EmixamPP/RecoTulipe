from manim import *

class Network(Graph):
    def __init__(self, neurones, center=(0,0), hDist=2, vDist=2, **kwargs):
        """
        :param neurones: [2,2,2]
        """

        if "vertex_config" not in kwargs:
            kwargs["vertex_config"] = {"radius":.3, "fill_opacity":1}

        if "vertex_type" not in kwargs:
            kwargs["vertex_type"] = Circle

        if "edge_config" not in kwargs:
            kwargs["edge_config"] = {"color": BLACK}


        self.neurones = neurones
        self.old = []#liste des verexe nuls
        self.labels = {} # dic contenant nom sommet: objet tex assosié
        n = sum(neurones) # nombre de neurones du graph
        vertices = [i for i in range(n)]

        #créé tous les arrêtes
        edges = []
        base = 0
        for j in range(len(neurones)-1):
            for k in range(base, base+neurones[j]):
                for l in range(base+neurones[j], base+neurones[j]+neurones[j+1]):
                    edges.append((k,l))
            base += neurones[j]

        pos = {}
        for c in range(len(neurones)):
            xPos = float(center[0]) - float((len(neurones)-1) * hDist) / 2 + hDist * c
            base=sum(neurones[:c])
            for j in range(neurones[c]):
                yPos = float(center[1]) - float((neurones[c]-1) * vDist) / 2 + vDist * j
                pos[base+j] = (xPos, yPos, 0)


        super().__init__(vertices, edges, layout=pos,**kwargs)

    def shift(self, deplacement):
        for el in self:
            el.shift(deplacement)

    def move_to(self, pos):
        for el in self:
            el.move_to(pos)

    def write_in_vertices(self, couples, **kwargs):
        """
        :Param couple: liste de tuple (nom_vertexe, texte à afficher dedans)
        :return: Liste des objets Tex
        """

        res = []
        for couple in couples:
            vertexe = self.vertices[couple[0]]
            texte = Tex(couple[1], **kwargs).next_to(vertexe, ORIGIN)
            res.append(texte)
            self.labels[self.vertices[couple[0]]] = texte
            self.add(texte)

        return res

    def create_edge_copy(self, edges, reverse=False, **kwargs):
        """
        :Param edges: liste de nom de edge
        """
        res = []
        for edge in edges:
            if reverse:
                edge = (edge[1], edge[0])
            old = self.edges[edge]

            if not reverse:
                newEdge = Line(old.get_start(), old.get_end(), **kwargs)
            else:
                newEdge = Line(old.get_end(), old.get_start(), **kwargs)


            #self.remove(old)
            self.old.append(old)
            self.add(newEdge)
            z_index = old.z_index
            newEdge.set_z_index(z_index)

            self.edges[edge] = newEdge
            res.append(newEdge)
        return res

    def clean(self):
        self.remove(*self.old)
        self.old=[]

    def get_neurones_on_layer(self, i):
        """
        retourne une liste des nom de neurones à la couche i
        """

        assert i<len(self.neurones), "numéro de couche trop grand"
        assert i>=0, "numéro < 0"

        base = sum(self.neurones[:i])

        res = [n+base for n in range(self.neurones[i])]
        return res

    def get_copy_vertice(self):
        return list(self.vertices.values())[0].copy()
