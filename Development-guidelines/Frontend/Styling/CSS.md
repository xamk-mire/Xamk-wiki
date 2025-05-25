## 1  What Is CSS?

CSS (**Cascading Style Sheets**) is a style‑sheet language that tells the browser **how** content should look: colors, size, layout, animation, and even print rules.
*HTML = structure* | *CSS = presentation* | *JavaScript = behavior*

### 1.1 Why “cascading”?

Multiple style sheets can target the same element. The browser resolves conflicts using the **cascade algorithm**—source order → importance (`!important`) → origin (user‑agent, user, author) → selector specificity.

---

## 2  Setting Up

### 2.1 Three Ways to Add CSS

```html
<!-- Inline (avoid in production) -->
<h1 style="color: tomato;">Hello</h1>

<!-- Internal -->
<style>
  h1 { color: tomato; }
</style>

<!-- External (best practice) -->
<link rel="stylesheet" href="styles.css" />
```

Put global styles in **external** `.css` files so you can cache and reuse them.

### 2.2 Folder Structure

```
project/
├── index.html
└── css/
    └── main.css
```

---

## 3  CSS Basics

### 3.1 Selectors, Properties, Values

Every CSS rule targets elements (selectors), declares which visual trait to change (property), and assigns a setting (value).

```css
/* selector   property     value  */
   header   { background: #0d47a1; }
```

Here’s a single mini‑webpage that demonstrates every common selector type in one place:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Selector Playground</title>
  <style>
    /* Type/tag selector */
    p { color: steelblue; }

    /* Class selector */
    .card { border: 2px solid tomato; padding: 1rem; margin-block: 1rem; }

    /* ID selector */
    #nav { background: hsl(210 90% 95%); padding: 0.5rem 1rem; position: sticky; top: 0; }

    /* Attribute selector */
    input[type="email"] { border: 2px solid mediumseagreen; }

    /* Pseudo‑class selector */
    a:hover { color: crimson; }

    /* Pseudo‑element selector */
    p::first-line { font-weight: 700; }
    ul li::marker { color: rebeccapurple; }
  </style>
</head>
<body>
  <nav id="nav"> <!-- ID selector -->
    <a href="#">Home</a> <!-- Pseudo‑class selector -->
    <a href="#">About</a> <!-- Pseudo‑class selector -->
  </nav>
 
  <article class="card">  <!-- Class selector -->
    <h2>Type & Pseudo‑element Example</h2>
    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur rhoncus.</p> <!-- Type/tag selector -->
  </article>

  <ul>
    <li>List item one</li> <!-- Pseudo‑element selector -->
    <li>List item two</li> <!-- Pseudo‑element selector -->
  </ul>

  <form class="card">
    <label>
      Your email:
      <input type="email" placeholder="you@example.com"> <!-- Attribute selector -->
    </label>
    <button type="submit">Submit</button>
  </form>
