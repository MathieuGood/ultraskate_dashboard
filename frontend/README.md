# ultraskate_dashboard_frontend

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VS Code](https://code.visualstudio.com/) + [Vue (Official)](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Recommended Browser Setup

- Chromium-based browsers (Chrome, Edge, Brave, etc.):
    - [Vue.js devtools](https://chromewebstore.google.com/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd)
    - [Turn on Custom Object Formatter in Chrome DevTools](http://bit.ly/object-formatters)
- Firefox:
    - [Vue.js devtools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/)
    - [Turn on Custom Object Formatter in Firefox DevTools](https://fxdx.dev/firefox-devtools-custom-object-formatters/)

## Type Support for `.vue` Imports in TS

TypeScript cannot handle type information for `.vue` imports by default, so we replace the `tsc` CLI with `vue-tsc` for type checking. In editors, we need [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) to make the TypeScript language service aware of `.vue` types.

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```

## Prompt

```prompt
 now I have to solve something in the backend. when I load all the events, I would like to add all the unique athletes to the athlete registry which
  contains all the unique athletes. equal() between athlete objects should be based on the name because other attributes could be potentially different
   for each event.  however, i have to be careful with the name comparison because i know some athletes were not registered on the same name on
  different event : like Joe Mazzone / Joseph Mazzone (same guy). And there is one very specific case, I think on Miami Ultra 2013 or 2014, where two
  athletes had the same name. hwo could i handle this weird scenario ? there should be a rule about finding two times the same name in one event and be
   able to connsider them as different athletes. in the end, i want the athlete objects to be only unique athletes and use the same athlete object
  inside each event performance of a single skater. update the claude.md accordingly if needed with this new cosntraint.
```
