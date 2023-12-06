--Manualní přidání typu účtů
INSERT INTO Typ_uctu (typ_uctu_id,typ_uctu_nazev) VALUES (1,'Dispečer');
INSERT INTO Typ_uctu (typ_uctu_id,typ_uctu_nazev) VALUES (2,'Technik');
INSERT INTO Typ_uctu (typ_uctu_id,typ_uctu_nazev) VALUES (3,'Zákazník');

--Manualní přidání účtů Dispečer,Technik, Zákazník pro test
INSERT INTO Ucet (ucet_id, ucet_jmeno, ucet_heslo, ucet_email, typ_uctu_id) VALUES (1, 'John_Dispecer', 'dispecer123', 'john.dispecer@example.com', 1);
INSERT INTO Ucet (ucet_id, ucet_jmeno, ucet_heslo, ucet_email, typ_uctu_id) VALUES (2, 'Jane_Technik', 'technik123', 'jane.technik@example.com', 2);
INSERT INTO Ucet (ucet_id, ucet_jmeno, ucet_heslo, ucet_email, typ_uctu_id) VALUES (3, 'Bob_Zakaznik', 'zakaznik123', 'bob.zakaznik@example.com', 3);


--TEST
INSERT INTO Typ_stroje (typ_stroje_id, typ_stroje_nazev) VALUES (1,'Kombajn');
INSERT INTO Typ_stroje (typ_stroje_id, typ_stroje_nazev) VALUES (2,'Sekačka');

INSERT INTO Stroj (stroj_id, stroj_nazev, stroj_cena, typ_stroje_id) VALUES (1,'John Deere S 685 i',50000,1);
INSERT INTO Stroj (stroj_id, stroj_nazev, stroj_cena, typ_stroje_id) VALUES (2,'Case IH CT 5080',20000,1);
INSERT INTO Stroj (stroj_id, stroj_nazev, stroj_cena, typ_stroje_id) VALUES (3,'CLAAS Lexion 770 TT',45000,1);

INSERT INTO Stroj (stroj_id, stroj_nazev, stroj_cena, typ_stroje_id) VALUES (4,'Husqvarna P535HX',5000,2);
INSERT INTO Stroj (stroj_id, stroj_nazev, stroj_cena, typ_stroje_id) VALUES (5,'Cub Cadet Z9 183id ZeroTurn',2500,2);
INSERT INTO Stroj (stroj_id, stroj_nazev, stroj_cena, typ_stroje_id) VALUES (6,'AL-KO Rider Solo R7-63.8 A 127486',500,2);