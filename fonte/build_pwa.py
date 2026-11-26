#!/usr/bin/env python3
"""Gera a versão PWA (instalável e offline) do NutriPen a partir do arquivo único.

Uso: python3 build_pwa.py <nutripen.html> <pasta_node_modules> <pasta_saida>
Requer: tailwindcss@3.4.16 e lucide@0.460.0 instalados em <pasta_node_modules>/..
"""
import hashlib, json, re, shutil, subprocess, sys
from pathlib import Path

src, node_dir, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
html = src.read_text(encoding='utf-8')
# A pasta de saída é apagada e recriada: nunca aceitar a raiz do repositório ou uma pasta que a contenha.
if (out / '.git').exists() or out.resolve() in Path.cwd().resolve().parents or out.resolve() == Path.cwd().resolve():
    sys.exit(f'Pasta de saída insegura (seria apagada): {out}. Use uma pasta temporária.')
if out.exists():
    shutil.rmtree(out)
(out / 'vendor').mkdir(parents=True)
(out / 'icons').mkdir()

def replace_once(text, pattern, repl, flags=re.S):
    new, n = re.subn(pattern, repl, text, count=1, flags=flags)
    if n != 1:
        sys.exit(f'Padrão não encontrado: {pattern[:60]}')
    return new

# 1) Extrai config e componentes do Tailwind e remove o CDN
cfg = re.search(r'tailwind\.config = (\{.*?\});\s*</script>', html, re.S).group(1)
components = re.search(r'<style type="text/tailwindcss">(.*?)</style>', html, re.S).group(1)
html = replace_once(html, r'\s*<!-- Tailwind v3.*?</script>\s*<script>\s*tailwind\.config = .*?</script>', '\n  <link rel="stylesheet" href="app.css" />')
html = replace_once(html, r'\s*<style type="text/tailwindcss">.*?</style>', '')
html = replace_once(html, r'<script src="https://unpkg\.com/lucide@[^"]+"></script>', '<script src="vendor/lucide.min.js"></script>')
html = replace_once(html, r'(<title>.*?</title>)', r'''\1
  <link rel="manifest" href="manifest.webmanifest" />
  <link rel="icon" type="image/svg+xml" href="icons/icon.svg" />
  <link rel="apple-touch-icon" href="icons/apple-touch-icon.png" />''')
csp = ("default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
       "font-src 'self' https://fonts.gstatic.com; img-src 'self' data: blob:; connect-src 'self' https://generativelanguage.googleapis.com; "
       "manifest-src 'self'; worker-src 'self'; object-src 'none'; base-uri 'none'; form-action 'none'")
html = replace_once(html, r'<meta charset="UTF-8" />', '<meta charset="UTF-8" />\n  <meta http-equiv="Content-Security-Policy" content="' + csp + '" />')
(out / 'index.html').write_text(html, encoding='utf-8')

# 2) CSS compilado e minificado (só as classes realmente usadas)
work = out.parent / '_tw_work'
work.mkdir(exist_ok=True)
(work / 'in.css').write_text('@tailwind base;\n@tailwind components;\n@tailwind utilities;\n' + components, encoding='utf-8')
(work / 'tailwind.config.js').write_text(
    f"module.exports = Object.assign({cfg}, {{ content: [{json.dumps(str((out / 'index.html').resolve()))}] }});", encoding='utf-8')
subprocess.run([str(node_dir / '.bin' / 'tailwindcss'), '-c', str(work / 'tailwind.config.js'),
                '-i', str(work / 'in.css'), '-o', str(out / 'app.css'), '--minify'], check=True, capture_output=True)
shutil.rmtree(work)

# 3) Lucide local
shutil.copy(node_dir / 'lucide' / 'dist' / 'umd' / 'lucide.min.js', out / 'vendor' / 'lucide.min.js')

# 4) Ícones SVG a partir do logotipo oficial (marca/simbolo-caneta-folha-ambar.svg)
logo = (Path(__file__).resolve().parent.parent / 'marca' / 'simbolo-caneta-folha-ambar.svg').read_text(encoding='utf-8')
(out / 'icons' / 'icon.svg').write_text(logo, encoding='utf-8')
# Versão "maskable": fundo até a borda e desenho reduzido para caber na área segura (círculo de 80%)
m = re.match(r'(<svg[^>]*>\s*<defs>.*?</defs>)\s*<rect[^>]*/>(.*)</svg>\s*$', logo, re.S)
maskable = m.group(1) + '<rect width="120" height="120" fill="url(#bg-ambar)"/><g transform="translate(60 60) scale(.74) translate(-60 -60)">' + m.group(2) + '</g></svg>'
(out / 'icons' / 'maskable.svg').write_text(maskable, encoding='utf-8')

# 5) Manifest
manifest = {
    'name': 'NutriPen — Acompanhamento GLP-1/GIP',
    'short_name': 'NutriPen',
    'description': 'Acompanhamento nutricional para quem usa canetas GLP-1/GIP.',
    'lang': 'pt-BR',
    'start_url': './',
    'scope': './',
    'display': 'standalone',
    'orientation': 'portrait',
    'background_color': '#f8fafc',
    'theme_color': '#0d9488',
    'categories': ['health', 'medical', 'lifestyle'],
    'icons': [
        {'src': 'icons/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
        {'src': 'icons/icon-512.png', 'sizes': '512x512', 'type': 'image/png'},
        {'src': 'icons/maskable-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'},
        {'src': 'icons/icon.svg', 'sizes': 'any', 'type': 'image/svg+xml'}
    ],
    'shortcuts': [
        {'name': 'Registrar glicemia', 'url': './?acao=glicemia'},
        {'name': 'Registrar refeição', 'url': './?aba=refeicoes'}
    ]
}
(out / 'manifest.webmanifest').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print('OK: html/css/vendor/manifest/svg gerados')
