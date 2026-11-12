# Frontend-arkkitehtuuri (Frontend Architecture)

## Sisällysluettelo

1. [Johdanto](#johdanto)
2. [Frontend on rajapinnan asiakas](#frontend-on-rajapinnan-asiakas)
3. [Frontendin kerrokset](#frontendin-kerrokset)
4. [API-client-kerros](#api-client-kerros)
5. [Tyypit ja DTO sopimuksena](#tyypit-ja-dto-sopimuksena)
6. [Hook: palvelimen tila yhdessä paikassa](#hook-palvelimen-tila-yhdessä-paikassa)
7. [Komponentit: näyttävät ja kokoavat](#komponentit-näyttävät-ja-kokoavat)
8. [Kansiorakenne](#kansiorakenne)
9. [Missä säännöt asuvat?](#missä-säännöt-asuvat)
10. [Palvelimen tila ja käyttöliittymän tila](#palvelimen-tila-ja-käyttöliittymän-tila)
11. [Virheet ja lataustilat](#virheet-ja-lataustilat)
12. [Reaaliaikaisuus](#reaaliaikaisuus)
13. [Kehitysympäristö: proxy vai CORS](#kehitysympäristö-proxy-vai-cors)
14. [Best Practices](#best-practices)
15. [Anti-patterns](#anti-patterns)
16. [Yhteenveto](#yhteenveto)

---

## Johdanto

Backendissä arkkitehtuuri kertoo, mihin kerrokseen kukin koodirivi kuuluu. Selaimessa pyörivä sovellus tarvitsee saman vastauksen. Ilman sitä jokainen komponentti hakee datansa itse, sama osoite on kirjoitettu kymmeneen tiedostoon ja liiketoimintasääntö on kopioitu lomakkeeseen.

**Frontend-arkkitehtuuri** tarkoittaa sovittua jakoa: mikä tiedosto puhuu palvelimelle, mikä pitää tilaa ja mikä piirtää ruudun. Tavoitteet ovat samat kuin backendissä:

- muutos osuu yhteen paikkaan
- osia voi testata ja vaihtaa erikseen
- uusi kehittäjä tai tekoälyagentti löytää oikean tiedoston nimen perusteella

Tämän sivun esimerkit ovat Reactia ja TypeScriptiä, ja backend on ASP.NET Core Web API. Periaatteet ovat samat Vuessa, Angularissa ja Blazorissa.

**Microsoft:** [Choose between traditional web apps and single-page apps](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/choose-between-traditional-web-and-single-page-apps)

---

## Frontend on rajapinnan asiakas

Yhden sivun sovellus (SPA, Single Page Application) on oma ohjelmansa. Se ladataan selaimeen kerran, ja sen jälkeen se keskustelee backendin kanssa HTTP-rajapinnan kautta.

```
┌──────────────────────┐        HTTP + JSON         ┌──────────────────────────┐
│  Selain              │  ───────────────────────►  │  Backend                 │
│  React-sovellus      │   GET /api/v1/products     │  API → Application       │
│                      │  ◄───────────────────────  │        → Domain          │
│  näyttää ja kerää    │        DTO:t               │  säännöt ja tietokanta   │
└──────────────────────┘                            └──────────────────────────┘
```

[Clean Architecturen](Clean-Architecture.md) näkökulmasta frontend on kehän uloin osa. Se riippuu backendin rajapinnasta, mutta backend ei tiedä frontendistä mitään. Sama rajapinta palvelee yhtä hyvin mobiilisovellusta tai toista palvelua.

Tästä seuraa kaksi asiaa:

1. **Rajapinta on sopimus.** Frontend tuntee vain osoitteet ja [DTO:t](DTOs.md). Se ei tunne entiteettejä eikä tietokantaa.
2. **Backend ei luota frontendiin.** Kuka tahansa voi lähettää pyynnön ohi käyttöliittymän. Siksi säännöt tarkistetaan aina backendissä.

Rajapinnan perusteet: [Backend ja API](../WebAPI/Backend-and-API.md).

---

## Frontendin kerrokset

Hyvin jaetussa frontendissä on neljä kerrosta. Kutsut kulkevat ylhäältä alas, ja jokainen kerros tuntee vain seuraavan.

```
┌─────────────────────────────────────────────┐
│  Komponentit                                │  piirtävät ruudun, ottavat vastaan klikkaukset
├─────────────────────────────────────────────┤
│  Hookit / tila                              │  data, lataus, virhe ja uudelleenhaku
├─────────────────────────────────────────────┤
│  API-client (api/)                          │  yksi funktio per rajapinnan operaatio
├─────────────────────────────────────────────┤
│  HTTP-apuri (fetch)                         │  osoitteen alku, otsikot, virheen käsittely
└─────────────────────────────────────────────┘
                      │
                      ▼
                  Backend API
```

| Kerros | Vastuu | Ei saa tehdä |
|--------|--------|--------------|
| **Komponentti** | Näyttää datan ja välittää käyttäjän toiminnot | Kutsua `fetch`iä, tuntea osoitteita |
| **Hook** | Omistaa palvelimelta haetun tilan | Piirtää mitään, tuntea HTTP:n yksityiskohtia |
| **API-client** | Muuttaa funktiokutsun HTTP-pyynnöksi ja vastauksen tyypitetyksi olioksi | Pitää tilaa, näyttää virheitä |
| **HTTP-apuri** | Yhteinen pohja kaikille pyynnöille | Tuntea yksittäisiä osoitteita |

Vertaa backendin kerroksiin: controller ei kutsu tietokantaa suoraan, ja komponentti ei kutsu `fetch`iä suoraan. Ajatus on sama kuin [riippuvuuksien kääntämisessä](../Dependency-Injection.md): ylempi kerros tuntee tehtävän, ei toteutustapaa.

---

## API-client-kerros

API-client on frontendin vastine [repositorylle](../Patterns/Repository-Pattern.md). Se piilottaa sen, *miten* data haetaan.

### HTTP-apuri

Yksi tiedosto on ainoa paikka, jossa `fetch` esiintyy:

```ts
// api/http.ts
export class ApiError extends Error {
  readonly status: number;

  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

async function request(path: string, init?: RequestInit): Promise<Response> {
  const response = await fetch(`/api/v1${path}`, init);

  if (!response.ok) {
    const text = await response.text();
    throw new ApiError(response.status, text || `Pyyntö epäonnistui (${response.status}).`);
  }

  return response;
}

export async function getJson<T>(path: string): Promise<T> {
  const response = await request(path);
  return (await response.json()) as T;
}

export async function postJson(path: string, body: unknown): Promise<void> {
  await request(path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
}
```

Kun rajapinnan versio vaihtuu tai pyyntöihin lisätään kirjautumistunniste, muutos tehdään vain tähän tiedostoon.

### Yksi moduuli per resurssi

```ts
// api/productsApi.ts
import { getJson, postJson } from './http';
import type { Product } from '../types/product';

export const productsApi = {
  getAll: () => getJson<Product[]>('/products'),
  getById: (id: number) => getJson<Product>(`/products/${id}`),
  create: (name: string, price: number) => postJson('/products', { name, price }),
};
```

Muu sovellus kutsuu `productsApi.getAll()`. Se ei tiedä osoitetta, HTTP-metodia eikä sitä, että välissä on JSON.

---

## Tyypit ja DTO sopimuksena

Backend palauttaa [DTO:n](DTOs.md), ei entiteettiä. Frontendissä jokaista DTO:ta vastaa yksi TypeScript-tyyppi.

```csharp
// Backend
public record ProductDto(int Id, string Name, decimal Price, bool InStock);
```

```ts
// types/product.ts
export interface Product {
  id: number;
  name: string;
  price: number;
  inStock: boolean;
}
```

Huomaa kolme asiaa:

- ASP.NET Core muuttaa kenttien nimet JSONissa pienellä alkaviksi (`InStock` → `inStock`).
- Tyyppi määritellään **kerran**. Jos jokainen komponentti kirjoittaa oman versionsa, DTO:n muutos rikkoo sovelluksen hiljaa.
- TypeScript ei tarkista tyyppiä ajon aikana. `as T` on lupaus, ei tarkistus. Sopimus pysyy ajan tasalla, kun DTO ja tyyppi muutetaan samassa muutoksessa.

Isoissa projekteissa tyypit generoidaan backendin OpenAPI-kuvauksesta, jolloin ne eivät voi ajautua erilleen.

---

## Hook: palvelimen tila yhdessä paikassa

Palvelimelta haettuun dataan liittyy aina kolme tietoa: itse data, onko haku kesken ja epäonnistuiko se. Hook kokoaa ne yhteen.

```ts
// features/products/useProducts.ts
import { useCallback, useEffect, useState } from 'react';
import { productsApi } from '../../api/productsApi';
import type { Product } from '../../types/product';

export function useProducts() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const reload = useCallback(async () => {
    try {
      setProducts(await productsApi.getAll());
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Haku epäonnistui.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void reload();
  }, [reload]);

  return { products, loading, error, reload };
}
```

Hook palauttaa myös `reload`-funktion. Kun data muuttuu palvelimella, se haetaan uudestaan sen sijaan, että selain yrittäisi päivittää omaa kopiotaan.

---

## Komponentit: näyttävät ja kokoavat

Komponentteja on kahta lajia.

**Näyttävä komponentti** saa datan propseina ja piirtää sen. Se ei tiedä, mistä data tulee.

```tsx
// features/products/ProductList.tsx
import type { Product } from '../../types/product';

interface Props {
  products: Product[];
  loading: boolean;
  error: string | null;
}

export function ProductList({ products, loading, error }: Props) {
  if (loading) {
    return <p>Ladataan…</p>;
  }

  if (error) {
    return <p className="error">{error}</p>;
  }

  return (
    <ul>
      {products.map((product) => (
        <li key={product.id}>
          {product.name}: {product.price} €
        </li>
      ))}
    </ul>
  );
}
```

**Kokoava komponentti** (sivu) käyttää hookia ja välittää datan eteenpäin.

```tsx
// features/products/ProductsPage.tsx
import { ProductList } from './ProductList';
import { useProducts } from './useProducts';

export function ProductsPage() {
  const { products, loading, error } = useProducts();

  return <ProductList products={products} loading={loading} error={error} />;
}
```

Näyttävää komponenttia on helppo käyttää uudestaan ja testata, koska sille voi antaa minkä tahansa datan.

---

## Kansiorakenne

Tiedostot voi ryhmitellä kahdella tavalla.

**Tyypin mukaan:** kaikki komponentit yhdessä kansiossa, kaikki hookit toisessa. Toimii pienessä sovelluksessa.

```
src/
├── components/
├── hooks/
├── api/
└── types/
```

**Ominaisuuden mukaan (feature-kansiot):** yhteen asiaan liittyvät tiedostot ovat vierekkäin. Kun ominaisuus muuttuu, muutos pysyy yhdessä kansiossa.

```
src/
├── api/                  ← http.ts + yksi moduuli per resurssi
├── types/                ← DTO:ita vastaavat tyypit
├── features/
│   ├── products/         ← ProductsPage, ProductList, useProducts
│   └── orders/           ← OrdersPage, OrderForm, useOrders
├── components/           ← usean ominaisuuden yhteiset osat (Button, Modal)
├── App.tsx
└── main.tsx
```

Jako vastaa backendin feature-kansioita (`Features/Products/Queries`). Kun backendissä ja frontendissä on samat nimet, saman ominaisuuden koodi löytyy molemmista päistä samalla hakusanalla.

Laajempi vertailu: [React-projektin kansiorakenne](../../../../Development-guidelines/Frontend/React/React-project-file-and-folder-structure.md) (englanniksi). Projektin luonti: [React frontend template](../../../../Development-guidelines/Frontend/React/React-frontend-template.md).

---

## Missä säännöt asuvat?

Backend on ainoa paikka, jossa liiketoimintasääntö päätetään. Frontend voi tarkistaa syötteen, mutta vain käyttökokemuksen vuoksi.

| Tarkistus | Frontend | Backend |
|-----------|----------|---------|
| Kenttä ei ole tyhjä | ✅ Nopea palaute käyttäjälle | ✅ Aina |
| Hinta on positiivinen | ✅ Nopea palaute | ✅ Aina (domain) |
| Tuotetta on varastossa | ❌ Selain ei tiedä tuoretta tilaa | ✅ Aina |
| Käyttäjällä on oikeus | ❌ Painikkeen piilotus ei ole suojaus | ✅ Aina |

Nyrkkisääntö: **frontendin tarkistus säästää pyynnön, backendin tarkistus suojaa datan.** Jos frontendin tarkistuksen voi poistaa ilman, että data menee rikki, jako on oikea.

Kun backend hylkää pyynnön, frontend näyttää backendin viestin. Se ei arvaile syytä itse.

```tsx
try {
  await ordersApi.create(productId, quantity);
} catch (e) {
  // Esim. "Tuotetta ei ole varastossa."
  setError(e instanceof Error ? e.message : 'Tilaus epäonnistui.');
}
```

---

## Palvelimen tila ja käyttöliittymän tila

Frontendissä on kahdenlaista tilaa, ja ne kannattaa pitää erillään.

| | Palvelimen tila | Käyttöliittymän tila |
|---|---|---|
| **Esimerkki** | Tuotelista, tilaukset | Avoin välilehti, lomakkeen kentät |
| **Kuka omistaa** | Backend | Selain |
| **Voiko vanhentua** | Kyllä, joku muu voi muuttaa sitä | Ei |
| **Missä** | Hookissa, haetaan rajapinnasta | `useState` komponentissa |

Palvelimen tila on selaimessa aina **kopio**. Kun käyttäjä tallentaa muutoksen, turvallisin tapa on hakea data uudestaan. Jos selain laskee uuden tilan itse, sillä on toinen totuus, joka voi poiketa backendin totuudesta.

Kun sovellus kasvaa, palvelimen tilan hallintaan käytetään usein kirjastoa (esimerkiksi TanStack Query), joka hoitaa välimuistin ja uudelleenhaun. Periaate ei muutu: data kuuluu backendille.

---

## Virheet ja lataustilat

Jokainen haku voi olla kolmessa tilassa: kesken, onnistunut tai epäonnistunut. Käyttöliittymän pitää näyttää ne kaikki.

- **Lataus:** käyttäjä näkee, että jotain tapahtuu.
- **Virhe:** käyttäjä näkee, mitä meni pieleen, mieluiten backendin omalla viestillä.
- **Tyhjä:** "Ei tuotteita" on eri asia kuin virhe.

HTTP-tilakoodi kertoo virheen lajin:

| Koodi | Merkitys | Frontend näyttää |
|-------|----------|------------------|
| 400 | Sääntö tai syöte hylättiin | Backendin viestin lomakkeen vieressä |
| 401 / 403 | Ei kirjautunut tai ei oikeutta | Ohjaa kirjautumaan tai kertoo oikeuden puuttuvan |
| 404 | Kohdetta ei ole | "Ei löytynyt" |
| 500 | Palvelimen vika | Yleisen virheviestin, ei teknisiä yksityiskohtia |

Koodit tarkemmin: [HTTP-pikaopas](../WebAPI/HTTP-Reference.md).

---

## Reaaliaikaisuus

Kun palvelimen pitää kertoa selaimelle muutoksesta, käytetään esimerkiksi [SignalR](../SignalR/README.md):ää. Arkkitehtuurin kannalta yhteys on samanlainen ulkoinen riippuvuus kuin HTTP, joten sille tehdään oma kerros.

```
src/
├── api/        ← HTTP
└── realtime/   ← SignalR-yhteys ja hook, joka kuuntelee tapahtumia
```

Kaksi periaatetta:

1. **Yksi tiedosto tuntee kirjaston.** Komponentti käyttää hookia (`useOrderEvents`), ei `HubConnection`ia.
2. **Tapahtuma on heräte, ei data.** Kun palvelin ilmoittaa "tilaus muuttui", frontend hakee tuoreen datan rajapinnasta. Näin totuus tulee aina samasta paikasta, ja katkennut yhteys ei jätä näkymää väärään tilaan.

---

## Kehitysympäristö: proxy vai CORS

Kehityksessä frontend ja backend pyörivät eri porteissa, esimerkiksi `localhost:5173` ja `localhost:5080`. Selain estää oletuksena pyynnöt toiseen alkuperään (*origin*). Ratkaisuja on kaksi.

**Kehityspalvelimen proxy.** Frontend kutsuu suhteellista osoitetta `/api/...`, ja kehityspalvelin välittää pyynnön backendille. Selain näkee vain yhden alkuperän.

```ts
// vite.config.ts
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://localhost:5080',
      '/hubs': { target: 'http://localhost:5080', ws: true },
    },
  },
});
```

**CORS backendissä.** Backend kertoo, mistä alkuperistä pyyntöjä hyväksytään.

```csharp
builder.Services.AddCors(options =>
    options.AddPolicy("Frontend", policy => policy
        .WithOrigins("http://localhost:5173")
        .AllowAnyHeader()
        .AllowAnyMethod()));

app.UseCors("Frontend");
```

Proxy on yksinkertaisempi, kun frontend ja backend julkaistaan saman osoitteen alle. CORS tarvitaan, kun ne ovat tuotannossa eri osoitteissa. Älä koskaan salli kaikkia alkuperiä (`AllowAnyOrigin`) tuotannossa.

---

## Best Practices

1. **Yksi `fetch`-paikka.** Kaikki pyynnöt kulkevat saman HTTP-apurin läpi.
2. **Tyyppi per DTO, määritelty kerran.** Muuta DTO ja tyyppi samassa muutoksessa.
3. **Hae uudestaan muutoksen jälkeen.** Älä päivitä palvelimen dataa käsin selaimessa.
4. **Näytä backendin virheviesti.** Älä kirjoita samaa sääntöä uudestaan frontendiin.
5. **Feature-kansiot, kun ominaisuuksia on enemmän kuin pari.** Käytä samoja nimiä kuin backendissä.
6. **Pidä komponentit pieninä.** Jos komponentti hakee, laskee ja piirtää, jaa se hookiin ja näyttävään komponenttiin.
7. **Ei salaisuuksia frontendiin.** Kaikki selaimeen ladattu koodi on käyttäjän luettavissa. Katso [salaisuuksien hallinta](../Secrets-Management/).

---

## Anti-patterns

### `fetch` komponentissa

```tsx
// ❌ Komponentti tuntee osoitteen, HTTP:n ja JSONin
function ProductList() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5080/api/v1/products')
      .then((r) => r.json())
      .then(setProducts);
  }, []);
  // ...
}
```

Osoite on kovakoodattu, virhettä ei käsitellä eikä dataa ole tyypitetty. Kun sama lista tarvitaan toisella sivulla, koodi kopioidaan.

### Sääntö kopioituna frontendiin

```tsx
// ❌ Selain päättää, saako tilata
if (product.stock < quantity) {
  alert('Ei varastossa');
  return;
}
```

Selaimen tieto varastosta voi olla minuutteja vanha. Kun sääntö muuttuu backendissä, tämä kopio jää vanhaksi. Lähetä pyyntö ja näytä backendin vastaus.

### Toinen totuus selaimessa

```tsx
// ❌ Selain laskee uuden saldon itse
setBalance(balance - amount);
```

Jos pyyntö epäonnistuu tai joku muu muutti saldoa, ruudulla on väärä luku. Hae saldo uudestaan.

### Entiteetti rajapinnassa

Jos backend palauttaa entiteetin sellaisenaan, frontend alkaa riippua tietokannan rakenteesta. Sarakkeen uudelleennimeäminen rikkoo käyttöliittymän. Katso [DTO:t](DTOs.md).

---

## Yhteenveto

| Käsite | Yhdellä lauseella |
|--------|-------------------|
| **SPA** | Selaimessa pyörivä sovellus, joka käyttää backendia HTTP-rajapinnan kautta |
| **API-client** | Kerros, joka piilottaa osoitteet ja HTTP:n muulta sovellukselta |
| **Tyyppi = DTO** | Yksi TypeScript-tyyppi jokaista backendin DTO:ta kohti |
| **Hook** | Omistaa palvelimelta haetun tilan: data, lataus, virhe |
| **Näyttävä komponentti** | Piirtää propsit, ei hae dataa |
| **Feature-kansio** | Yhden ominaisuuden tiedostot vierekkäin |
| **UX-validointi** | Frontendin tarkistus nopeaa palautetta varten; sääntö päätetään backendissä |
| **Palvelimen tila** | Backendin omistama data, josta selaimessa on vain kopio |
| **Proxy / CORS** | Kaksi tapaa sallia frontendin kutsut eri portissa pyörivään backendiin |

### Muista

- Riippuvuudet kulkevat yhteen suuntaan: komponentti → hook → API-client → HTTP.
- Backend on ainoa totuus. Selain näyttää ja kysyy.
- Kun data muuttuu, hae se uudestaan.

---

## Seuraavaksi

- **[DTO:t](DTOs.md)** - Rajapinnan sopimus backendin puolelta
- **[CQRS](CQRS.md)** - Lukumallit, jotka on tehty juuri näkymää varten
- **[SignalR](../SignalR/README.md)** - Palvelimelta selaimeen kulkevat ilmoitukset
- **[Clean Architecture](Clean-Architecture.md)** - Sama riippuvuuksien suunta backendissä

### Hyödyllisiä linkkejä

- [Microsoft: Choose between traditional web apps and SPAs](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/choose-between-traditional-web-and-single-page-apps)
- [Microsoft: Enable CORS in ASP.NET Core](https://learn.microsoft.com/en-us/aspnet/core/security/cors)
- [Microsoft: ASP.NET Core SignalR JavaScript client](https://learn.microsoft.com/en-us/aspnet/core/signalr/javascript-client)
- [React: Reusing Logic with Custom Hooks](https://react.dev/learn/reusing-logic-with-custom-hooks)
- [React: You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect)
- [Vite: Server Options (proxy)](https://vite.dev/config/server-options.html#server-proxy)
