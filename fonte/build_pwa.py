#!/usr/bin/env python3
"""Gera a versão PWA (instalável e offline) do NutriPen a partir do arquivo único.

Uso: python3 build_pwa.py <nutripen.html> <pasta_node_modules> <pasta_saida>
Requer: tailwindcss@3.4.16 e lucide@0.460.0 instalados em <pasta_node_modules>/..
"""
import hashlib, json, re, shutil, subprocess, sys
from pathlib import Path

src, node_dir, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
html = src.read_text(encoding='utf-8')
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

# 4) Ícone SVG (mesmo desenho do logotipo)
icon_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#14b8a6"/><stop offset="1" stop-color="#115e59"/></linearGradient></defs>
  <rect width="512" height="512" rx="{rx}" fill="url(#g)"/>
  <g transform="translate({t} {t}) scale({s})" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/><path d="m15 5 4 4"/><path d="M9.5 11.5c1.5-1.5 3.5-1.5 5 0"/>
  </g>
</svg>'''
(out / 'icons' / 'icon.svg').write_text(icon_svg.format(rx=112, t=106, s=12.5), encoding='utf-8')
(out / 'icons' / 'maskable.svg').write_text(icon_svg.format(rx=0, t=156, s=8.33), encoding='utf-8')

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
