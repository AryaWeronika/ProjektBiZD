DELIMITER //

CREATE PROCEDURE ZestawienieMiesieczneWszystkie()
BEGIN
    SELECT YEAR(data_seansu) AS rok,
           MONTH(data_seansu) AS miesiac,
           COUNT(*) AS ilosc_seansow
    FROM seanse
    GROUP BY YEAR(data_seansu), MONTH(data_seansu)
    ORDER BY YEAR(data_seansu), MONTH(data_seansu);
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE ZestawienieKwartalneWszystkie()
BEGIN
    SELECT YEAR(data_seansu) AS rok,
           QUARTER(data_seansu) AS kwartal,
           COUNT(*) AS ilosc_seansow
    FROM seanse
    GROUP BY YEAR(data_seansu), QUARTER(data_seansu)
    ORDER BY YEAR(data_seansu), QUARTER(data_seansu);
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE ZestawienieRoczneWszystkie()
BEGIN
    SELECT YEAR(data_seansu) AS rok,
           COUNT(*) AS ilosc_seansow
    FROM seanse
    GROUP BY YEAR(data_seansu)
    ORDER BY YEAR(data_seansu);
END //

DELIMITER ;





