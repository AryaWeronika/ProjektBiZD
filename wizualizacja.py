import mysql.connector
import matplotlib.pyplot as plt

def generate_bar_chart(labels, values, title, xlabel, ylabel, color):
    plt.figure()
    plt.bar(labels, values, color=color)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=45, ha='right')  
    plt.tight_layout()  
    plt.show()

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    database='siec_kin'
)
cursor = conn.cursor()

all_data = {}

# Zestawienie Miesięczne
cursor.callproc('ZestawienieMiesieczneWszystkie')
wyniki_miesieczne = cursor.stored_results()

miesiace = []
ilosci_seansow_miesieczne = []

for result in wyniki_miesieczne:
    for row in result.fetchall():
        miesiace.append(f'Miesiąc {row[1]} {row[0]}')
        ilosci_seansow_miesieczne.append(row[2])

all_data['ZestawienieMiesieczne'] = {'labels': miesiace, 'values': ilosci_seansow_miesieczne}

# Zestawienie Kwartalne
cursor.callproc('ZestawienieKwartalneWszystkie')
wyniki_kwartalne = cursor.stored_results()

kwartaly = []
ilosci_seansow_kwartalne = []

for result in wyniki_kwartalne:
    for row in result.fetchall():
        kwartaly.append(f'Kw. {row[1]} {row[0]}')
        ilosci_seansow_kwartalne.append(row[2])

all_data['ZestawienieKwartalne'] = {'labels': kwartaly, 'values': ilosci_seansow_kwartalne}

# Zestawienie Roczne
cursor.callproc('ZestawienieRoczneWszystkie')
wyniki_roczne = cursor.stored_results()

lata = []
ilosci_seansow_roczne = []

for result in wyniki_roczne:
    for row in result.fetchall():
        lata.append(f'Rok {row[0]}')
        ilosci_seansow_roczne.append(row[1])

all_data['ZestawienieRoczne'] = {'labels': lata, 'values': ilosci_seansow_roczne}

for key, data in all_data.items():
    generate_bar_chart(data['labels'], data['values'], f'Zestawienie {key}', 'Okres', 'Ilość seansów', 'lightblue')

cursor.close()
conn.close()
