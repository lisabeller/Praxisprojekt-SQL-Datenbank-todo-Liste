<br><br><center><h2 style="font-size:3em">Praxisprojekt Datenbanken und SQL</h1></center>

- Ausführen des Skripts in Kommandozeile (Miniconda)
- cd "PFAD"
- streamlit run "Dateiname"

### Projektbeschreibung

Allgemein: ToDo-Listen Anwendung in Python, die Daten in einer SQL-Datenbank speichert

#### Code Überblick

##### Datenbankverbindung und -erstellung

- Verbindungsaufbau zu einer PostgreSQL-Datenbank mit SQLAlchemy
- Erstellung der Datenbank todo

##### Tabellenstruktur

Projekte (projekte)
- projekt_id (Primärschlüssel)
- projekt_name (Text, nicht null)
- beschreibung (Text)
- startdatum (Datum, nicht null)
- enddatum (Datum)

Team (team)
- mitarbeiter_id (Primärschlüssel)
- vorname, nachname (Text, nicht null)
- rolle (Text)
- email (Text, nicht null)

Aufgaben (aufgaben)
- aufgaben_id (Primärschlüssel)
- aufgaben_name (Text, nicht null)
- projekt_id (Fremdschlüssel)
- aufgaben_beschreibung (Text)
- mitarbeiter_id (Fremdschlüssel)
- status (Text)
- erstellungsdatum (Timestamp, Standard CURRENT_TIMESTAMP)
- faelligkeit (Datum)

##### Klassen und Methoden

Klasse Projekt
- Methoden: insert, update, delete
- Verwaltung von Projekten: Hinzufügen, Aktualisieren, Löschen (inkl. Prüfung auf verknüpfte Aufgaben)

Klasse Team
- Methoden: insert, update, delete
- Verwaltung von Teammitgliedern: Hinzufügen, Aktualisieren, Löschen

Klasse Aufgaben
- Methoden: insert, update, delete
- Verwaltung von Aufgaben: Hinzufügen, Aktualisieren, Löschen (inkl. Anzeige der verbleibenden Aufgaben)

##### Zusätzliche Funktionen
- get_info(mitarbeiter_id): Abfrage von Informationen zu Aufgaben eines bestimmten Mitarbeiters.
- get_all_aufgaben(): Abfrage und Anzeige aller Aufgaben.
- set_status_erledigt(aufgaben_id): Setzt den Status einer Aufgabe auf "Erledigt".
- set_status(aufgaben_id, status): Setzt den Status einer Aufgabe auf einen gegebenen Wert.
- display_table(tabellen_name): Anzeige einer Tabelle aus der Datenbank.

##### Log-Tabellen und Trigger
- Log Tabellen für Projekte, Aufgaben und Team.
- Trigger Funktionen für Insert, Update und Delete auf den Projekten, Aufgaben und Team-Tabellen
- Änderungen werden in den Log-Tabellen gespeichern


