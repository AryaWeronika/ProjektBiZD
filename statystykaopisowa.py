import pandas as pd
import mysql.connector
from datetime import datetime

# Połączenie z bazą danych
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    database="siec_kin"
)

cursor = conn.cursor()

# Funkcja do pobierania danych i wyświetlania statystyki opisowej
def get_and_display_statistics(table_name):
    # Pobranie danych z bazy danych
    select_query = f"SELECT * FROM {table_name}"
    cursor.execute(select_query)

    # Pobranie wyników zapytania do ramki danych (DataFrame)
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=columns)

    # Statystyka opisowa
    statistics = df.describe()

    # Wyświetlenie statystyki opisowej
    print(f"\nStatystyka opisowa {table_name}:")
    print(statistics)

# Pobierz i wyświetl statystykę dla tabeli "bilety"
get_and_display_statistics("bilety")

# Pobierz i wyświetl statystykę dla tabeli "seanse"
get_and_display_statistics("seanse")

# Pobierz i wyświetl statystykę dla tabeli "kina"
get_and_display_statistics("kina")

# Pobierz i wyświetl statystykę dla tabeli "filmy"
get_and_display_statistics("filmy")

# Zamknięcie połączenia
cursor.close()
conn.close()