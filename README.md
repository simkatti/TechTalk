# TechTalk

TechTalk on redditin/jodelin tyylinen keskustleualusta erityisesti tietojenkäsittelytieteiden jäsenille.
Käyttäjä voi:
- luoda uuden käyttäjän
- kirjautua sisään ja ulos
- kirjauduttuaan sisään nähdä eri huoneita(kanavia) eri kategorioista
- aloittaa uuden keskustelun
- luoda uuden huoneen
- vastata jo olemassa oleviin keskusteluihin
- nähdä kirjoitetut viestit ja aloitetut keskustelut
- hakea keskusteluja ja viestejä hakusanoilla
- poistaa lähettämiä viestejä.

Sovelluksen kaikki funktiot toimii. Kirjauduttasi sisään/luotuasi käyttäjätunnuksen etusivulla näkyy eri huoneita kategorioittain. Klikatessasi mielestä huonetta näet huoneessa olevat keskustelut. Voit luoda uusia huoneita, viestiketjuja sekä vastata jo olemassa oleviin viestiketjuihin. Voit myös poistaa lähettämäsi viestit. Kun viestiketjussa ei ole enää viestejä, chätti poistuu tietokannasta eikä sitä enää lyödy.

Sovellus ei ole testattavissa tuotannossa. requirements.txt ja schema.sql ovat ajan tasalla. Lisää tietokantaan myös datacontent.sql mukaiset taulukot täyden käyttökokemuksen takaamiseksi.  

## TESTAUS:
- avaa terminaali
- mene kansioon johon haluat kloonata repon
- kloonaa repo
- Luo .env:
  - DATABASE_URL=postgresql:///(tietokannan-nimi)
  - SECRET_KEY=(salainen avain)
-Terminaalissa:
  - $ `python3 -m venv venv`
  - $ `source venv/bin/activate`
  - $ `pip install -r ./requirements.txt`
  - aktivoi tietokanta `start-pg.sh`
  - $ `psql`
  - user=# `CREATE DATABASE (tietokannan nimi);`
  - $ `psql -d (tietokannan nimi) < schema.sql`
  - $ `psql -d (tietokannan nimi) < datacontent.sql`
