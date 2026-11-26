# NutriPen

Diário de acompanhamento nutricional para quem usa canetas GLP-1/GIP (tirzepatida, semaglutida, liraglutida): proteína, água, fibras, peso, medidas, glicemia, sintomas, evacuação e rodízio dos locais de aplicação.

**Versão de teste.** Não substitui orientação médica ou nutricional. Os dados de cada pessoa ficam apenas no navegador do próprio aparelho.

## Usar
Abra https://gilrock-git.github.io/nutripem/ no celular. Para instalar: Android (Chrome) → menu ⋮ do app → "Instalar no celular"; iPhone (Safari) → Compartilhar → "Adicionar à Tela de Início". Depois da primeira abertura funciona sem internet (exceto a análise por IA).

## Estrutura
- `index.html`, `app.css`, `vendor/`, `icons/`, `manifest.webmanifest`, `sw.js` — app publicado (gerado).
- `fonte/nutripen.html` — código-fonte em arquivo único; `fonte/*.py|*.js` — scripts que geram a versão publicada.

## Gerar de novo após editar `fonte/nutripen.html`
```
npm i tailwindcss@3.4.16 lucide@0.460.0
python3 fonte/build_pwa.py fonte/nutripen.html node_modules ./_build
node fonte/finalize_pwa.js ./_build     # requer Playwright
```
Copie o conteúdo de `_build/` para a raiz do repositório e publique.
