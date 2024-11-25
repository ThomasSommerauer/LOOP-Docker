from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from alembic.config import Config
from alembic import command
import os

# Verbindung zur PostgreSQL-Datenbank herstellen
DATABASE_URL = "postgresql+psycopg2://my_user:my_password@localhost:5432/my_database"

# Datenbank-Engine erstellen
engine = create_engine(DATABASE_URL)

# Basis-Klasse für Tabellenmodelle
Base = declarative_base()

# Tabellenmodell erstellen
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    age = Column(Integer)  # age-Spalte hinzufügen, falls noch nicht vorhanden

# Alembic-Konfiguration initialisieren
alembic_cfg = Config("alembic.ini")

# Migration durchführen
def run_migrations():
    try:
        # Migration erstellen
        command.revision(alembic_cfg, message="Add age column to user", autogenerate=True)
        # Migration anwenden
        command.upgrade(alembic_cfg, "head")
        print("Migration erfolgreich angewendet!")
    except Exception as e:
        print("Fehler bei der Migration.")
        print(e)

# Tabellen in der Datenbank erstellen (nur bei leerer Datenbank)
try:
    Base.metadata.create_all(engine)
    print("Tabelle 'users' erfolgreich erstellt!")
except Exception as e:
    print("Fehler beim Erstellen der Tabelle.")
    print(e)

# Verbindung und Sitzung einrichten, um die Datenbank weiter zu testen
Session = sessionmaker(bind=engine)
session = Session()

# Beispiel-Datensatz einfügen
try:
    new_user = User(name="John Doe", email="john.doe@example.com", age=30)  # Hier fügen wir den 'age'-Wert hinzu
    session.add(new_user)
    session.commit()
    print("Benutzer erfolgreich hinzugefügt!")
except Exception as e:
    print("Fehler beim Einfügen des Benutzers.")
    print(e)
finally:
    session.close()

# Migrationen anwenden
run_migrations()
