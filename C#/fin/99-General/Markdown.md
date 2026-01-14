# Markdown (.md)

## Mikä on Markdown?

**Markdown** on kevyt merkintäkieli, jota käytetään tekstin muotoiluun. Se on suunniteltu helposti luettavaksi ja kirjoitettavaksi, ja se voidaan muuntaa HTML:ksi ja moniin muihin formaatteihin.

Markdown-tiedostot tunnistetaan `.md`-tiedostopäätteestä.

## Mihin Markdown-tiedostoja käytetään?

### 1. Dokumentaatio
- **README-tiedostot** projekteissa (GitHub, GitLab)
- Käyttöoppaat ja tekninen dokumentaatio
- API-dokumentaatio
- Projektin ohjeet ja säännöt

### 2. Wikis ja tietokannat
- GitHub Wiki
- Confluence
- Notion
- Obsidian

### 3. Blogikirjoitukset ja artikkelit
- Staattiset sivugeneraattorit (Jekyll, Hugo, Gatsby)
- Tekninen kirjoittaminen
- Portfoliot

### 4. Muistiinpanot
- Henkilökohtaiset muistiinpanot
- Oppimispäiväkirjat
- Projektisuunnitelmat

## Markdownin hyödyt

### ✅ Helppo oppia ja käyttää
- Yksinkertainen syntaksi
- Ei vaadi erikoisohjelmia
- Nopea kirjoittaa

### ✅ Luettavuus
- Raakakoodikin on helposti luettavaa
- Selkeä rakenne
- Ei tarvitse nähdä "renderöitynä"

### ✅ Yhteensopivuus
- Toimii kaikilla alustoilla
- Voidaan muuntaa HTML:ksi, PDF:ksi, jne.
- Git-ystävällinen (helppo version hallinta)

### ✅ Joustava
- Tukee koodinäytteitä
- Tukee kuvia ja linkkejä
- Tukee taulukoita ja listoja

### ✅ Laaja tuki
- GitHub, GitLab, Bitbucket
- VS Code, Visual Studio
- Slack, Discord, Reddit
- Stack Overflow

## Perussyntaksi

### Otsikot
```markdown
# Otsikko 1
## Otsikko 2
### Otsikko 3
#### Otsikko 4
```

### Tekstin muotoilu
```markdown
**Lihavoitu teksti**
*Kursivoitu teksti*
~~Yliviivattu teksti~~
`Koodi inline`
```

**Tulos:**
- **Lihavoitu teksti**
- *Kursivoitu teksti*
- ~~Yliviivattu teksti~~
- `Koodi inline`

### Listat

**Numeroitu lista:**
```markdown
1. Ensimmäinen
2. Toinen
3. Kolmas
```

**Luettelomerkitty lista:**
```markdown
- Kohta 1
- Kohta 2
  - Alakohta 2.1
  - Alakohta 2.2
- Kohta 3
```

### Linkit
```markdown
[Linkin teksti](https://example.com)
[GitHub](https://github.com)
```

