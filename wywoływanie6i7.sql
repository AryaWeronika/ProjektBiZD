CALL DodajFilm('Titanic', 'Drama');
CALL UsunFilm(800);
CALL AktualizujFilm(801,'Titanic2', 'Drama2');

UPDATE seanse SET id_filmu = NULL WHERE id_filmu = 796;
CALL UsunFilm(796);

CALL LogujInformacje('INFORMACJA', 'Pomyślnie dodano nowy film.');

CALL Wyjatki(5);
CALL Wyjatki(-5);
CALL Wyjatki(0);
SELECT * FROM logi;


SELECT DodajLiczby(5, 3);
SELECT DodajLiczby(5,0);    

SELECT SprawdzFormatDaty('2022-01-31'); 
SELECT SprawdzFormatDaty('31-01-2022'); 