</body>
</html>
```

### 3.2 Comments & Readability Comments & Readability Comments & Readability

```css
/* ===== Typography ===== */
```

Use section comments to group related rules.

---

## 4  The Box Model Deep Dive

![box model diagram](https://media.geeksforgeeks.org/wp-content/uploads/20241210112354236207/Screenshot-2024-12-10-105714.png)

Every element is a rectangle with:

* **Content** (blue)
* **Padding** (green)
* **Border** (yellow)
* **Margin** (orange)

```css
.card {
  padding: 1rem;   /* inside */
  border: 1px solid #ccc;
  margin: 1rem 0; /* outside */
}
```

---

## 5  Layout Systems

Modern CSS gives you three complementary systems for arranging elements: **Flexbox**, **Grid**, and **positioning/z‑index**.
Think of them as tools in a toolbox—each excels at certain jobs and can be combined for complex interfaces.

### 5.1  Flexbox — the one‑dimensional powerhouse

Flexbox lays items out **in a single *main axis*** (row *or* column). It shines for nav bars, tool‑bars, forms, cards, or any component where items flow in one direction but need smart distribution or alignment.

| Category      | Key Properties (Container)                                                                  | Key Properties (Items)                    | What They Do                        |
| ------------- | ------------------------------------------------------------------------------------------- | ----------------------------------------- | ----------------------------------- |
| **Axis**      | `flex-direction`                                                                            | –                                         | Switch row/column and reverse order |
| **Alignment** | `justify-content` (main axis)<br>`align-items` (cross axis)<br>`align-content` (multi‑line) | `align-self`                              | Control spacing and alignment       |
| **Wrapping**  | `flex-wrap` (`nowrap` `wrap` `wrap-reverse`)                                                | –                                         | Allow items to move to new lines    |
| **Sizing**    | `gap`                                                                                       | `flex: 1 0 200px` (grow / shrink / basis) | Proportional growth & shrink        |

```css
ul.menu {
  display: flex;
  flex-direction: row;
  gap: 2rem;
  justify-content: flex-end; /* push items to the right */
}
.menu li {
  flex: 0 1 auto; /* don’t grow, allow shrink */
}
```

> **Debug tip:** In DevTools enable *“flex overlay”* to visualize the main axis, cross axis, and item sizes.

**When to choose Flexbox:**

* You want to create a flexible website.
* Linear layouts (rows/columns) that **re‑flow** with content.
* Centering (set `display:flex; justify-content:center; align-items:center;`).
* Fancy equal‑height cards without extra wrappers.

---

### 5.2  CSS Grid — the two‑dimensional layout manager

Grid treats the page as a matrix of **rows *and* columns**, letting you place items precisely into cells or named areas.

| Concept                  | How It Works                                      | Quick Example                 |
| ------------------------ | ------------------------------------------------- | ----------------------------- |
| **Track definition**     | `grid-template-columns: 1fr 2fr 1fr;`             | 3 columns in 1:2:1 ratio      |
| **Implicit tracks**      | `grid-auto-rows: 200px;`                          | Auto rows when content spills |
| **Line‑based placement** | `grid-column: 2 / 4;`                             | Span from line 2 to line 4    |
| **Named areas**          | `grid-template-areas: "hd hd" "sb main" "ft ft";` | Semantic mapping              |
| **Responsive repeat**    | `repeat(auto-fit, minmax(16rem, 1fr))`            | Fluid card grids              |

```css
.dashboard {
  display: grid;
  grid-template-columns: 220px 1fr; /* sidebar + content */
  grid-template-areas:
    "nav   nav"
    "side  main"
    "side  main";
  min-height: 100vh;
}
nav    { grid-area: nav; }
.aside { grid-area: side; }
main   { grid-area: main; }
```

> **Tip:** Use the **`fr` unit** for flexible tracks and **`minmax()`**/`auto-fit` for responsive masonry‑like layouts.

**When to choose Grid:**

* Page‑level scaffolding—headers, sidebars, footers.
* Complex components needing **both dimensions** (calendars, image galleries).
* Overlapping content via `grid-template-areas` or `grid-area` stacking.

---

### 5.3  Positioning & Stacking Contexts — absolute precision

Flexbox & Grid handle most layout—reserve *positioning* for overlays, tooltips, and fine‑grained tweaks.

| Position value       | Creates new stacking context? | Use case                                              |
| -------------------- | ----------------------------- | ----------------------------------------------------- |
| `static` *(default)* | ✖                             | Normal flow                                           |
| `relative`           | ✖                             | Offset element while **keeping** its space            |
| `absolute`           | ✔ (if `z-index` ≠ `auto`)     | Place tooltip relative to nearest positioned ancestor |
| `fixed`              | ✔                             | Sticky header that ignores page scroll                |
| `sticky`             | ✖                             | Sidebar that sticks after a threshold                 |

#### 5.3.1  Understanding `z-index`

`z-index` controls **stacking order** *within the same stacking context*. A new context is created by:

* Positioned elements (`relative | absolute | fixed | sticky`) **with `z-index` other than `auto`**
* Flex/Grid children with `z-index` ≠ `auto`
* `opacity` < 1, `transform`, `filter`, `perspective`, `isolation: isolate`, etc.

```css
.modal {
  position: fixed;
  inset: 0;
  display: grid;
  place-items: center;
  background: rgba(0 0 0 / .4);
  z-index: 1000; /* sits above header (900) */
}
```

> **Debug tip:** In Chrome’s Layers panel (or Firefox’s 3‑D view) you can inspect stacking contexts to track mysterious overlap bugs.

**Guidelines for Positioning & `z-index`:**

1. Declare **sensible tiers** (`header 900`, `modal 1000`, etc.) in tokens/variables.
2. Keep contexts shallow—avoid random `transform` on parents.
3. Prefer `translate` over changing `top/left` for animation (it’s GPU‑accelerated and avoids layout thrash).

---

### 5.4  Choosing the Right Tool

```
Is it linear?  → Flexbox
Does it need rows *and* columns?  → Grid / Flexbox using flex-grid
Is it an overlay or offset tweak?  → Positioning + z‑index
```

In practice you’ll most likely end up using each layout system at the same time: a Grid page containing Flexbox nav items, with `position:sticky` headers. Master all three and layout becomes a creative playground.

> **Tip:** It's recommended to start by using Flexbox and only use CSS Grid if it becomes absolutely necessary or easier to implement the wanted layout.

---

## 6  Responsive Design  Responsive Design

### 6.1 Media Queries

```css
/* When viewport width is less or equal to 600px */
@media (width <= 600px) {
  .sidebar { display: none; }
}
```

### 6.2 Fluid Units

* `rem` for typography, spacing
* `%` or `fr` for Grid tracks
* `min()`/`clamp()` for “stretchy” sizes

### 6.3 Mobile‑First Strategy

1. Write base styles for small screens.
2. Layer on media queries for larger breakpoints.

---

## 7  Understanding the Cascade & Specificity

| Selector                                                                                   | Specificity Value |
| ------------------------------------------------------------------------------------------ | ----------------- |
| Element                                                                                    | 0‑0‑0‑1           |
| Class                                                                                      | 0‑0‑1‑0           |
| ID                                                                                         | 0‑1‑0‑0           |
| Use the **Lowest Specificity Needed** principle—avoid IDs except for anchors and JS hooks. |                   |

---

## 8  Organizing & Scaling CSS

* **Naming conventions**: Utility‑first (`.mt-4`).
* **Cascade Layers**: `@layer reset, base, components, utilities;` to control order.
* **Modularity**: Separate files per feature (`buttons.css`, `forms.css`) and import with `@import` or bundler.

---

## 9  Modern CSS Features

* **Custom properties (variables)**

  ```css
  :root {
    --brand-hue: 220;
    --brand: hsl(var(--brand-hue) 80% 50%);
  }
  a { color: var(--brand); }
  ```
* **Nesting** *(Stage 3 — works in all evergreen browsers as of 2025)*

  ```css
  .card {
    &:hover {
      transform: translateY(-4px);
    }
  }
  ```
* **Container Queries**

  ```css
  @container style(min-width: 400px) {
    .product-card { grid-template-columns: 1fr 2fr; }
  }
  ```

---

## 10  Performance & Best Practices

1. **Avoid `!important`**—it breaks the cascade.
2. **Group repaint‑heavy properties** in `:root` variables & transition only what’s needed.
3. **Minify & bundle** in production (e.g., `cssnano`, `LightningCSS`).
4. **Use prefers‑reduced‑motion** to respect accessibility.
5. **Audit with DevTools → Performance → Lighthouse**.

---

## 11  Workflow & Debugging

* Open **DevTools** (F12). Inspect, live‑edit styles, and toggle classes.
* Learn `:hov` tool to force `:hover` & `:focus` states.
* Use the **Computed** tab to trace which rule wins.

---

## 12  Hands‑On Project: Responsive Card Layout

Follow these steps to create simple responsive card layout.

### 12.1 Starter HTML

```html
<section class="cards">
  <article class="card">
    <img src="https://picsum.photos/400/300?random=1" alt="Random" />
    <h2>Card 1</h2>
    <p>Lorem ipsum dolor sit amet…</p>
    <a class="btn" href="#">Read More</a>
  </article>
  <!-- Repeat 3–4 times -->
</section>
```

### 12.2 CSS Steps (Simplified)

1. **Reset & base styles**

   ```css
   *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    body {
      font-family: system-ui, sans-serif;
      line-height: 1.6;
      background: #f6f8fa;
    }
    .btn {
      display: inline-block;
      padding: 0.6rem 1rem;
      background: #1865f2;
      color: #fff;
      border-radius: 0.4rem;
      text-decoration: none;
      transition: background 0.25s;
    }
    .btn:hover {
      background: #0047c2;
    }
   ```
2. **Grid Layout**

   ```css
   .cards {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr));
      gap: 1.5rem;
      padding: 2rem;
    }
    .card {
      background: #fff;
      border-radius: 1rem;
      overflow: hidden;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
      display: flex;
      flex-direction: column;
    }
    .card img {
      width: 100%;
      aspect-ratio: 4/3;
      object-fit: cover;
    }
    .card h2 {
      font-size: 1.25rem;
      padding: 1rem 1rem 0;
    }
    .card p {
      padding: 0 1rem 1rem;
    }
    .card .btn {
      margin: 0 1rem 1rem auto;
    }
   ```
3. **Enhance with media queries** if desired.

Test in the browser—resize to watch cards re‑flow.

---
