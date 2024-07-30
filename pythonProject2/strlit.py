import streamlit as st
import pandas as pd
import ID3
import graphviz as gv


class ID3Streamlit:

    def run(self):
        st.title("Algoritmo ID3")
        st.write("Seleccione un fichero CSV para aplicar el algoritmo ID3")

        uploaded_file = st.file_uploader("Seleccione un fichero CSV", type=["csv"])

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.write("Fichero CSV cargado correctamente")

            # Convertir el DataFrame a una lista de listas y construir el arbol
            #las caracteristicas y las etiquetas son necesarias en listas separadas
            # ya que son datos que se leen y modifican en las llamadas recursivas
            caracteristicas = df.iloc[0]
            caract = caracteristicas.values.tolist()
            etiq = df.iloc[:,-1]
            etiquetas= etiq.values.tolist()
            datos = df.values.tolist()
            ID3.ID3.build_ID3(datos, caract, etiquetas)
            gv.Graph(ID3.ID3.getArbol())


            # Pedir al usuario que seleccione las características y la etiqueta
            caracteristicas = st.multiselect("Seleccione las características", df.columns.tolist())
            etiqueta = st.selectbox("Seleccione la etiqueta", df.columns.tolist())

            # Crear una lista con los índices de las características seleccionadas
            caracteristicas_indices = [df.columns.tolist().index(c) for c in caracteristicas]

            # Llamar al algoritmo ID3
            arbol = self.id3.id3(df, caracteristicas_indices, [etiqueta])

            # Mostrar el árbol de decisión
            st.write("Árbol de decisión:")
            st.code(arbol)


if __name__ == "__main__":
    id3_streamlit = ID3Streamlit()
    id3_streamlit.run()
