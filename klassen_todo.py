# Importe
import streamlit as st
import pandas as pd
import sqlalchemy as sa
import yaml
from sqlalchemy import text

# Projektklasse
class Projekt:
    def __init__(self, 
                 projekt_id, 
                 projekt_name = None, 
                 beschreibung = None, 
                 startdatum = None, 
                 enddatum = None):
        self.projekt_id = projekt_id
        self.projekt_name = projekt_name
        self.beschreibung = beschreibung
        self.startdatum = startdatum
        self.enddatum = enddatum
    
        # Standart-config-Datei laden
        with open('..\\config.yaml', 'r') as file:
            config = yaml.load(file, Loader=yaml.BaseLoader)

        # Connection-String
        con_string_todo_list = f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/todo"

        # Verbindung zur Datenbank
        self.sa_eng = sa.create_engine(con_string_todo_list, isolation_level='AUTOCOMMIT')

        # Metadaten und Auswahl Tabelle
        meta = sa.MetaData()
        self.projekte_table = sa.Table('projekte', meta, autoload_with=self.sa_eng)

    # Definition INSERT 
    def insert(self):
        # Einträge definieren
        ins = self.projekte_table.insert().values(
            projekt_name=self.projekt_name,
            beschreibung=self.beschreibung,
            startdatum=self.startdatum,
            enddatum=self.enddatum
        )
        
        with self.sa_eng.connect() as con:
            try:
                con.execute(ins)
                print(f"Das Projekt {self.projekt_name} wurde erfolgreich angelegt.")
            except sa.exc.SQLAlchemyError as e:
                print(f"Fehler beim Einfügen in die Datenbank: {e}")

    # Definition UPDATE 
    def update(self):
        # Einträge definieren
        upd = self.projekte_table.update().where(
                self.projekte_table.c.projekt_id == self.projekt_id).values(
                    projekt_name=self.projekt_name,
                    beschreibung=self.beschreibung,
                    startdatum=self.startdatum,
                    enddatum=self.enddatum
                    )
        
        with self.sa_eng.connect() as con:
            try:
                con.execute(upd)
                print(f"Das Projekt {self.projekt_name} wurde erfolgreich geändert.")
            except sa.exc.SQLAlchemyError as e:
                print(f"Fehler beim Aktualisieren in der Datenbank: {e}")

     # Definition DELETE 
    def delete(self):
        with self.sa_eng.connect() as con:
            # Abfrage, ob Aufgaben mit dem Projekt verknüpft sind
            query = text('SELECT COUNT(*) FROM aufgaben WHERE projekt_id = :projekt_id')
            result = con.execute(query,{'projekt_id': self.projekt_id}).fetchone()
            count_tasks = result[0]
            
            if count_tasks > 0:
                print(f"Das Projekt {self.projekt_name} kann nicht gelöscht werden, da noch {count_tasks} Aufgaben damit verknüpft sind.")
                return

            # Wenn keine Aufgaben verknüpft sind, Projekt löschen
            delete_projekt = self.projekte_table.delete().where(
                                self.projekte_table.c.projekt_id == self.projekt_id)
            
            try:
                con.execute(delete_projekt)
                print(f"Das Projekt {self.projekt_name} wurde erfolgreich gelöscht.")

                # Auswahl und Anzeige der aktuellen Projekt Tabelle
                query = self.projekte_table.select()
                pd.read_sql(query, con)
            except sa.exc.SQLAlchemyError as e:
                print(f"Fehler beim Löschen aus der Datenbank: {e}")

