CREATE DATABASE IF NOT EXISTS siec_kin;

USE siec_kin;

CREATE TABLE IF NOT EXISTS filmy (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tytul VARCHAR(255) NOT NULL,
    gatunek VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS kina (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nazwa VARCHAR(255) NOT NULL,
    miasto VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS seanse (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_filmu INT,
    id_kina INT,
    data_seansu DATE,
    godzina_seansu TIME,
    FOREIGN KEY (id_filmu) REFERENCES filmy(id),
    FOREIGN KEY (id_kina) REFERENCES kina(id)
);

CREATE TABLE IF NOT EXISTS bilety (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_seansu INT,
    cena DECIMAL(8, 2),
    ilosc_miejsc INT,
    FOREIGN KEY (id_seansu) REFERENCES seanse(id)
);
