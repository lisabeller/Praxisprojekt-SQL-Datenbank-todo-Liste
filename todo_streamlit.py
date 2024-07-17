# Ausführen des Skripts in Kommandozeile (Miniconda)
# cd "PFAD"
# conda activate DataCraft
# streamlit run  todo_streamlit.py

# IMPORTE
import streamlit as st

import pandas as pd

import funktionen_todo as func
import klassen_todo as kla

# Streamlit UI
def main():
    st.title('Projekt Management System')

    # Hauptmenü
    menu = ['Home', 
            'Projekte',
            'Aufgaben',  
            'Team']
    
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Home':
        st.subheader('Home')
        st.write('Willkommen im Projekt Management System')

    # SUBMENU PROJEKTE
    elif choice == 'Projekte':
        st.subheader('Projekte')

       # Untermenü
        submenu = ['Projektübersicht', 'Projekt hinzufügen', 'Projekt bearbeiten', 'Projekt löschen']
        subchoice = st.sidebar.selectbox('Projekt Menu', submenu)

        if subchoice == 'Projektübersicht':
            projekt_table = func.display_table('projekte')
            st.dataframe(projekt_table)

        elif subchoice == 'Projekt hinzufügen':
            st.subheader('Projekt hinzufügen')
            projekt_name = st.text_input('Projektname')
            beschreibung = st.text_area('Beschreibung')
            startdatum = st.date_input('Startdatum')
            enddatum = st.date_input('Enddatum')

            if st.button('Projekt hinzufügen'):
                projekt = kla.Projekt(None, projekt_name, beschreibung, startdatum, enddatum)
                projekt.insert()
                st.success('Projekt erfolgreich hinzugefügt')

        elif subchoice == 'Projekt bearbeiten':
            st.subheader('Projekt bearbeiten')
            projekt_table = func.display_table('projekte')
            projekt_ids = projekt_table['projekt_id'].tolist()
            selected_projekt_id = st.selectbox('Wähle ein Projekt aus', projekt_ids)
            projekt_details = projekt_table[projekt_table['projekt_id'] == selected_projekt_id].iloc[0]

            projekt_name = st.text_input('Projektname', projekt_details['projekt_name'])
            beschreibung = st.text_area('Beschreibung', projekt_details['beschreibung'])
            startdatum = st.date_input('Startdatum', pd.to_datetime(projekt_details['startdatum']))
            enddatum = st.date_input('Enddatum', pd.to_datetime(projekt_details['enddatum']))

            if st.button('Projekt bearbeiten'):
                projekt = kla.Projekt(selected_projekt_id, projekt_name, beschreibung, startdatum, enddatum)
                projekt.update()
                st.success('Projekt erfolgreich bearbeitet')

        elif subchoice == 'Projekt löschen':
            st.subheader('Projekt löschen')
            projekt_table = func.display_table('projekte')
            projekt_ids = projekt_table['projekt_id'].tolist()
            selected_projekt_id = st.selectbox('Wähle ein Projekt aus', projekt_ids)
            projekt_details = projekt_table[projekt_table['projekt_id'] == selected_projekt_id].iloc[0]

            if st.button('Projekt löschen'):
                projekt = kla.Projekt(selected_projekt_id)
                projekt.delete()
                st.success('Projekt erfolgreich gelöscht')


    #SUBMENU AUFGBAEN
    elif choice == 'Aufgaben':
        st.subheader('Aufgaben verwalten')

        # Untermenü
        submenu = ['Aufgaben anzeigen', 'Aufgabe hinzufügen', 'Aufgabe bearbeiten', 'Aufgabe löschen']
        subchoice = st.sidebar.selectbox('Aufgaben Menu', submenu)

        if subchoice == 'Aufgaben anzeigen':
            aufgaben_table = func.display_table('aufgaben')
            st.dataframe(aufgaben_table)

        elif subchoice == 'Aufgabe hinzufügen':
            st.subheader('Aufgabe hinzufügen')
            projekt_table = func.display_table('projekte')
            projekt_ids = projekt_table['projekt_id'].tolist()
            selected_projekt_id = st.selectbox('Wähle ein Projekt aus', projekt_ids)
            aufgabenname = st.text_input('Aufgabenname')
            beschreibung = st.text_area('Beschreibung')
            status_options = ['Offen', 'In Bearbeitug', 'Erledigt']
            status = st.selectbox('Status', status_options)

            if st.button('Aufgabe hinzufügen'):
                aufgabe = kla.Aufgabe(None, selected_projekt_id, aufgabenname, beschreibung, status)
                aufgabe.insert()
                st.success('Aufgabe erfolgreich hinzugefügt')

        elif subchoice == 'Aufgabe bearbeiten':
            st.subheader('Aufgabe bearbeiten')
            aufgaben_table = func.display_table('aufgaben')
            aufgaben_ids = aufgaben_table['aufgaben_id'].tolist()
            selected_aufgabe_id = st.selectbox('Wähle eine Aufgabe aus', aufgaben_ids)
            aufgaben_details = aufgaben_table[aufgaben_table['aufgaben_id'] == selected_aufgabe_id].iloc[0]

            aufgabenname = st.text_input('Aufgabenname', aufgaben_details['aufgaben_name'])
            beschreibung = st.text_area('Beschreibung', aufgaben_details['aufgaben_beschreibung'])
    
            # Definieren der Status-Optionen
            status_options = ['Offen', 'In Bearbeitung', 'Erledigt']

            # Setzen des Status über einen Fallback-Mechanismus
            # Standardindex, falls der Status nicht in der Liste gefunden wird
            default_index = 0 

            if aufgaben_details['status'] in status_options:
                default_index = status_options.index(aufgaben_details['status'])

            status = st.selectbox('Status', status_options, index=default_index)

            if st.button('Aufgabe bearbeiten'):
                aufgabe = kla.Aufgaben(selected_aufgabe_id, aufgaben_table['projekt_id'], aufgabenname, beschreibung, status)
                aufgabe.update()
                st.success('Aufgabe erfolgreich bearbeitet')
                

        elif subchoice == 'Aufgabe löschen':
            st.subheader('Aufgabe löschen')
            aufgaben_table = func.display_table('aufgaben')
            aufgaben_ids = aufgaben_table['aufgaben_id'].tolist()
            selected_aufgabe_id = st.selectbox('Wähle eine Aufgabe aus', aufgaben_ids)
            aufgaben_details = aufgaben_table[aufgaben_table['aufgaben_id'] == selected_aufgabe_id].iloc[0]

            if st.button('Aufgabe löschen'):
                aufgabe = kla.Aufgaben(selected_aufgabe_id)
                aufgabe.delete()
                st.success('Aufgabe erfolgreich gelöscht')


    # SUBMENU TEAM 
    elif choice == 'Team':
        st.subheader('Team verwalten')

        # Untermenü
        submenu = ['Team anzeigen', 'Infos', 'Teammitglied hinzufügen', 'Teammitglied bearbeiten', 'Teammitglied löschen']
        subchoice = st.sidebar.selectbox('Team Menu', submenu)

        if subchoice == 'Team anzeigen':
            team_table = func.display_table('team')
            st.dataframe(team_table)

        elif subchoice == 'Infos':
            st.subheader('Informationen')
            team_table = func.display_table('team')

            # Selectbox mit vorhanden Mitarbeiter-IDs
            mitarbeiter_ids = team_table['mitarbeiter_id'].tolist()
            selected_mitarbeiter_id = st.selectbox('Mitarbeiter ID', mitarbeiter_ids)
           
            if st.button('Info anzeigen'):
                mitarbeiter_info = func.get_info(selected_mitarbeiter_id)
                if isinstance(mitarbeiter_info, pd.DataFrame):
                     st.dataframe(mitarbeiter_info)
                else:
                    st.write(mitarbeiter_info)
            

        elif subchoice == 'Teammitglied hinzufügen':
            st.subheader('Neues Teammitglied hinzufügen')
            # Hier Code einfügen, um ein neues Teammitglied hinzuzufügen
            vorname = st.text_input('Vorname')
            nachname = st.text_input('Nachname')
            rolle = st.text_input('Rolle')
            email = st.text_input('E-Mailadresse')

            if st.button('Teammitglied hinzufügen'):
                neues_mitglied = kla.Team(None, vorname, nachname, rolle, email)
                neues_mitglied.insert()
                st.success('Mitglied erfolgreich hinzugefügt')

        elif subchoice == 'Teammitglied bearbeiten':
            st.subheader('Teammitglied bearbeiten')

            # Selectbox mit vorhanden Mitarbeiter-IDs
            team_table = func.display_table('team')
            mitarbeiter_ids = team_table['mitarbeiter_id'].tolist()
            selected_mitarbeiter_id = st.selectbox('Mitarbeiter ID auswählen', mitarbeiter_ids)
           
            vorname = st.text_input('Neuer Vorname')
            nachname = st.text_input('Neuer Nachname')
            rolle = st.text_input('Neue Rolle')
            email = st.text_input('Neue E-Mailadresse')

            if st.button('Teammitglied aktualisieren'):
                team = kla.Team(selected_mitarbeiter_id, vorname, nachname, rolle, email)
                team.update()
                st.success('Mitglied erfolgreich aktualisiert')


        elif subchoice == 'Teammitglied löschen':
            st.subheader('Teammitglied löschen')
        
            # Selectbox mit vorhanden Mitarbeiter-IDs
            team_table = func.display_table('team')
            mitarbeiter_ids = team_table['mitarbeiter_id'].tolist()
            selected_mitarbeiter_id = st.selectbox('Mitarbeiter ID auswählen', mitarbeiter_ids)

            if st.button('Teammitglied löschen'):
                team = kla.Team(selected_mitarbeiter_id)
                team.delete()
                st.success('Mitglied erfolgreich gelöscht')
           

# Main-Funktion aufrufen
if __name__ == '__main__':
    main()

# Funktion Status ändern
# Tabellen anzeigen lassen mit Dropdown
# 