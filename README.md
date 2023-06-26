# Konferencja

Projekt zaliczeniowy na zajęcia Podstawy Baz Danych. Projekt ma na celu przygotowanie bazy danych dla konferencji naukowej dla fizyków. W projekcie znajdują się takie funckje jak: rejestracja, logowanie, dodawania prezentacji, edycja prezentacji (jeżeli jest się autorem), rezerwacja pokoi hotelowych, obliczanie kosztów konferencji oraz dla administratora dodatkowo możliwość usuwania uczestników z bazy danych oraz ich edycja.

W projekcie wykorzystano technologie:
* PostgreSQL
* SQLAlchemy
* Flask
* Docker

W projekcie wykorzystano dodatkowe zadania bazy danych, takie jak:
* stworzenie funkcji
* stworzenie triggerów
* analityka (GROUP BY, ORDER BY, OUTER JOIN) z wykorzystaniem ORM

W celu inicjalizacji projektu, należy w folderze głównym wykonać komendę 

```shell
docker-compose up
```

Baza danych powinna zawierać przykładowe dane. Aby uzyskać dostęp do panelu administratora, statystki, należy stworzyć użytkownika korzystając z: <br>
adresu email: admin@admin.pl <br>
hasło dowolne.


oraz zalogować się. 
