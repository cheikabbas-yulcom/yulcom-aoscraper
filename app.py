# Modules
import streamlit as st
import main as ds
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

st.set_page_config(page_title="Appels d'offre", page_icon="logo.png")

# Functions
@st.cache
def load_data():
    return [ds.joffres(), ds.undp()]

try:
    dfs = load_data()

    site = st.sidebar.radio(label="**Choisir le site web**", options=["joffres.net", "PNUD"])

    if site == 'joffres.net':
        data = dfs[0]
        st.header("Appels d'offres du site joffres.net")
        st.info("Nombre d'offres : " + str(len(data)))
        gd = GridOptionsBuilder.from_dataframe(data)
        gd.configure_pagination(enabled=True)
        gd.configure_selection(use_checkbox=True)

        gridoptions = gd.build()
        grid_table = AgGrid(data, gridOptions=gridoptions, theme='alpine', height=300)
        sel_row = grid_table['selected_rows']
        st.subheader('Détails')
        if not sel_row:
            st.write('Sélectionner une offre pour afficher les détails')
        else:
            selected = sel_row[0]
            st.write(f"**TITRE**: {selected['Offres']}")
            st.write(f"**SOCIETE**: {selected['Societes']}")
            st.write(f"**LOCALITE**: {selected['Localites']}")
            st.write(f"**PUBLIE**: {selected['DatePublication']}")
            st.write(f"**DATE EXPIRATION**: {selected['DateExpiration']}")
            st.write(f'''
                        <a href='{selected['Liens']}'>
                            <button style='background-color:red; color:white'>Accéder à l'offre</button>
                        </a>''',
                        unsafe_allow_html=True)
    if site == 'PNUD':
        data = dfs[1]
        st.header("Appels d'offres du PNUD")
        st.info("Nombre d'offres : " + str(len(data)))
        gd = GridOptionsBuilder.from_dataframe(data)
        gd.configure_pagination(enabled=True)
        gd.configure_selection(use_checkbox=True)

        gridoptions = gd.build()
        grid_table = AgGrid(data, gridOptions=gridoptions, theme='alpine', height=300)
        sel_row = grid_table['selected_rows']
        st.subheader('Détails')
        if not sel_row:
            st.write('Sélectionner une offre pour afficher les détails')
        else:
            selected = sel_row[0]
            st.write(f"**TITRE**: {selected['Title']}")
            st.write(f"**SOCIETE**: UNDP, {selected['UNDP Office']}")
            st.write(f"**LOCALITE**: {selected['UNDP Country']}")
            st.write(f"**DATE PUBLICATION**: {selected['Posted']}")
            st.write(f"**DATE EXPIRATION**: {selected['Deadline']}")
            st.write(f'''
                        <a href='{selected['links']}'>
                            <button style='background-color:red; color:white'>Accéder à l'offre</button>
                        </a>''',
                     unsafe_allow_html=True)
except:
    st.write("Nous n'avons pas pu charger les données. Vérifier que vous êtes connecté à internet")
