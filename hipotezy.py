import pandas as pd
import mysql.connector
from datetime import datetime
from scipy import stats
import numpy as np

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
    print(f"\nStatystyka opisowa {table_name}:\n{statistics}")

    # Test normalności rozkładu dla wszystkich zmiennych
    print(f"\nTest normalności rozkładu {table_name}:")

    for column in df.columns:
        if "id" in column.lower():
            print(f"    {column}: Pominięto - kolumna z identyfikatorem.")
            continue
        # Konwersja kolumny do liczbowego typu danych (pominięcie, jeśli nie jest to możliwe)
        try:
            df[column] = pd.to_numeric(df[column])
        except:
            pass

        # Test normalności tylko dla kolumn liczbowych
        if np.issubdtype(df[column].dtype, np.number):
            shapiro_stat, shapiro_p_value = stats.shapiro(df[column])
            print(f"{column} - Shapiro-Wilk Statistic: {shapiro_stat:.4f}, P-value: {shapiro_p_value:.4f}")
            if shapiro_p_value < 0.05:
                print(f"    {column}: Wartości nie pochodzą z rozkładu normalnego.")
            else:
                print(f"    {column}: Wartości pochodzą z rozkładu normalnego.")
        else:
            print(f"    {column}: Pominięto - nie jest to kolumna liczbowa.")

    # Test równości wariancji
    print(f"\nTest równości wariancji {table_name}:")
    try:
        levene_stat, levene_p_value = stats.levene(*[df[col] for col in df.columns if np.issubdtype(df[col].dtype, np.number)])
        print(f"Levene Statistic: {levene_stat:.4f}, P-value: {levene_p_value:.4f}")
        if levene_p_value < 0.05:
            print("Istnieje przynajmniej jedna różnica w wariancjach.")
        else:
            print("Wariancje są równe.")
    except Exception as e:
        print(f"Błąd przy teście równości wariancji: {str(e)}")
        
    # Testy dla zmiennych zależnych (sparowanych)
    print(f"\nTesty dla zmiennych zależnych (sparowanych) {table_name}:")
    paired_t_stat, paired_t_p_value = stats.ttest_rel(df['cena'], df['ilosc_miejsc'])
    print(f"T-Statistic: {paired_t_stat:.4f}, P-value: {paired_t_p_value:.4f}")
    if paired_t_p_value < 0.05:
        print("Średnie są różne.")
    else:
        print("Średnie są równe.")

    # Testy dla zmiennych niezależnych
    print(f"\nTesty dla zmiennych niezależnych {table_name}:")
    independent_t_stat, independent_t_p_value = stats.ttest_ind(df['cena'], df['ilosc_miejsc'])
    print(f"T-Statistic: {independent_t_stat:.4f}, P-value: {independent_t_p_value:.4f}")
    if independent_t_p_value < 0.05:
        print("Średnie są różne.")
    else:
        print("Średnie są równe.")

    # Test ANOVA (analiza wariancji) dla wielu średnich
    print(f"\nTest ANOVA dla wielu średnich {table_name}:")
    anova_stat, anova_p_value = stats.f_oneway(df['cena'], df['ilosc_miejsc'])
    print(f"F-Statistic: {anova_stat:.4f}, P-value: {anova_p_value:.4f}")
    if anova_p_value < 0.05:
        print("Przynajmniej jedna grupa ma inną średnią.")
    else:
        print("Średnie są równe.")

get_and_display_statistics("bilety")

# Zamknięcie połączenia
cursor.close()
conn.close()
