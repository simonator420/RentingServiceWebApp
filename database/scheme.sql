Tec--Manualní přidání typu účtů
INSERT INTO Typ_uctu (typ_uctu_id,typ_uctu_nazev) VALUES (1,'Dispečer');
INSERT INTO Typ_uctu (typ_uctu_id,typ_uctu_nazev) VALUES (2,'Technik');
INSERT INTO Typ_uctu (typ_uctu_id,typ_uctu_nazev) VALUES (3,'Zákazník');

--Manualní přidání účtů Dispečer,Technik, Zákazník pro test
INSERT INTO Ucet (ucet_id, ucet_jmeno, ucet_heslo, ucet_email, typ_uctu_id) VALUES (1, 'John_Dispecer', 'dispecer123', 'john.dispecer@example.com', 1);
INSERT INTO Ucet (ucet_id, ucet_jmeno, ucet_heslo, ucet_email, typ_uctu_id) VALUES (2, 'Jane_Technik', 'technik123', 'jane.technik@example.com', 2);
INSERT INTO Ucet (ucet_id, ucet_jmeno, ucet_heslo, ucet_email, typ_uctu_id) VALUES (3, 'Bob_Zakaznik', 'zakaznik123', 'bob.zakaznik@example.com', 3);