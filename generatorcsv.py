import csv
import random
from datetime import datetime, timedelta

# Wczytywanie danych z pliku mymoviedb.csv
def load_movie_data_from_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        return [row for row in csv_reader]
    
# Generator danych o filmach
def generate_filmy_data(num_records, movie_db_path='mymoviedb.csv'):
    movie_data = load_movie_data_from_csv(movie_db_path)
    data = []
    for _ in range(num_records):
        movie = random.choice(movie_data)
        tytul = movie['Title']
        gatunek = movie['Genre']
        data.append((tytul, gatunek))
    return data

# Generator danych o kinach
nazwy_kin = ["Multikino", "Cinema City", "Helios", "IMAX", "Silver Screen"]
miasta = ["Warszawa", "Krakow", "Lodz", "Poznan", "Wroclaw"]
def generate_kina_data(num_records):
    data = []
    for _ in range(num_records):
        nazwa = random.choice(nazwy_kin)
        miasto = random.choice(miasta)
        data.append((nazwa, miasto, ))
    return data

# Generator danych o seansach
def generate_seanse_data(filmy_data, kina_data, num_records):
    data = []
    for _ in range(num_records):
        id_filmu = random.randint(1, len(filmy_data))  # Losowy identyfikator filmu
        id_kina = random.randint(1, len(kina_data))
        data_seansu = (datetime.now() + timedelta(days=random.randint(-30, 30))).strftime('%Y-%m-%d')
        godzina_seansu = f"{random.randint(10, 22)}:{random.choice(['00', '15', '30', '45'])}"
        data.append((id_filmu, id_kina, data_seansu, godzina_seansu))
    return data


# Generator danych o sprzedaży biletów
def generate_bilety_data(seans_data, num_records):
    data = []
    for _ in range(num_records):
        id_seansu = random.randint(1, len(seans_data))
        cena = round(random.uniform(10, 25), 2)
        ilosc_miejsc = random.randint(50, 150)
        data.append((id_seansu, cena, ilosc_miejsc))
    return data


# Zapis danych do plików CSV
def save_to_csv(data, file_name):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows([data[0]])  # Zapis nagłówka jako listy
        writer.writerows(data[1:])   # Pozostałe dane

# Wygenerowanie danych
filmy_data = generate_filmy_data(num_records=800)
kino_data = generate_kina_data(num_records=800)
seans_data = generate_seanse_data(filmy_data,kino_data,num_records=800)
bilety_data = generate_bilety_data(seans_data, num_records=800)

# Zapis danych do plików CSV
save_to_csv(filmy_data, 'filmy.csv')
save_to_csv(kino_data, 'kina.csv')
save_to_csv(seans_data, 'seanse.csv')
save_to_csv(bilety_data, 'bilety.csv')