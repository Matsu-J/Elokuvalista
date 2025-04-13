# Elokuvalista

Sovelluksen idea on olla lista, johon käyttäjät voivat lisätä elokuvia joita he ovat katsoneet tai haluavat katsoa. Käyttäjät voivat arvostella elokuvat ateikolla 0-10. Lisäksi elokvat voi järjestää muun muassa aakkosjärjestyksessä, pituuden, julkaisuvuoden tai arvosanan mukaisessa järjestyksessä.

## Sovelluksen toimintojen tilanne:

  ✅ Käyttäjä voi luoda tilin ja kirjautua sisään
  
  ✅ Käyttäjä voi lisätä elokuvan katsomislistalle
  
  ✅ Käyttäjä voi muokata katsomislistaansa

  ✅ Käyttäjä voi lajitella elokuvat julkaisuvuoden mukaan

  ✅ Käyttäjä voi lajitella elokuvat pituuden mukaan

  ❌ Käyttäjä voi merkitä elokuvan katsotuksi
  
  ❌ Käyttäjä voi lajitella elokuvat katsottuihin ja ei katsottuihin
  
  ❌ Käyttäjä voi lajitella elokuvat arvosanan mukaan
  
  ❌ Käyttäjä voi arvostella elokuvia
  
  ❌ Käyttäjä voi kommentoida muiden listoilla olevia elokuvia
  
  ❌ Käyttäjä voi hakea elokuvia listaltaan
  


## Asennusohjeet:

Vaatimukset:
Python

Lataa koodi esimerkiksi git clone komennolla

```
git clone https://github.com/Matsu-J/Elokuvalista.git
```

Navigoi kansioon johon latasit koodin

Luo ja käynnistä virtuaaliympäristö

```
python3 -m venv venv

source venv/bin/activate
```

Asenna Flask-kirjasto

```
pip install flask
```

Luo sovelluksen tietokanta
```
sqlite3 database.db < schema.sql
```

Suorita sovellus komennolla
```
flask run
```
