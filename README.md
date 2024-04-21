Koirapuistot

21.4.2024 Arviointia varten:

Tämänhetkinen tilanne:

- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen. OK
- Käyttäjä näkee koirapuistot kartalla ja voi painaa puiston kohdalta, jolloin siitä näytetään lisää tietoa. OK
- Käyttäjä voi antaa arvion (tähdet ja kommentti) koirapuistosta ja lukea muiden antamia arvioita. OK
- Ylläpitäjä voi lisätä ja poistaa puistoja sekä määrittää niistä näytettävät tiedot. EI TEHTY
- Käyttäjä voi etsiä koirapuistoja sijainnin tai ominaisuuksien perusteella. OK
- Käyttäjä näkee myös listan, jossa koirapuistot on järjestetty parhaimmasta huonoimpaan arvioiden mukaisesti. OK
- Ylläpitäjä voi tarvittaessa poistaa käyttäjän antaman arvion. EI TEHTY
- Ylläpitäjä voi luoda ryhmiä, joihin koirapuistoja voi luokitella. Puisto voi kuulua yhteen tai useampaan ryhmään. OK

Ylläpitäjän rooliin liittyviä toimintoja puuttuu yhä. Niitä työstän vielä.
Ulkoasu on myös keskeneräinen, vaikka siihen onkin tehty jo joitain elementtejä. Ulkoasu muualla kuin etusivulla on erityisen kömpelö, sitä tulen korjaamaan.
Virheilmoituksia pitää vielä hioa, suurin osa toimii kuitenkin nyt.
Yleistä koodin siistimistä ja refaktorointia on vielä.
Sovellus on testattavissa paikallisesti, alla ohjeet:

Ohjeet:

Kloonaa tämä repositorio omalle koneellesi ja siirry sen juurikansioon. Luo kansioon .env-tiedosto ja määritä sen sisältö seuraavanlaiseksi:

DATABASE_URL=<tietokannan-paikallinen-osoite>
SECRET_KEY=<salainen-avain>

Seuraavaksi aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla

$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r ./requirements.txt

Määritä vielä tietokannan skeema komennolla

$ psql < schema.sql

Nyt voit käynnistää sovelluksen komennolla

$ flask run


7.4.2024 Vertaisarviointia varten:
- Sovellus on hyvin alustavassa vaiheessa. Olen työstänyt kirjautumista ja rekisteröintiä, karttaa, hakutoimintoa, sekä arviointia. Näissä on kuitenkin vielä puutteita, esim. ohjaaminen takaisin kirjautumiseen silloin kun kirjautuminen vaaditaan ja paljon muita kömpelyyksiä
- Ylläpitäjän rooliin liittyvät toiminnot puuttuvat kokonaan. Samoin puistojen listaus arviointien mukaan. Ryhmiin liittyviä ominaisuuksia ei ole vielä tehty. Ulkoasua ei ole tehty. Tietoturva-asiat ovat kesken: syötteiden tarkistamista sekä sql-injektioita ja xss-/csrf-haavoittuvuuksia ei ole otettu vielä huomioon. Töitä siis vielä riittää rutkasti.
- Sovellus on tällä hetkellä testattavissa vain paikallisesti.


Suunnitelma:

Sovelluksessa näkyy Helsingin kantakaupungin koirapuistot. Sovelluksen avulla voi etsiä tietoa puistoista ja lukea arvioita.
Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.

- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- Käyttäjä näkee koirapuistot kartalla ja voi painaa puiston kohdalta, jolloin siitä näytetään lisää tietoa.
- Käyttäjä voi antaa arvion (tähdet ja kommentti) koirapuistosta ja lukea muiden antamia arvioita.
- Ylläpitäjä voi lisätä ja poistaa puistoja sekä määrittää niistä näytettävät tiedot.
- Käyttäjä voi etsiä koirapuistoja sijainnin tai ominaisuuksien perusteella.
- Käyttäjä näkee myös listan, jossa koirapuistot on järjestetty parhaimmasta huonoimpaan arvioiden mukaisesti.
- Ylläpitäjä voi tarvittaessa poistaa käyttäjän antaman arvion.
- Ylläpitäjä voi luoda ryhmiä, joihin koirapuistoja voi luokitella. Puisto voi kuulua yhteen tai useampaan ryhmään.
