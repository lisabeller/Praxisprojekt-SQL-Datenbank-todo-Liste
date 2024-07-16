# Ausführen des Skripts in Kommandozeile (Miniconda)
# cd "PFAD"
# conda activate "Umgebung"
# streamlit run  "Datei"

# IMPORTE
import streamlit as st

import pandas as pd
import sqlalchemy as sa
from sqlalchemy import text
import yaml

import funktionen_todo as func
import klassen_todo as kla

# Streamlit UI
def main():
    st.title('Projekt Management System')

    # Sidebar mit Auswahlmöglichkeiten
    menu = ['Home', 'Projekt hinzufügen', 'Teammitglied hinzufügen', 'Aufgabe hinzufügen', 'Aufgaben anzeigen', 'Team anzeigen']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Home':
        st.subheader('Home')
        st.write('Willkommen im Projekt Management System')

    elif choice == 'Projekt hinzufügen':
        st.subheader('Projekt hinzufügen')
        projekt_name = st.text_input('Projektname')
        beschreibung = st.text_area('Beschreibung')
        startdatum = st.date_input('Startdatum')
        enddatum = st.date_input('Enddatum')

        if st.button('Projekt hinzufügen'):
            # Funktion aus der Projekt-Klasse aufrufen
            projekt = kla.Projekt(None, projekt_name, beschreibung, startdatum, enddatum)
            projekt.insert()
            

    elif choice == 'Teammitglied hinzufügen':
        st.subheader('Teammitglied hinzufügen')
        vorname = st.text_input('Vorname')
        nachname = st.text_input('Nachname')
        rolle = st.text_input('Rolle')
        email = st.text_input('Email')

        if st.button('Teammitglied hinzufügen'):
            # Funktion aus der Team-Klasse aufrufen
            teammitglied = kla.Team(None, vorname, nachname, rolle, email)
            teammitglied.insert()
            

    elif choice == 'Aufgabe hinzufügen':
        st.subheader('Aufgabe hinzufügen')
        aufgaben_name = st.text_input('Aufgabenname')
        aufgaben_beschreibung = st.text_area('Aufgabenbeschreibung')
        projekt_id = st.number_input('Projekt ID', min_value=1)
        mitarbeiter_id = st.number_input('Mitarbeiter ID', min_value=1)
        status = st.selectbox('Status', ['Offen', 'In Bearbeitung', 'Erledigt'])
        faelligkeit = st.date_input('Fälligkeitsdatum')

        if st.button('Aufgabe hinzufügen'):
            # Funktion aus der Aufgaben-Klasse aufrufen
            aufgabe = kla.Aufgaben(None, aufgaben_name, aufgaben_beschreibung, projekt_id, mitarbeiter_id, status, faelligkeit)
            aufgabe.insert()

    elif choice == 'Aufgaben anzeigen':
        st.subheader('Alle Aufgaben anzeigen')
        aufgaben_df = func.get_all_aufgaben()
        st.dataframe(aufgaben_df)

    elif choice == 'Team anzeigen':
        st.subheader('Team anzeigen')
        mitarbeiter_id = st.number_input('Mitarbeiter ID', min_value=1)

        if st.button('Info anzeigen'):
            mitarbeiter_info = func.get_info(mitarbeiter_id)
            if isinstance(mitarbeiter_info, pd.DataFrame):
                st.dataframe(mitarbeiter_info)
            else:
                st.write(mitarbeiter_info)

# Main-Funktion aufrufen
if __name__ == '__main__':
    main()