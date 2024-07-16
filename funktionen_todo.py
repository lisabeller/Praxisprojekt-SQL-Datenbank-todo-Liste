# Modul-IMPORTE

import streamlit as st
import pandas as pd
import sqlalchemy as sa
import yaml
from sqlalchemy import text

#FUNKTION Mitarbeiter Informationen
def get_info(mitarbeiter_id):
    # Standart-config-Datei laden
    with open('..\\config.yaml', 'r') as file:
        config = yaml.load(file, Loader=yaml.BaseLoader)

    # Connection-String
    con_string_todo_list = f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/todo"

    # Verbindung zur Datenbank
    sa_eng = sa.create_engine(con_string_todo_list, isolation_level='AUTOCOMMIT')

    query = text('''
        SELECT 
            t.vorname || ' ' || t.nachname AS mitarbeiter_name,
            p.projekt_name,
            a.aufgaben_name,
            a.status
        FROM 
            team t
        LEFT JOIN 
            aufgaben a ON t.mitarbeiter_id = a.mitarbeiter_id
        LEFT JOIN 
            projekte p ON a.projekt_id = p.projekt_id
        WHERE 
            t.mitarbeiter_id = :mitarbeiter_id;
    ''')
    
    with sa_eng.connect() as con:
        result = con.execute(query, {'mitarbeiter_id': mitarbeiter_id}).fetchall()
    
    if result:
        df = pd.DataFrame(result, columns=['Mitarbeiter', 'Projekt', 'Aufgabe', 'Status'])
        return df
    else:
        return f"Keine Daten für Mitarbeiter-ID {mitarbeiter_id} gefunden."
    

# FUNKTION Aufgaben anzeigen lassen
def get_all_aufgaben():
    # Standart-config-Datei laden
    with open('..\\config.yaml', 'r') as file:
        config = yaml.load(file, Loader=yaml.BaseLoader)

    # Connection-String
    con_string_todo_list = f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/todo"

    # Verbindung zur Datenbank
    sa_eng = sa.create_engine(con_string_todo_list, isolation_level='AUTOCOMMIT')

    query = text('''
        SELECT 
            a.aufgaben_id,
            a.aufgaben_name,
            p.projekt_name,
            t.vorname || ' ' || t.nachname AS mitarbeiter_name,
            a.aufgaben_beschreibung,
            a.status
        FROM 
            aufgaben a
        LEFT JOIN 
            projekte p ON a.projekt_id = p.projekt_id
        LEFT JOIN 
            team t ON a.mitarbeiter_id = t.mitarbeiter_id;
    ''')
    
    with sa_eng.connect() as con:
        result = con.execute(query).fetchall()
    
    if result:
        df = pd.DataFrame(result, columns=['Aufgaben ID', 'Aufgabe', 'Projekt', 'Mitarbeiter', 'Aufgaben Beschreibung', 'Status'])
        return df
    else:
        return print("Keine Aufgaben gefunden.")

# FUNKTION Status auf erledigt setzten
def set_status_erledigt(aufgaben_id):
    # Standart-config-Datei laden
    with open('..\\config.yaml', 'r') as file:
        config = yaml.load(file, Loader=yaml.BaseLoader)

    # Connection-String
    con_string_todo_list = f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/todo"

    # Verbindung zur Datenbank
    sa_eng = sa.create_engine(con_string_todo_list, isolation_level='AUTOCOMMIT')

    update_query = text('''
        UPDATE aufgaben
        SET status = 'Erledigt'
        WHERE aufgaben_id = :aufgaben_id;
    ''')
    
    with sa_eng.connect() as con:
        try:
            con.execute(update_query, {'aufgaben_id': aufgaben_id})
            print(f"Status der Aufgaben ID {aufgaben_id} wurde auf 'Erledigt' gesetzt.")
        except sa.exc.SQLAlchemyError as e:
            print(f"Fehler beim Aktualisieren des Status: {e}")

# FUNKTION Status ändern
def set_status(aufgaben_id, status):
    # Standard-config-Datei laden
    with open('..\\config.yaml', 'r') as file:
        config = yaml.load(file, Loader=yaml.BaseLoader)

    # Connection-String
    con_string_todo_list = f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/todo"

    # Verbindung zur Datenbank
    sa_eng = sa.create_engine(con_string_todo_list, isolation_level='AUTOCOMMIT')

    update_query = text('''
        UPDATE aufgaben
        SET status = :status
        WHERE aufgaben_id = :aufgaben_id;
    ''')

    with sa_eng.connect() as con:
        try:
            con.execute(update_query, {'aufgaben_id': aufgaben_id, 'status': status})
            print(f"Status der Aufgaben ID {aufgaben_id} wurde auf '{status}' gesetzt.")
        except sa.exc.SQLAlchemyError as e:
            print(f"Fehler beim Aktualisieren des Status: {e}")


# FUNKTION Tabelle anzeigen lassen
def display_table(tabellen_name):
    # Standart-config-Datei laden
    with open('..\\config.yaml', 'r') as file:
        config = yaml.load(file, Loader=yaml.BaseLoader)

    # Connection-String
    con_string_todo_list = f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/todo"

    # Verbindung zur Datenbank
    sa_eng = sa.create_engine(con_string_todo_list, isolation_level='AUTOCOMMIT')

    with sa_eng.connect() as con:
        try:
            # Versuche, die Tabelle aus der Datenbank abzurufen
            tabelle = pd.read_sql(tabellen_name, con)
            tabelle
        except sa.exc.NoSuchTableError as e:
            # Falls die Tabelle nicht existiert, gib eine Fehlermeldung aus
            print(f"Die Tabelle '{tabellen_name}' existiert nicht in der Datenbank.")
        except Exception as e:
            # Falls es andere Fehler gibt, gib eine generelle Fehlermeldung aus
            print(f"Fehler beim Abrufen der Tabelle '{tabellen_name}': {e}")