# Teamklasse
class Team:
    def __init__(self, 
                 mitarbeiter_id, 
                 vorname = None, 
                 nachname = None, 
                 rolle = None, 
                 email = None):
        self.mitarbeiter_id = mitarbeiter_id
        self.vorname = vorname
        self.nachname = nachname
        self.rolle = rolle
        self.email = email
        
        # Standard-config-Datei laden und Verbindung zur Datenbank herstellen
        with open('..\\config.yaml', 'r') as file:
            config = yaml.safe_load(file)

        # Connection-String für SQLAlchemy
        con_string_todo_list = f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/todo"

        # Verbindung zur Datenbank herstellen
        self.sa_eng = sa.create_engine(con_string_todo_list, isolation_level='AUTOCOMMIT')

        # Metadaten und Auswahl der Tabelle
        meta = sa.MetaData()
        self.team_table = sa.Table('team', meta, autoload_with=self.sa_eng)

    # Definition INSERT 
    def insert(self):
        # Einträge definieren und einfügen
        ins = self.team_table.insert().values(
            vorname=self.vorname,
            nachname=self.nachname,
            rolle=self.rolle,
            email=self.email)
        
        with self.sa_eng.connect() as con:
            try:
                con.execute(ins)
                print(f"Die Person {self.nachname}, {self.vorname} wurde erfolgreich in die Tabelle eingefügt.")
            except sa.exc.SQLAlchemyError as e:
                print(f"Fehler beim Einfügen in die Datenbank: {e}")
            
            # Auswahl und Anzeige der Team Tabelle
            query = self.team_table.select()
            pd.read_sql(query, con)


    # Definition UPDATE 
    def update(self):
        # Einträge definieren und aktualisieren
        upd = self.team_table.update().where(
                    self.team_table.c.mitarbeiter_id == self.mitarbeiter_id).values(
            vorname=self.vorname,
            nachname=self.nachname,
            rolle=self.rolle,
            email=self.email)
                
        with self.sa_eng.connect() as con:
            try:
                con.execute(upd)
            except sa.exc.SQLAlchemyError as e:
                print(f"Fehler beim Aktualisieren in der Datenbank: {e}")

            print(f"Die Person {self.vorname} {self.nachname} wurde erfolgreich in der Tabelle aktualisiert.")

            # Auswahl und Anzeige der Team Tabelle
            query = self.team_table.select()
            pd.read_sql(query, con)

    # Definition DELETE 
    def delete(self):
        # Einträge definieren und löschen
        delete_id = self.team_table.delete().where(
                        self.team_table.c.mitarbeiter_id == self.mitarbeiter_id)
        
        with self.sa_eng.connect() as con:
            try:
                con.execute(delete_id)

                # Auswahl und Anzeige der aktuellen Team Tabelle
                query = self.team_table.select()
                pd.read_sql(query, con)

            except sa.exc.SQLAlchemyError as e:
                print(f"Fehler beim Löschen aus der Datenbank: {e}")


