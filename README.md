# InteraktTöri app

Az InteraktTöri egy webalkalmazás, amely a történelemoktatást hivatot segíteni.
Az alkalmazás adatvizualizációs eszközök segítségével mutatja be a feldolgozott témát (a Római Birodalom). Az alkalmazás térkép oldala interaktívan mutatja be 
a Római Birodalom területi változásait és az témához kapcsolódó, időben egymás után következő történelmi eseményeket.
Az alkalmazás tesztek oldalai pedig lehetővé teszik a témában megszerzett tudás ellenőrzését, gyakorlását.  
Az alkalmazás az "Adatvizualizáció a történelemoktatásban" című szakdolgozatom keretében készült.

## Az alklamazás telepítése és futtatása

### Windows környezetben
1.	Virtuális környezet készítése	`python -m venv interakt_tori_venv`
2.	Virtuális környezet elindítása	`interakt_tori_venv\Scripts\activate`
3.	Alkalmazás letöltése	`git clone https://github.com/nineno98/InteraktTori.git`
4.	Szükséges függőségek telepítése	`cd ancient_interactive pip install -r requirements.txt`
5.	Alkalmazás futtatása	`python manage.py runserver`
6.	Megnyitás a böngészőben	`http://127.0.0.1:8000/`

### Linux környezetben
1.	Virtuális környezet készítése	`python3 -m venv interakt_tori_venv`
2.	Virtuális környezet elindítása	`source interakt_tori_venv/bin/activate`
3.	Alkalmazás letöltése	`git clone https://github.com/nineno98/InteraktTori.git`
4.	Szükséges függőségek telepítése	`cd ancient_interactive pip install -r requirements.txt`
5.	Alkalmazás futtatása	`python3 manage.py runserver`
6.	Megnyitás a böngészőben	`http://127.0.0.1:8000/`
