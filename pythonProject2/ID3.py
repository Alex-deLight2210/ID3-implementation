import math

from collections import Counter

from binarytree import Node


class ID3:
    #El algoritmo ID3 es un algoritmo usado para construir arboles de decision
    #a partir de conjuntos de datos nominales(muy importante esto), que usando
    #formulas de ciencia de la informacion agrupa los datos por caracteristicas
    #arbitrarias en base a la entropia que genera dicha clasificacion en conjunto
    #y la ganancia que estas generan
    def __init__(self):

        self.arbol = None


    def calcular_ganancia(self, datos, caracteristica, entropia_general):

        # Calcula la ganancia de información para una característica

        valores_caracteristica = [fila[caracteristica] for fila in datos]

        valores_unicos = set(valores_caracteristica)

        ganancia = entropia_general

        for valor in valores_unicos:

            subset = [fila for fila in datos if fila[caracteristica] == valor]

            probabilidad = len(subset) / len(datos)

            entropia = self.calcular_entropia(subset)

            ganancia -= probabilidad * entropia

        return ganancia


    def calcular_entropia(self, datos):

        # Calcula la entropía de un conjunto de datos

        etiquetas = [fila[-1] for fila in datos]

        n = len(etiquetas)

        counter = Counter(etiquetas)

        entropia = 0.0

        for cuenta in counter.values():

            probabilidad = cuenta / n

            entropia -= probabilidad * math.log2(probabilidad)

        return entropia


    def build_ID3(self, datos, caracteristicas, etiquetas):

        # Implementación del algoritmo ID3

        if len(caracteristicas) == 0:

            # Si no hay más características, devuelve la etiqueta más común
            # esto se usa como condicion de parada cuando el agoritmo revisa
            # todo el conjunto de datos
            etiqueta_mas_comun = Counter([fila[-1] for fila in datos]).most_common(1)[0][0]

            return Node(etiqueta_mas_comun)


        # Calcula la entropía general
        # Esto se hace en cada llamada recursiva para a partir de la entropia
        # general del grupo, ver cual caracteristica genera mas ganancia
        entropia_general = self.calcular_entropia(datos)


        # Encuentra la característica con la mayor ganancia de información

        mejor_caracteristica = None

        mejor_ganancia = 0.0

        for caracteristica in caracteristicas:

            ganancia = self.calcular_ganancia(datos, caracteristica, entropia_general)

            if ganancia > mejor_ganancia:

                mejor_ganancia = ganancia

                mejor_caracteristica = caracteristica


        # Crea un nodo con la mejor característica

        nodo = Node(mejor_caracteristica)


        # Recorre las características restantes
        # a partir de aqui se genera un nuevo subconjunto de datos
        # que descarta los valores ya analizados para asi usarlos en la llamada recursiva

        for valor in set([fila[mejor_caracteristica] for fila in datos]):
            caracteristicas_rest = [c for c in caracteristicas if c != mejor_caracteristica]
            subset = [fila for fila in datos if fila[mejor_caracteristica] == valor]
            etiquetas_subset = [fila[-1] for fila in subset]
            nodo_hijo = ID3.id3(subset, caracteristicas_rest, etiquetas_subset)
            nodo.left = nodo_hijo if nodo.left is None else nodo.right
            if nodo.left == nodo_hijo:
                nodo.left = Node(f"{mejor_caracteristica}={valor}")
                nodo.left.left = nodo_hijo
            else:
                nodo.right = Node(f"{mejor_caracteristica}={valor}")
                nodo.right.left = nodo_hijo

        return nodo

    def clasificar(self, datos):
        resultados = []
        for fila in datos:
            resultado = self._recorrer_arbol(fila, self.arbol)
            resultados.append(resultado)
        return resultados

    # este metodo se usa para recorrer el arbol ya construido
    # para clasificar datos de entrada de usuario
    def _recorrer_arbol(self, fila, nodo):
        if nodo.left is None and nodo.right is None:
            # Si el nodo es una hoja, devuelve la etiqueta
            return nodo.value
        else:
            # Si el nodo no es una hoja, recorre el árbol según la característica
            caracteristica = nodo.value
            valor_caracteristica = fila[caracteristica]
            if nodo.left is not None:
             if nodo.left.value.startswith(caracteristica + "="):
                # Si el nodo izquierdo tiene la característica, recorre el árbol por la izquierda
                return self._recorrer_arbol(fila, nodo.left.left)
             elif nodo.right is not None:
                if nodo.right.value.startswith(caracteristica + "="):
                # Si el nodo derecho tiene la característica, recorre el árbol por la derecha
                 return self._recorrer_arbol(fila, nodo.right.left)
                else:
                # Si no se encuentra la característica, devuelve un error
                 return "Error: no se encuentra la característica"

    def getArbol(self):

        return self.arbol