# Aufgabenklasse
class Aufgaben:
    # Standartwert None um Argumentenübergabe bei Aufruf zu verkürzen
    def __init__(self, aufgaben_id, 
                 aufgaben_name = None,  
                 projekt_id = None, 
                 aufgaben_beschreibung = None,
                 mitarbeiter_id = None, 
                 status = None, 
                 erstellungsdatum = None, 
                 faelligkeit = None):
        self.aufgaben_id = aufgaben_id
        self.aufgaben_name = aufgaben_name
        self.projekt_id = projekt_id
        self.aufgaben_beschreibung = aufgaben_beschreibung
        self.mitarbeiter_id = mitarbeiter_id
        self.status = status
        self.erstellungsdatum = erstellungsdatum 
        self.faelligkeit = faelligkeit

        # Standart-config-Datei laden
        with open('..\\config.yaml', 'r') as file:
            config = yaml.load(file, Loader=yaml.BaseLoader)

        # Connection-String
        con_string_todo_list = f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/todo"

        # Verbindung zur Datenbank
        self.sa_eng = sa.create_engine(con_string_todo_list, isolation_level='AUTOCOMMIT')

        # Metadaten und Auswahl Tabelle
        meta = sa.MetaData()
        self.aufgaben_table = sa.Table('aufgaben', meta, autoload_with=self.sa_eng)

    # Definition INSERT 
    def insert(self):
        # Einträge definieren
        ins = self.aufgaben_table.insert().values(
            aufgaben_name = self.aufgaben_name,
            aufgaben_beschreibung = self.aufgaben_beschreibung,
            projekt_id = self.projekt_id,
            mitarbeiter_id = self.mitarbeiter_id,
            status = self.status,
            faelligkeit = self.faelligkeit
        )
        
        with self.sa_eng.connect() as con:
            con.execute(ins)

            print(f"Die Aufgabe {self.aufgaben_name} wurde erfolgreich in die Tabelle eingefügt.")

            # Auswahl und Anzeige der Aufgaben mit der gleichen Projekt-ID
            query = self.aufgaben_table.select().where(
                    self.aufgaben_table.c.projekt_id == self.projekt_id)
            
            pd.read_sql(query, con)
    
    
    # Definition UPDATE 
    def update(self):
        with self.sa_eng.connect() as con:
            # Aktuelle Werte aus der Datenbank abrufen
            result = con.execute(text('SELECT * FROM aufgaben WHERE aufgaben_id = :id'), {'id': self.aufgaben_id}).fetchone()

            if result is None:
                print(f"Die Aufgabe mit ID {self.aufgaben_id} wurde nicht gefunden.")
                return
            
            # Extrahieren der Werte aus der result-Liste
            current_values = {
                'aufgaben_name': result[1],
                'projekt_id': result[2],
                'aufgaben_beschreibung': result[3],
                'mitarbeiter_id': result[4],
                'status': result[5],
                'erstellungsdatum': result[6],
                'faelligkeit': result[7]
            }

            # Nur die angegebenen Werte ändern, andere unverändert lassen
            updated_values = {
                'aufgaben_name': self.aufgaben_name if self.aufgaben_name is not None else current_values['aufgaben_name'],
                'projekt_id': self.projekt_id if self.projekt_id is not None else current_values['projekt_id'],
                'aufgaben_beschreibung': self.aufgaben_beschreibung if self.aufgaben_beschreibung is not None else current_values['aufgaben_beschreibung'],  
                'mitarbeiter_id': self.mitarbeiter_id if self.mitarbeiter_id is not None else current_values['mitarbeiter_id'],
                'status': self.status if self.status is not None else current_values['status'],
                'erstellungsdatum': self.erstellungsdatum if self.erstellungsdatum is not None else current_values['erstellungsdatum'],
                'faelligkeit': self.faelligkeit if self.faelligkeit is not None else current_values['faelligkeit']
            }

            # Update-Statement mit den aktualisierten Werten
            upd = self.aufgaben_table.update().where(
                    self.aufgaben_table.c.aufgaben_id == self.aufgaben_id).values(updated_values)

            con.execute(upd)
            print(f"Die Aufgabe '{updated_values['aufgaben_name']}' wurde erfolgreich in der Tabelle aktualisiert.")

            # Auswahl und Anzeige der Aufgaben mit der gleichen Projekt-ID
            query = self.aufgaben_table.select().where(
                    self.aufgaben_table.c.projekt_id == updated_values['projekt_id'])
            pd.read_sql(query, con)


    # Definition DELETE 
    def delete(self):
        with self.sa_eng.connect() as con:
            # Aufgaben-ID abrufen, bevor gelöscht wird
            result = con.execute(text('SELECT projekt_id FROM aufgaben WHERE aufgaben_id = :id'),
                                     {'id': self.aufgaben_id}).fetchone()

            if result is None:
                print(f"Die Aufgabe mit ID {self.aufgaben_id} ist nicht vorhanden.")
                return

            self.projekt_id = result[0]

            # Aufgabe löschen
            con.execute(text('DELETE FROM aufgaben WHERE aufgaben_id = :id'), {'id': self.aufgaben_id})
            print(f"Die Aufgabe mit ID {self.aufgaben_id} wurde erfolgreich in der Tabelle gelöscht.")

            # Anzeige der verbleibenden Aufgaben mit der gleichen Projekt-ID
            if self.projekt_id is not None:
                query = con.execute(text('SELECT * FROM aufgaben WHERE projekt_id = :projekt_id'), {'projekt_id': self.projekt_id})
                df = pd.DataFrame(query.fetchall(), columns=query.keys())
                print(f"Folgende Aufgaben mit Projekt_id: {self.projekt_id} sind noch offen")
                df
            else:
                print(f"Fehler beim Löschen der Aufgabe: {self.aufgaben_id}")