# Express.js-backend (Express.js)

Express on Node.js:n kevyt web-sovelluskehys REST API -rajapintojen ja palvelinsovellusten tekemiseen. Se on JavaScript-maailman vastine ASP.NET Corelle: reititys, middleware ja JSON-vastaukset muutamalla rivillä.

**Dokumentaatio:** [expressjs.com](https://expressjs.com/)

## Sisällysluettelo

1. [Projektin luonti](#1-projektin-luonti)
2. [Ensimmäinen API](#2-ensimmäinen-api)
3. [Reitit ja Router](#3-reitit-ja-router)
4. [Middleware](#4-middleware)
5. [Virheenkäsittely](#5-virheenkäsittely)
6. [Suositeltu rakenne ja käytännöt](#6-suositeltu-rakenne-ja-käytännöt)

---

## 1. Projektin luonti

Vaatii [Node.js](https://nodejs.org/):n (LTS-versio).

```bash
mkdir my-api && cd my-api
npm init -y
npm install express
```

Lisää `package.json`-tiedostoon `"type": "module"`, jotta voit käyttää `import`-syntaksia.

---

## 2. Ensimmäinen API

`index.js`:

```javascript
import express from "express";

const app = express();
app.use(express.json()); // lukee JSON-rungon req.body:hin

const products = [{ id: 1, name: "Kahvi" }];

app.get("/api/products", (req, res) => {
  res.json(products);
});

app.get("/api/products/:id", (req, res) => {
  const product = products.find(p => p.id === Number(req.params.id));
  if (!product) return res.status(404).json({ error: "Not found" });
  res.json(product);
});

app.post("/api/products", (req, res) => {
  const product = { id: products.length + 1, name: req.body.name };
  products.push(product);
  res.status(201).json(product);
});

app.listen(3000, () => console.log("http://localhost:3000"));
```

Käynnistä: `node index.js` (tai `node --watch index.js`, joka käynnistää palvelimen uudelleen muutoksista).

| Express | ASP.NET Core -vastine |
|---|---|
| `app.get("/api/products", …)` | `[HttpGet]`-metodi controllerissa |
| `req.params.id` | reittiparametri `{id}` |
| `req.body` | `[FromBody]`-parametri |
| `res.status(404).json(…)` | `return NotFound(…)` |

---

## 3. Reitit ja Router

Jaa reitit omiin tiedostoihinsa `express.Router()`:lla.

```javascript
// routes/products.js
import { Router } from "express";
const router = Router();

router.get("/", (req, res) => res.json([]));

export default router;

// index.js
import productsRouter from "./routes/products.js";
app.use("/api/products", productsRouter);
```

---

## 4. Middleware

Middleware on funktio, joka ajetaan pyynnön ja vastauksen välissä. `next()` siirtää vuoron seuraavalle.

```javascript
app.use((req, res, next) => {
  console.log(`${req.method} ${req.url}`);
  next();
});
```

Yleisiä: `express.json()` (JSON-runko), [`cors`](https://www.npmjs.com/package/cors) (selaimen ristiinpyynnöt frontendiltä).

---

## 5. Virheenkäsittely

Virhemiddlewarella on neljä parametria, ja se rekisteröidään viimeisenä:

```javascript
app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).json({ error: "Internal server error" });
});
```

---

## 6. Suositeltu rakenne ja käytännöt

```
my-api/
├─ routes/        reitit (vrt. controllers)
├─ services/      liiketoimintalogiikka
├─ middleware/    omat middlewaret
├─ index.js       sovelluksen käynnistys
└─ .env           ympäristömuuttujat (EI GitHubiin)
```

- Pidä reitit ohuina ja logiikka serviceissä, samoin kuin [ASP.NET Coressa](../AspNet/AspNet.md).
- Lue asetukset ympäristömuuttujista (`process.env.PORT`). Lisää `.env` ja `node_modules/` tiedostoon `.gitignore`.
- Palauta oikeat statuskoodit. Katso [HTTP-referenssi](../../../C%23/fin/04-Advanced/WebAPI/HTTP-Reference.md).
- Validoi syöte ennen käsittelyä.

---

## Hyödyllisiä linkkejä

- [Express — Getting started](https://expressjs.com/en/starter/installing.html)
- [Express — Routing](https://expressjs.com/en/guide/routing.html)
- [Express — Using middleware](https://expressjs.com/en/guide/using-middleware.html)
- [MDN: Express/Node introduction](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Express_Nodejs/Introduction)