**Tulos:** [GitHub](https://github.com)

### Kuvat
```markdown
![Kuvan alt-teksti](kuvan-url.png)
![Logo](https://example.com/logo.png)
```

### Lainaukset
```markdown
> Tämä on lainaus.
> Se voi olla useita rivejä.
```

**Tulos:**
> Tämä on lainaus.
> Se voi olla useita rivejä.

### Koodilohkot

**Inline-koodi:**
```markdown
Käytä `Console.WriteLine()` metodia tulostukseen.
```

**Koodilohko:**
````markdown
```csharp
public class HelloWorld
{
    static void Main()
    {
        Console.WriteLine("Hello, World!");
    }
}
```
````

**Tulos:**
```csharp
public class HelloWorld
{
    static void Main()
    {
        Console.WriteLine("Hello, World!");
    }
}
```

### Taulukot
```markdown
| Nimi    | Ikä | Kaupunki |
|---------|-----|----------|
| Alice   | 25  | Helsinki |
| Bob     | 30  | Turku    |
| Charlie | 35  | Tampere  |
```

**Tulos:**

| Nimi    | Ikä | Kaupunki |
|---------|-----|----------|
| Alice   | 25  | Helsinki |
| Bob     | 30  | Turku    |
| Charlie | 35  | Tampere  |

### Vaakaviiva
```markdown
---
```

**Tulos:**

---

### Tehtävälista (GitHub Flavored Markdown)
```markdown
- [x] Valmis tehtävä
- [ ] Keskeneräinen tehtävä
- [ ] Tekemättä oleva tehtävä
```

**Tulos:**
- [x] Valmis tehtävä
- [ ] Keskeneräinen tehtävä
- [ ] Tekemättä oleva tehtävä

## Markdown-editoreita

### Ilmaiset editorit
- **Visual Studio Code** (suositeltu)
  - Sisäänrakennettu Markdown-tuki
  - Live preview (Ctrl+Shift+V)
  - Laajennukset: Markdown All in One, Markdown Preview Enhanced

- **Typora** - WYSIWYG-tyylinen
- **Mark Text** - Avoimen lähdekoodin
- **Obsidian** - Muistiinpanoihin
- **Notable** - Muistiinpanoihin

### Online-editorit
- **StackEdit** - Selaimessa toimiva
- **Dillinger** - Online Markdown-editori
- **HackMD** - Yhteistyöpohjainen

## Markdown GitHub:ssa

GitHub käyttää **GitHub Flavored Markdown (GFM)** -muotoa, joka tukee lisäominaisuuksia:

### Emojit
```markdown
:smile: :heart: :thumbsup: :rocket:
```
**Tulos:** 😄 ❤️ 👍 🚀

### Syntax highlighting
````markdown
```python
def hello():
    print("Hello, World!")
```
````

### Automaattiset linkit
```markdown
https://github.com → muuttuu automaattisesti linkiksi
```

### Käyttäjien ja issuejen viittaaminen
```markdown
@käyttäjänimi
#123 (issue-numero)
```

## README.md - projektin käyntikortti

`README.md` on projektin tärkein tiedosto. Sen tulisi sisältää:

### 1. Projektin nimi ja kuvaus
```markdown
# Projektin nimi

Lyhyt kuvaus siitä, mitä projekti tekee.
```

### 2. Ominaisuudet
```markdown
## Ominaisuudet
- Ominaisuus 1
- Ominaisuus 2
- Ominaisuus 3
```

### 3. Asennus
```markdown
## Asennus

1. Kloonaa repositorio
2. Asenna riippuvuudet
3. Käynnistä sovellus
```

### 4. Käyttö
```markdown
## Käyttö

Ohjeet sovelluksen käyttöön.

\```csharp
// Koodiesimerkkejä
\```
```

### 5. Teknologiat
```markdown
## Teknologiat
- C# 12.0
- .NET 8.0
- ASP.NET Core
```

### 6. Kontribuutio
```markdown
## Kontribuutio

Pull requestit ovat tervetulleita!
```

### 7. Lisenssi
```markdown
## Lisenssi

MIT License
```

## Parhaat käytännöt

### ✅ Käytä selkeitä otsikoita
- Hyvin jäsennelty dokumentti on helppo lukea
- Otsikoiden hierarkia on tärkeä

### ✅ Käytä koodiesimerkkejä
- Syntaksin korostus auttaa ymmärryksessä
- Konkreettiset esimerkit ovat selkeämpiä

### ✅ Pidä teksti ytimekkäänä
- Älä kirjoita liikaa kerralla
- Jaa suuret dokumentit pienempiin osiin

### ✅ Käytä linkkejä viisaasti
- Linkit muihin dokumentteihin
- Ulkoiset resurssit
- Sisäiset ankkurit pitkissä dokumenteissa

### ✅ Päivitä säännöllisesti
- Vanhentuneet ohjeet ovat haitallisia
- README.md:n tulisi olla ajan tasalla

## Markdown ja Visual Studio Code

### Hyödylliset pikanäppäimet
- `Ctrl+Shift+V` - Avaa preview
- `Ctrl+K V` - Avaa preview vierekkäin
- `Ctrl+B` - Lihavointi
- `Ctrl+I` - Kursivointi

### Suositeltuja laajennuksia
1. **Markdown All in One**
   - Pikanäppäimet
   - Automaattinen sisällysluettelo
   - Taulukoiden muotoilu

2. **Markdown Preview Enhanced**
   - Parempi preview
   - Export PDF:ksi
   - Kaaviot ja diagrammit

3. **markdownlint**
   - Tarkistaa Markdown-syntaksin
   - Noudattaa parhaita käytäntöjä

## Esimerkkejä

### Esimerkki 1: README.md projektipohjalle
```markdown
# Projektin nimi

Lyhyt kuvaus projektista.

## Ominaisuudet
- Ominaisuus 1
- Ominaisuus 2

## Asennus

\```bash
git clone https://github.com/käyttäjä/projekti.git
cd projekti
dotnet restore
dotnet run
\```

## Käyttö

\```csharp
var app = new Application();
app.Run();
\```

## Lisenssi
MIT
```

### Esimerkki 2: Dokumentaatio
```markdown
# API-dokumentaatio

## Käyttäjän haku

**Endpoint:** `GET /api/users/{id}`

**Parametrit:**
- `id` (int) - Käyttäjän ID

**Vastaus:**
\```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com"
}
\```
```

## Yhteenveto

Markdown on:
- **Yksinkertainen** - Helppo oppia ja käyttää
- **Joustava** - Sopii moniin käyttötarkoituksiin
- **Laajalti tuettu** - Toimii kaikkialla
- **Git-ystävällinen** - Helppo version hallinta
- **Tulevaisuuden varma** - Pelkkää tekstiä

Markdown on must-have taito jokaiselle ohjelmoijalle!

## Lisäresurssit

- [Markdown Guide](https://www.markdownguide.org/) - Kattava opas
- [GitHub Flavored Markdown Spec](https://github.github.com/gfm/) - GFM-spesifikaatio
- [CommonMark](https://commonmark.org/) - Markdown-standardi
- [Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) - Pikaopas
- [Dillinger](https://dillinger.io/) - Online-editori harjoitteluun
