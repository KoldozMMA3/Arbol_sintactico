import pandas as pd
import lex_calculador
from graphviz import Digraph

# Definition of the NodoPila class
class NodoPila:
    def __init__(self, simbolo, lexema):
        global contador
        self.simbolo = simbolo
        self.lexema = lexema
        self.id = contador + 1
        contador += 1

# Definition of the NodoArbol class
class NodoArbol:
    def __init__(self, id, simbolo, lexema):
        self.id = id
        self.simbolo = simbolo
        self.lexema = lexema
        self.hijos = []
        self.padre = None

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)
        hijo.padre = self

# Function to search for a node in the tree
def buscar_nodo(id, nodo):
    if nodo.id == id:
        return nodo
    else:
        for hijo in nodo.hijos:
            resultado = buscar_nodo(id, hijo)
            if resultado is not None:
                return resultado
        return None

# Function to print the tree
def imprimir_arbol(nodo, dot=None, nivel=0):
    if dot is None:
        dot = Digraph(comment='Arbol de Derivacion')

    # Include the lexema in addition to the symbol in the node
    nodo_label = f"{nodo.simbolo} ({nodo.lexema})" if nodo.lexema is not None else nodo.simbolo

    # Configure style and fill color for the node
    dot.node(str(nodo.id), nodo_label, style='filled', fillcolor='aqua')

    for hijo in nodo.hijos:
        # Configure edge color for the edge
        dot.edge(str(nodo.id), str(hijo.id), color='yellow')
        imprimir_arbol(hijo, dot, nivel + 1)

    return dot

# Load the table and set up the initial stack
tabla = pd.read_csv("parcialCompiladores/tabla.csv", index_col=0)
contador = 0
pila = []

# Initialize the stack with start and end symbols
simbolo_E = NodoPila('INICIO_CODIGO', None)
simbolo_dolar = NodoPila('$', None)
pila.append(simbolo_dolar)
pila.append(simbolo_E)

# Configure the tree with the start symbol
raiz = NodoArbol(simbolo_E.id, simbolo_E.simbolo, simbolo_E.lexema)

# Define the input
entrada = [
    {"simbolo": "INICIO_PROCESO", "lexema": "INICIO_PROCESO", "nroline": 1, "col": 1},
    {"simbolo": "IMPRESOR", "lexema": "IMPRESOR", "nroline": 1, "col": 15},
    {"simbolo": "CADENA_TEXTO", "lexema": "Hola, Mundo!", "nroline": 1, "col": 24},
    {"simbolo": "FIN_PROCESO", "lexema": "FIN_PROCESO", "nroline": 1, "col": 39},
    {"simbolo": "$", "lexema": "$", "nroline": 0, "col": 0},
]


index_entrada = 0

# Analyze the input
while len(pila) > 0:
    simbolo_entrada = entrada[index_entrada]["simbolo"]

    # Check if the input symbol is valid
    if simbolo_entrada not in tabla.columns:
        print("Error en el proceso sintactico")
        break

    # Compare the top of the stack with the input symbol
    if pila[-1].simbolo == simbolo_entrada:
        pila.pop()
        index_entrada += 1
    else:
        # Get the production from the analysis table
        produccion = tabla.loc[pila[-1].simbolo, simbolo_entrada]

        # Handle syntax errors
        if isinstance(produccion, float):
            print("Error en el proceso sintactico")
            break

        # Apply the production on the stack and the tree
        if produccion != ('e'):
            padre = buscar_nodo(pila[-1].id, raiz)
            pila.pop()
            for simbolo in reversed(str(produccion).split()):
                nodo_p = NodoPila(simbolo, None)
                pila.append(nodo_p)
                hijo = NodoArbol(nodo_p.id, nodo_p.simbolo, nodo_p.lexema)
                padre.agregar_hijo(hijo)
        else:
            pila.pop()

# Check the result of the analysis
if len(pila) == 0:
    print("Proceso ejecutado correctamente")
else:
    print("Error en el proceso sintactico: pila no vacia al finalizar")

# Print and visualize the tree
dot = imprimir_arbol(raiz)
dot.render('arbol', format='png', cleanup=True)
print("Arbol de derivacion generado y guardado como 'arbol.png'.")
