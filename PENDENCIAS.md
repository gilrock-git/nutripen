# NutriPen — pendências e ideias

Lista de melhorias anotadas para as próximas versões. Marque com [x] quando concluir.

## Pedidas pelo usuário (prioridade)

- [ ] **Doses fracionadas.** Hoje a dose é escolhida numa lista fixa por medicação
  (ex.: tirzepatida 2,5 / 5 / 7,5 mg…). Permitir doses intermediárias, como as usadas
  ao fracionar a caneta (ex.: 1,25 mg, 3,75 mg, 6 mg):
  - campo de dose livre em mg (com vírgula), mantendo a lista como atalho;
  - opcional: registrar em "cliques/unidades" da caneta multidose, com conversão para mg;
  - gráficos, titulação no relatório e marcadores de troca de dose devem aceitar esses valores.
  - Telas afetadas: Meu Perfil, Iniciar perfil, Aplicação (Diário) e Peso (Medidas).

- [ ] **Intervalo entre aplicações configurável.** Nem sempre é 1x por semana — no fim do
  tratamento é comum espaçar (ex.: a cada 10, 14 dias). Hoje o app só tem "dia da semana".
  - No perfil: **intervalo em dias** (7 por padrão; aceitar qualquer valor) em vez de só o dia da semana;
  - próxima aplicação = **data da última aplicação + intervalo** (contagem e aviso de atraso
    passam a usar esse intervalo);
  - ao registrar uma aplicação, poder informar a dose **e** o intervalo até a próxima
    (o intervalo pode mudar ao longo do tratamento);
  - relatório: mostrar a evolução de dose **e** de intervalo (ex.: "5 mg a cada 7 dias → 5 mg a cada 14 dias").

- [ ] **Alarme / lembrete da aplicação.** Hoje o app só mostra a contagem quando é aberto.
  - Versão Android: notificação local agendada (plugin `@capacitor/local-notifications`), que
    funciona sem internet e não altera a "Segurança dos dados";
  - lembrete no dia, no horário escolhido (ex.: 9h), e opcional na véspera à noite;
  - reagendar sozinho ao registrar uma aplicação ou mudar o intervalo (depende do item acima);
  - pedir a permissão de notificação (Android 13+) só quando a pessoa ativar o lembrete;
  - não usar "alarme exato" (permissão restrita pelo Google Play); alguns minutos de atraso são aceitáveis;
  - versão web: sem notificação confiável → oferecer "Adicionar à agenda" (.ics), que toca pelo app de calendário.

- [ ] **Revisão de segurança** proporcional ao app (ver seção abaixo).

## Decisões em aberto

- [ ] **Nome na loja:** proposta "NutriPen: Diário da Caneta" (26 caracteres), com "caneta
  emagrecedora" na descrição curta e na descrição completa (evitar no nome: risco de reprovação
  e de parecer promessa de resultado). Trocar "GLP-1/GIP" por "caneta" nos textos que o usuário
  lê dentro do app; manter o termo técnico no relatório. *Aguardando confirmação.*

## Já sugeridas anteriormente

- [ ] Ver e editar registros de dias anteriores (refeições, check-ins).
- [ ] Editar registros já salvos (hoje só dá para excluir e registrar de novo).
- [ ] Favoritos e "repetir ontem" nas refeições.
- [ ] Cadastrar alimentos próprios na tabela.
- [ ] Sintomas × dias após a aplicação (padrão de náusea/constipação).
- [ ] Estoque da caneta (doses restantes, quando comprar).
- [ ] Lembrete da aplicação via calendário (.ics).
- [ ] Tela de sinais de alerta (pancreatite, vesícula, desidratação).
- [ ] Exames laboratoriais (HbA1c, B12, ferritina, vitamina D) no relatório.
- [ ] Resumo semanal de adesão.
- [ ] Mover a política de privacidade para outro endereço antes de tornar o repositório privado.
- [ ] Futuro: "NutriPen IA" (análise de foto) como assinatura opcional.

## Revisão de segurança (checklist)

O NutriPen não tem servidor, login nem internet na versão Android — a superfície de ataque é pequena,
mas ainda há pontos a verificar antes de publicar:

- [ ] **Importação de backup:** arquivo malicioso não pode executar código (XSS) nem travar o app
      (tamanho, campos inesperados, textos com HTML). Testes automatizados com arquivos "envenenados".
- [ ] **Escapar textos** digitados pelo usuário em todas as telas e no relatório.
- [ ] **Política de segurança de conteúdo (CSP)** na versão da loja: proibir scripts externos e conexões.
- [ ] **Android:** permissões (nenhuma), componentes exportados, FileProvider, depuração do WebView
      desligada em produção, backup automático do Android (decidir se fica ligado).
- [ ] **Dependências:** `npm audit` e versões fixas.
- [ ] **GitHub:** secrets da chave de assinatura, permissões mínimas do workflow, ações fixadas por versão
      exata (hash), proteção da branch main.
- [ ] **Versão web (testadores):** chave do Gemini guardada no navegador — aviso claro e nunca no backup.

