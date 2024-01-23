from matplotlib.widgets import Lasso
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import mysql.connector
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

# Połączenie z bazą danych
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    database="siec_kin"
)
cursor = conn.cursor()

# Nazwa twojej tabeli
table_name = 'bilety'

# Pobranie danych z bazy danych
select_query = f"SELECT cena, ilosc_miejsc FROM {table_name}"
try:
    cursor.execute(select_query)
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=columns)

    # Zamknięcie połączenia z bazą danych
    cursor.close()
    conn.close()

    # Podział danych na zestaw treningowy i testowy
    X_train, X_test, y_train, y_test = train_test_split(df[['cena']], df['ilosc_miejsc'], test_size=0.2, random_state=42)

    # Regresja liniowa
    model_linear = LinearRegression()
    model_linear.fit(X_train, y_train)
    y_pred_linear = model_linear.predict(X_test)

    # Regresja wielomianowa
    degree = 2  # Stopień wielomianu
    model_poly = make_pipeline(PolynomialFeatures(degree), LinearRegression())
    model_poly.fit(X_train, y_train)
    y_pred_poly = model_poly.predict(X_test)

    # Regresja grzbietowa (Ridge)
    alpha_ridge = 1.0  # Parametr regularyzacji
    model_ridge = Ridge(alpha=alpha_ridge)
    model_ridge.fit(X_train, y_train)
    y_pred_ridge = model_ridge.predict(X_test)

    # Regresja logistyczna (przykładowo - wymaga dostosowania do problemu)
    model_logistic = LogisticRegression()
    model_logistic.fit(X_train, (y_train > y_train.median()).astype(int))
    y_pred_logistic = model_logistic.predict(X_test)

    # Wyświetlenie wyników
    print("Regresja liniowa - MSE:", mean_squared_error(y_test, y_pred_linear))
    print("Regresja wielomianowa - MSE:", mean_squared_error(y_test, y_pred_poly))
    print("Regresja grzbietowa (Ridge) - MSE:", mean_squared_error(y_test, y_pred_ridge))
    print("Regresja logistyczna - MSE:", mean_squared_error(y_test, y_pred_logistic))

    # Wykres regresji liniowej
    plt.scatter(X_train, y_train, color='blue', label='Dane treningowe')
    plt.scatter(X_test, y_test, color='red', label='Dane testowe')
    plt.plot(X_test, y_pred_linear, color='green', linewidth=2, label='Regresja liniowa')
    plt.xlabel('cena')
    plt.ylabel('ilosc_miejsc')
    plt.title('Regresja Liniowa')
    plt.legend()
    plt.show()
    
    # Wykres regresji wielomianowej
    plt.scatter(X_train, y_train, color='blue', label='Dane treningowe')
    plt.scatter(X_test, y_test, color='red', label='Dane testowe')
    plt.plot(X_test, y_pred_poly, color='orange', linewidth=2, label=f'Regresja wielomianowa (stopień {degree})')
    plt.xlabel('cena')
    plt.ylabel('ilosc_miejsc')
    plt.title(f'Regresja Wielomianowa (stopień {degree})')
    plt.legend()
    plt.show()
    
    # Wykres regresji grzbietowej (Ridge)
    plt.scatter(X_train, y_train, color='blue', label='Dane treningowe')
    plt.scatter(X_test, y_test, color='red', label='Dane testowe')
    plt.plot(X_test, y_pred_ridge, color='purple', linewidth=2, label='Regresja grzbietowa (Ridge)')
    plt.xlabel('cena')
    plt.ylabel('ilosc_miejsc')
    plt.title('Regresja Grzbietowa (Ridge)')
    plt.legend()
    plt.show()
    
    # Wykres regresji logistycznej
    plt.scatter(X_train, y_train, color='blue', label='Dane treningowe')
    plt.scatter(X_test, y_test, color='red', label='Dane testowe')
    plt.plot(X_test, y_pred_logistic, color='cyan', linewidth=2, label='Regresja logistyczna')
    plt.xlabel('cena')
    plt.ylabel('ilosc_miejsc')
    plt.title('Regresja Logistyczna')
    plt.legend()
    plt.show()

except mysql.connector.Error as err:
    print(f"Błąd w trakcie wykonywania zapytania: {err}")
    cursor.close()
    conn.close()