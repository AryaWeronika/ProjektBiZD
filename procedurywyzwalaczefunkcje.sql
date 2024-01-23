USE siec_kin;
-- Procedura do dodawania nowego filmu:
DELIMITER //
CREATE PROCEDURE DodajFilm (IN tytul_param VARCHAR(255), IN gatunek_param VARCHAR(255))
BEGIN
    INSERT INTO filmy (tytul, gatunek) VALUES (tytul_param, gatunek_param);
END //
DELIMITER ;

-- Procedura do usuwania filmu:
DELIMITER //
CREATE PROCEDURE UsunFilm (IN film_id INT)
BEGIN
    INSERT INTO filmy_archiwum (tytul, gatunek, status)
    SELECT tytul, gatunek, 'usuniety' FROM filmy WHERE id = film_id;

    DELETE FROM filmy WHERE id = film_id;
END //
DELIMITER ;

-- Procedura do aktualizacji filmu:
DELIMITER //
CREATE PROCEDURE AktualizujFilm (IN film_id INT, IN nowy_tytul VARCHAR(255), IN nowy_gatunek VARCHAR(255))
BEGIN
    UPDATE filmy SET tytul = nowy_tytul, gatunek = nowy_gatunek WHERE id = film_id;
END //
DELIMITER ;

-- Stworzenie tabeli do archiwum
CREATE TABLE IF NOT EXISTS filmy_archiwum (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tytul VARCHAR(255) NOT NULL,
    gatunek VARCHAR(255),
    status ENUM('usuniety') NOT NULL DEFAULT 'usuniety',
    data_archiwizacji TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Wyzwalacz do automatycznego przenoszenia do archiwum:
DELIMITER //
CREATE TRIGGER PrzeniesDoArchiwum 
BEFORE DELETE ON filmy 
FOR EACH ROW 
BEGIN 
    DECLARE film_status VARCHAR(255);

    SELECT status INTO film_status FROM filmy WHERE id = OLD.id;

    IF film_status IS NOT NULL AND film_status <> 'usuniety' THEN
        INSERT INTO filmy_archiwum (tytul, gatunek, status, data_archiwizacji) 
        VALUES (OLD.tytul, OLD.gatunek, 'usuniety', NOW());
    END IF;
END;
//
DELIMITER ;

-- Tworzenie tabeli logów
CREATE TABLE IF NOT EXISTS logi (
    id INT AUTO_INCREMENT PRIMARY KEY,
    typ_logu VARCHAR(255),
    komunikat TEXT,
    data_logowania TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Procedura do logowania informacji
DELIMITER //
CREATE PROCEDURE LogujInformacje (IN typ_logu_param VARCHAR(255), IN komunikat_param TEXT)
BEGIN
    INSERT INTO logi (typ_logu, komunikat) VALUES (typ_logu_param, komunikat_param);
END //
DELIMITER ;

-- Procedura z obsługą wyjątków
DELIMITER //
CREATE PROCEDURE wyjatki(IN x INT)
BEGIN
    DECLARE custom_error CONDITION FOR SQLSTATE '45000';
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
    BEGIN
        -- Obsługa wyjątku ogólnego SQL
        INSERT INTO logi (typ_logu, komunikat) VALUES ('BŁĄD', 'Wystąpił ogólny błąd SQL.');
    END;
    DECLARE CONTINUE HANDLER FOR NOT FOUND
    BEGIN
        -- Obsługa braku wyników (np. w przypadku SELECT)
        INSERT INTO logi (typ_logu, komunikat) VALUES ('INFORMACJA', 'Brak wyników.');
    END;
    DECLARE CONTINUE HANDLER FOR custom_error
    BEGIN
        -- Obsługa własnego wyjątku
        INSERT INTO logi (typ_logu, komunikat) VALUES ('BŁĄD', 'Wystąpił własny błąd.');
    END;

    IF x < 0 THEN
        SIGNAL custom_error SET MESSAGE_TEXT = 'Wartość x nie może być ujemna.';
    ELSE
        SELECT 1 / x;
    END IF;
END //
DELIMITER ;

SET GLOBAL log_bin_trust_function_creators = 1;

-- Poprawiona funkcja z przypisaniem domyślnej wartości przed deklaracją zmiennej
DELIMITER //

CREATE FUNCTION DodajLiczby(a INT, b INT)
RETURNS INT
BEGIN
    DECLARE wynik INT;
    SET b = IFNULL(b, 0);
    SET wynik = a + b;
    RETURN wynik;
END //

DELIMITER ;

-- Funkcja sprawdzająca poprawność formatu daty
DELIMITER //
CREATE FUNCTION SprawdzFormatDaty(data_param VARCHAR(10))
RETURNS BOOLEAN
BEGIN
    DECLARE valid BOOLEAN DEFAULT TRUE;
    -- Sprawdzenie, czy data_param ma poprawny format daty (przykładowy format: 'YYYY-MM-DD')
    IF NOT REGEXP_LIKE(data_param, '^[0-9]{4}-[0-9]{2}-[0-9]{2}$') THEN
        SET valid = FALSE;
    END IF;
    RETURN valid;
END //
DELIMITER ;










