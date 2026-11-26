#!/usr/bin/env python3
"""Converte nutripen.html na versão de teste publicada no claude.ai."""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
h = open(src, encoding='utf-8').read()
def rep(a, b):
    global h
    assert h.count(a) == 1, (h.count(a), a[:70]); h = h.replace(a, b)
rep('<!DOCTYPE html>\n<html lang="pt-BR">\n<head>\n', '<title>NutriPen</title>\n')
rep('  <title>NutriPen — Acompanhamento Nutricional & GLP-1/GIP</title>\n', '')
cls = re.search(r'</head>\n<body class="([^"]+)">', h).group(1)
h = re.sub(r'</head>\n<body class="[^"]+">', f'<script>document.documentElement.lang="pt-BR";document.body.className={cls!r};</script>', h, count=1)
rep('</body>\n</html>', '')
rep("""        var t = localStorage.getItem('nutripen_theme');
        if (t === 'dark' || (!t && window.matchMedia('(prefers-color-scheme: dark)').matches)) {""",
"""        var v = document.documentElement.getAttribute('data-theme');
        var t = null; try { t = localStorage.getItem('nutripen_theme'); } catch (e) {}
        if (v === 'dark' || (!v && (t === 'dark' || (!t && window.matchMedia('(prefers-color-scheme: dark)').matches)))) {""")
rep('    body { font-family:', '    html.dark { color-scheme: dark; }\n    header.sticky { top: env(safe-area-inset-top, 0px); }\n    body { font-family:')
rep('            <button type="button" onclick="window.print()" class="btn btn-md btn-soft">🖨️ Imprimir / PDF</button>\n', '')
h = h.rstrip() + '''
<script>
  // Versão de teste no claude.ai: sem download de arquivo e sem acesso ao Gemini
  async function exportBackupJSON() {
    const copy = JSON.parse(JSON.stringify(appState));
    copy.profile.customGeminiKey = '';
    copy.exportedAt = new Date().toISOString();
    try { await navigator.clipboard.writeText(JSON.stringify(copy)); showToast('Backup copiado. Cole num bloco de notas e salve como .json.', 'success', { duration: 7000 }); }
    catch (e) { showToast('Não consegui copiar o backup nesta versão de teste.', 'error'); }
  }
  async function callGeminiNutritionAI() {
    $('ai-result-card').classList.add('hidden');
    showAIFallback('🧪 IA indisponível na versão de teste', 'A análise por foto/texto só funciona na versão instalável (pasta nutripen-pwa publicada). Aqui, use o Montador rápido ou a Tabela.', false);
    toggleOfflinePlateBuilder(true);
  }
</script>
'''
open(dst, 'w', encoding='utf-8').write(h)
print('ok')
