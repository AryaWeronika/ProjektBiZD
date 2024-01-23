import csv
import mysql.connector
import shutil
from datetime import datetime
import os

# Połączenie z bazą danych
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    database="siec_kin"
)

cursor = conn.cursor()

def load_data_from_csv(file_path, encoding='utf-8'):
    with open(file_path, 'r', encoding=encoding) as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        return [tuple(row) for row in csv_reader]

def insert_data(table_name, columns, data):
    placeholders = ", ".join(["%s"] * len(columns))
    query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
    try:
        cursor.executemany(query, data)
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()

def validate_data(data, expected_columns):
    for row in data:
        if len(row) != len(expected_columns):
            print("Error: Incorrect number of columns in data.")
            return False
    return True

def archive_data(file_path, backup_folder):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_file_path = f"{backup_folder}/backup_{timestamp}_{file_path}"

    # Sprawdzenie, czy katalog istnieje, a jeśli nie, utworzenie go
    os.makedirs(backup_folder, exist_ok=True)

    shutil.copy(file_path, backup_file_path)
    print(f"Archived {file_path} to {backup_file_path}")

filmy_data = load_data_from_csv('filmy.csv', encoding='ISO-8859-1')
kina_data = load_data_from_csv('kina.csv', encoding='ISO-8859-1')
seanse_data = load_data_from_csv('seanse.csv', encoding='ISO-8859-1')
bilety_data = load_data_from_csv('bilety.csv', encoding='ISO-8859-1')

# Walidacja danych przed wstawieniem do bazy
if validate_data(kina_data, ["nazwa", "miasto"]) and validate_data(filmy_data, ["tytul", "gatunek"]) and \
   validate_data(seanse_data, ["id_filmu", "id_kina", "data_seansu", "godzina_seansu"]) and \
   validate_data(bilety_data, ["id_seansu", "cena", "ilosc_miejsc"]):

    insert_data("kina", ["nazwa", "miasto"], kina_data)
    insert_data("filmy", ["tytul", "gatunek"], filmy_data)
    insert_data("seanse", ["id_filmu", "id_kina", "data_seansu", "godzina_seansu"], seanse_data)
    insert_data("bilety", ["id_seansu", "cena", "ilosc_miejsc"], bilety_data)

    # Archiwizacja przetworzonych danych
    archive_data('kina.csv', 'backup_folder')
    archive_data('filmy.csv', 'backup_folder')
    archive_data('seanse.csv', 'backup_folder')
    archive_data('bilety.csv', 'backup_folder')

cursor.close()
conn.close()