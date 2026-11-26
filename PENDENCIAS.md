# NutriPen — pendências e ideias

Lista de melhorias anotadas para as próximas versões. Marque com [x] quando concluir.

## Pedidas pelo usuário (prioridade)

- [x] **Doses fracionadas.** Hoje a dose é escolhida numa lista fixa por medicação
  (ex.: tirzepatida 2,5 / 5 / 7,5 mg…). Permitir doses intermediárias, como as usadas
  ao fracionar a caneta (ex.: 1,25 mg, 3,75 mg, 6 mg):
  - campo de dose livre em mg (com vírgula), mantendo a lista como atalho;
  - opcional: registrar em "cliques/unidades" da caneta multidose, com conversão para mg;
  - gráficos, titulação no relatório e marcadores de troca de dose devem aceitar esses valores.
  - Telas afetadas: Meu Perfil, Iniciar perfil, Aplicação (Diário) e Peso (Medidas).

- [x] **Intervalo entre aplicações configurável.** Nem sempre é 1x por semana — no fim do
  tratamento é comum espaçar (ex.: a cada 10, 14 dias). Hoje o app só tem "dia da semana".
  - No perfil: **intervalo em dias** (7 por padrão; aceitar qualquer valor) em vez de só o dia da semana;
  - próxima aplicação = **data da última aplicação + intervalo** (contagem e aviso de atraso
    passam a usar esse intervalo);
  - ao registrar uma aplicação, poder informar a dose **e** o intervalo até a próxima
    (o intervalo pode mudar ao longo do tratamento);
  - relatório: mostrar a evolução de dose **e** de intervalo (ex.: "5 mg a cada 7 dias → 5 mg a cada 14 dias").

- [x] **Alarme / lembrete da aplicação.** Hoje o app só mostra a contagem quando é aberto.
  - Versão Android: notificação local agendada (plugin `@capacitor/local-notifications`), que
    funciona sem internet e não altera a "Segurança dos dados";
  - lembrete no dia, no horário escolhido (ex.: 9h), e opcional na véspera à noite;
  - reagendar sozinho ao registrar uma aplicação ou mudar o intervalo (depende do item acima);
  - pedir a permissão de notificação (Android 13+) só quando a pessoa ativar o lembrete;
  - não usar "alarme exato" (permissão restrita pelo Google Play); alguns minutos de atraso são aceitáveis;
  - versão web: sem notificação confiável → oferecer "Adicionar à agenda" (.ics), que toca pelo app de calendário.

- [x] **Revisão de segurança** proporcional ao app (ver seção abaixo).

- [x] **"Esqueci a aplicação" — orientação para dose atrasada.** Quando a aplicação passar da data
  (o app já mostra "Aplicação atrasada há X dias"), exibir uma dica acolhedora e um botão/chave
  "Esqueci a aplicação" com a orientação da bula da caneta em uso. Tom: *"Acontece. Na maioria dos
  casos não atrapalha o tratamento — veja o que fazer."*
  - **Regras a confirmar na bula vigente (ANVISA) antes de implementar** — resumo do que consta nas bulas:
    - **Tirzepatida (Mounjaro):** aplicar assim que lembrar, **se faltarem até 4 dias (96 h)** desde a dose
      esquecida; passou de 4 dias → **pular** e aplicar no próximo dia programado. Entre duas doses,
      no mínimo **3 dias (72 h)**.
    - **Semaglutida — Ozempic:** aplicar assim que lembrar **em até 5 dias**; passou disso → pular.
    - **Semaglutida — Wegovy:** se faltarem **mais de 2 dias** para a próxima dose, aplicar; se menos → pular.
    - **Liraglutida (Saxenda, diária):** não dobrar; seguir no dia seguinte. **Mais de 3 dias sem aplicar** →
      falar com o médico (pode ser preciso reiniciar a dose mais baixa).
    - **Todas:** nunca aplicar duas doses para "compensar". **2 semanas ou mais** sem aplicar → falar com o
      médico antes de voltar (risco de enjoo forte ao retomar a mesma dose).
    - **Intervalo personalizado pelo médico** (ex.: 10 ou 14 dias): mostrar "siga a orientação do seu médico"
      em vez da regra da bula.
  - Ao tocar em "Já apliquei", registrar com a data real; ao escolher "Vou pular", registrar a dose pulada
    (aparece no relatório para o médico) e recalcular a próxima data.
  - O lembrete (notificação) de atraso passa a trazer essa orientação resumida.

- [x] **Ciclo menstrual (opcional, só para perfil feminino).** No cadastro e em Meu Perfil, para quem marcou
  sexo feminino: "Quer acompanhar o ciclo menstrual?" (desligado por padrão).
  - Campos: data de início da última menstruação e duração média do ciclo (padrão 28 dias); opções
    "não menstruo / menopausa / uso contínuo de anticoncepcional" para desligar.
  - No Diário: chip rápido "🩸 Menstruada hoje" / "TPM" no check-in.
  - **Acolhimento:** nos dias pré-menstruais e menstruais, se o peso subir, mostrar mensagem como
    *"Nesses dias é comum reter líquido e o peso subir 0,5 a 2 kg. Não é gordura — olhe a tendência das
    próximas semanas."* Marcar esses dias no gráfico de peso (faixa rosa clara) e não tratar a alta como
    "piora" nos cartões.
  - Dica da Nutri no período: reduzir sal, manter água, proteína e fibras; inchaço e vontade de doce são esperados.
  - Relatório (opcional): indicar quais pesagens caíram no período pré-menstrual.
  - **Lembrete de segurança a confirmar na bula:** a tirzepatida pode reduzir o efeito do **anticoncepcional
    oral** no início do tratamento e a cada aumento de dose (a bula orienta método de barreira ou não oral por
    4 semanas). Exibir esse aviso para mulheres em idade fértil que usam tirzepatida.
  - Privacidade: dado sensível de saúde — fica só no aparelho, como o resto; mencionar na política.

- [ ] **Termo "glicemia capilar".** Avaliar trocar no app por "Glicemia (medida no dedo)" e manter
  "glicemia capilar" só no relatório para o médico. *Aguardando decisão.*

- [x] **Tela limpa e "árvore" para abrir contextos (redesenho de navegação).** Mostrar só o essencial e
  abrir detalhes sob demanda (seções que expandem ▸), lembrando o que a pessoa deixou aberto.
  - **Hoje:** saudação, cartão da próxima aplicação e só 3 metas (proteína, água, fibras) com "Ver todas
    as metas ▸"; Dica da Nutri em 1 linha que expande; checklist resumido ("4/6 ▸"); contabilidade clínica
    vai para Meu Perfil.
  - **Botão "+" flutuante** com registro rápido: peso, água, refeição, glicemia, atividade, sintoma, aplicação.
  - **Diário:** linhas que abrem — Peso ▸ · Aplicação ▸ · Evacuação e sintomas ▸ · Lembrete ▸ · Linha do tempo ▸.
  - **Medidas:** abas internas Peso | Medidas | Glicemia | Exames, cada uma com gráfico e "Registrar ▸".
  - **Refeições:** resumo do dia no topo; "Registrar refeição ▸", "Montador ▸", "Diário de hoje (3) ▸".

- [x] **Diário em primeiro lugar.** É a tela usada todos os dias: deve ser a primeira da navegação e a tela
  inicial do app, fácil de achar e rápida de preencher (registrar em 1–2 toques).

- [x] **Lembretes de água.** Opcional: avisar a cada X horas (ex.: de 2 em 2 h, das 8h às 20h) com quanto
  falta para a meta; parar sozinho quando a meta do dia for batida; não avisar à noite. No Android, notificação
  local (mesmo mecanismo do lembrete da aplicação); na web, só o lembrete visual ao abrir o app.

- [x] **Atividade física.** Registro simples por dia: *Não pratiquei* / *Caminhada* / *Musculação* /
  *Outra*, com minutos opcionais.
  - Meta semanal de referência (OMS): **150 min de atividade moderada + 2 dias de força**; mostrar progresso
    da semana. Destacar **musculação/força** (protege a massa magra durante o emagrecimento com a caneta).
  - Substitui o item "Treino de força / caminhada" do checklist; entra no relatório (média semanal).
  - Se o padrão real ficar diferente do "nível de atividade" do perfil, sugerir atualizar (muda a meta de calorias).

- [x] **Exames com gráfico de evolução.** Condições novas no cadastro: **colesterol alto** e **gordura no
  fígado**. Área "Exames" (dentro de Medidas): data + valores de HbA1c, glicemia de jejum (laboratório),
  colesterol total, LDL, HDL, triglicerídeos; opcionais TGO/TGP, vitamina D, B12, ferritina, creatinina.
  Gráfico por exame com faixa de referência geral (meta individual é do médico) e tabela "antes → agora"
  no relatório.

- [x] **Bulas: só resumos com fonte (decidido).** Não guardar a bula no app. Para cada caneta:
  - resumos curtos do que importa no momento (ex.: dose esquecida, anticoncepcional), sempre com
    *"Fonte: bula [nome] — ANVISA, versão de [data]. Verifique se há atualização."*;
  - botão "📄 Ver bula oficial" que abre o **Bulário Eletrônico da ANVISA** no navegador (sempre atualizado);
  - guardar no código a data da versão consultada e revisar os resumos a cada nova versão da bula.

- [x] **Central de avisos (sininho 🔔 no topo).** Todos os avisos vão para um só lugar, com contador, para a
  tela não ficar poluída: comprar/encomendar a caneta, consulta agendada, agendar a próxima consulta, aplicação
  atrasada, exame a refazer, fazer backup. Avisos importantes também podem virar notificação no celular.

- [x] **Estoque da caneta.** Informar quantas doses tem a caneta (ou cliques) e quantas restam; avisar no sininho
  quando faltarem ~2 aplicações para dar tempo de encomendar.

- [x] **Consultas.** Agenda simples: médico, nutricionista e "Outro profissional" (campo livre); data/hora e
  local; aviso na véspera e no dia; após a consulta, lembrar de **agendar a próxima** (ex.: "Sua última consulta
  com a nutricionista foi há 30 dias"). Lista "Perguntar ao médico" ligada à próxima consulta.
  - Decisão: não criar telas específicas para educador físico ou psicólogo (foco do app); o campo livre atende.

- [x] **Fome e saciedade × dias após a aplicação.** Registro diário de 1 a 5 (1 toque). Gráfico "fome por dia
  do ciclo da caneta" (dia 1, 2, 3… após a aplicação) para a pessoa perceber se a fome volta antes da próxima dose;
  entra no relatório para o médico ajustar dose/intervalo.

- [x] **Contador de dias de tratamento.** Mostrar no Diário, perto da saudação: *"Você está no 15º dia de
  tratamento"*.
  - Data de início = primeira aplicação registrada; campo "Comecei o tratamento em" no cadastro/perfil para
    quem começou antes de usar o app (editável).
  - Marcos com mensagem de incentivo (30, 60, 90 dias, 6 meses, 1 ano), com resumo do período: peso e medidas
    desde o início, semanas com a meta de proteína batida.
  - Se houver pausa longa (ex.: semanas sem aplicação), perguntar se a pessoa retomou e permitir recomeçar a
    contagem ou manter a data original.
  - Entra no relatório: "Tempo de tratamento: 15 dias (desde 12/11/2026)".

### Aprovadas para o futuro (26/11/2026)
- [x] "O que comer agora?" — sugestões de lanches que fecham a proteína/fibra que falta no dia.
- [x] Visão do mês (calendário) com aplicações, peso, sintomas, atividade e fome.
- [x] Lista "Perguntar ao médico" (entra no relatório).
- [x] Tamanho de letra ajustável (acessibilidade).
- [x] Fotos de progresso (só no aparelho).
- [x] Fase de manutenção: acompanhar o peso ao espaçar/parar a caneta e avisar com delicadeza se voltar a subir.
- [x] Resumo da semana com conquistas, em tom de incentivo.
- [x] Navegação em 5 abas: **Diário (tela inicial)** · Refeições · Evolução · Caneta · Mais.

## Decisões em aberto

- [x] **Nome na loja:** proposta "NutriPen: Diário da Caneta" (26 caracteres), com "caneta
  emagrecedora" na descrição curta e na descrição completa (evitar no nome: risco de reprovação
  e de parecer promessa de resultado). Trocar "GLP-1/GIP" por "caneta" nos textos que o usuário
  lê dentro do app; manter o termo técnico no relatório. *Confirmado e aplicado (26/11/2026).*

## Já sugeridas anteriormente

- [ ] Ver e editar registros de dias anteriores (refeições, check-ins).
- [ ] Editar registros já salvos (hoje só dá para excluir e registrar de novo).
- [ ] Favoritos e "repetir ontem" nas refeições.
- [ ] Cadastrar alimentos próprios na tabela.
- [ ] Sintomas × dias após a aplicação (padrão de náusea/constipação).
- [ ] Estoque da caneta (doses restantes, quando comprar).
- [x] Lembrete da aplicação via calendário (.ics).
- [ ] Tela de sinais de alerta (pancreatite, vesícula, desidratação).
- [ ] Exames laboratoriais (HbA1c, B12, ferritina, vitamina D) no relatório.
- [ ] Resumo semanal de adesão.
- [ ] Mover a política de privacidade para outro endereço antes de tornar o repositório privado.
- [ ] Futuro: "NutriPen IA" (análise de foto) como assinatura opcional.

## Revisão de segurança (checklist)

O NutriPen não tem servidor, login nem internet na versão Android — a superfície de ataque é pequena,
mas ainda há pontos a verificar antes de publicar:

- [x] **Importação de backup:** arquivo malicioso não pode executar código (XSS) nem travar o app
      (tamanho, campos inesperados, textos com HTML). Testes automatizados com arquivos "envenenados".
- [x] **Escapar textos** digitados pelo usuário em todas as telas e no relatório.
- [x] **Política de segurança de conteúdo (CSP)** na versão da loja: proibir scripts externos e conexões.
- [x] **Android:** permissões (nenhuma), componentes exportados, FileProvider, depuração do WebView
      desligada em produção, backup automático do Android (decidir se fica ligado).
- [x] **Dependências:** `npm audit` e versões fixas.
- [x] **GitHub:** secrets da chave de assinatura, permissões mínimas do workflow, ações fixadas por versão
      exata (hash), proteção da branch main.
- [x] **Versão web (testadores):** chave do Gemini guardada no navegador — aviso claro e nunca no backup.

### Resultado da revisão (26/11/2026)

- **Corrigido — execução de código via backup adulterado:** IDs de registros iam para atributos
  `onclick` (o escape HTML não protege nesse contexto) e datas eram exibidas sem escape. Agora todo
  campo importado passa por validação estrita (IDs, datas, horas, números em faixas, textos com limite).
- **Corrigido — troca da chave da IA por backup:** a chave do Gemini nunca é lida de arquivo importado.
- **Adicionado — CSP** nas duas versões: a loja não conecta em nada; a web só nas fontes do Google e no Gemini.
- **Android:** sem internet; permissões só de notificação/reinício (lembrete); alarme exato removido;
  1 componente exportado (tela principal); depuração do WebView desligada; backup automático do Android
  mantido (documentado na política de privacidade).
- **Dependências:** `npm audit` sem vulnerabilidades. **Workflow:** actions fixadas por hash, permissão só de leitura.
- **Testes:** `testes/seguranca.js` (15 verificações) roda no GitHub antes de gerar o app; a versão anterior às
  correções reprova em 9 delas.
- **Pendente (ação do dono do repositório):** proteger a branch `main` em Settings → Branches.

## Versão 1.2 (26/11/2026) — implementado
Diário como tela inicial (5 abas, seções que expandem, botão +, sininho de avisos), contador de dias de
tratamento, fome × dia do ciclo, atividade física com meta semanal, lembrete de água (Android), "o que comer
agora", exames com gráficos, consultas e perguntas, estoque da caneta, dose esquecida com resumo da bula e
opção de pular, aviso de anticoncepcional (tirzepatida), ciclo menstrual com acolhimento no peso, calendário do
mês, fotos de progresso (só no aparelho), tamanho de letra, aviso de reganho na manutenção e resumo da semana.

### Revisão da 1.2 (26/11/2026) — corrigido
- **Aplicação atrasada:** "Já apliquei" agora faz a próxima voltar ao dia de sempre (respeitando o intervalo
  mínimo da bula) e não muda o intervalo do tratamento; no histórico aparece "aplicada com atraso".
- **Estoque da caneta:** excluir uma aplicação devolve a dose; "Desfazer" desconta de novo.
- **Semaglutida:** com atraso, o aviso separa Ozempic (até 5 dias) e Wegovy (pular se faltarem 2 dias ou menos).
- **Datas automáticas:** data e hora do check-in, peso, refeição e aplicação acompanham a virada do dia
  (app aberto de um dia para o outro); o que a pessoa digitou é respeitado.
- **Zerar perfil** apaga também as fotos guardadas no aparelho.
- Backup na versão Android registra a data (o aviso "faça backup" some); exames na mesma data são somados;
  fome no "dia da aplicação"; ciclo da fome conta só doses aplicadas; toque na notificação abre a aba certa;
  letra maior aplicada antes de a tela aparecer; perfil não aceita início do tratamento no futuro.
- `build_pwa.py` recusa pasta de saída que contenha o repositório (ela é apagada no build).

### A conferir antes de publicar na loja
- [ ] **Bulas:** confirmar os resumos (dose esquecida, anticoncepcional, sinais de alerta) com a versão vigente
  de cada bula no Bulário da ANVISA e registrar a **data da versão** em `BULA_INFO` (hoje o app mostra
  "confira a data da versão vigente").
- [ ] **Links do Bulário:** conferir se o formato `consultas.anvisa.gov.br/#/bulario/q/?nomeProduto=...` abre a
  busca certa no celular.
- [ ] Faixas de referência dos exames: validar com a nutricionista/médico parceiro.


## Ideias anotadas (26/11/2026) — para depois

### Versão 1.3 (26/11/2026) — implementado
- [x] **"Senti fome" com horário** e intensidade, no cartão da fome e no botão "+".
- [x] **Refeição "fora do plano"**, com motivo opcional (fome, evento, vontade, emoção, sem opção), marcada ao
  salvar ou depois pela bandeira; texto acolhedor ("sem culpa").
- [x] **Diário da semana para a nutricionista:** no relatório nutricional, a linha do tempo de cada dia
  (refeições e fome com horários, itens fora do plano), mais o resumo:
  - quantas refeições saíram do plano e por quê;
  - horário mais frequente de fome;
  - tempo médio entre sentir fome e comer.
  
  Na tela de Refeições há um atalho para esse relatório.
- [x] **Plano alimentar e receitas (PDF ou foto)** em Mais:
  - os arquivos ficam só no aparelho, fora do backup;
  - foto abre dentro do app; PDF abre no leitor do celular;
  - botão para enviar o arquivo (WhatsApp etc.);
  - receita com validade e aviso no sininho 7 dias antes de vencer.
- [x] Corrigido: o botão "voltar" do Android ainda usava a aba antiga "hoje". Ele nunca saía do app e não
  fechava o painel de avisos.
- [ ] *Opcional:* no Android, o PDF abre pelo menu "Abrir com…". Para mostrar direto no leitor padrão, dá para
  usar o plugin `@capacitor-community/file-opener` (versão 8.0.1). Adicionar uma dependência nova precisa de
  autorização.

### Outros idiomas e países
- Ordem sugerida: **espanhol** (América Latina e Espanha) → **inglês** (EUA, Reino Unido, Canadá, Austrália) →
  francês / alemão / italiano.
- O que adaptar:
  - todos os textos do app em arquivo de tradução;
  - unidades: lb, mmol/L (glicemia e colesterol), HbA1c em mmol/mol (Reino Unido), datas e números;
  - tabela de alimentos e nomes das refeições de cada país;
  - nomes comerciais e resumo da bula pela agência local (FDA, EMA, COFEPRIS…);
  - telefone de emergência (192 → 911/112);
  - faixas de referência dos exames;
  - política de privacidade por lei: GDPR na Europa; leis estaduais de dados de saúde nos EUA;
  - página na Play Store, imagens e preço em cada idioma e país.

## Pedidos de 26/11/2026 (tarde) — para a próxima versão

### Refeições (a parte que mais precisa simplificar)
- [x] **Nome da tela:** "Refeições & Scanner" → **"Refeições"**.
- [x] **IA:** escrever só "IA" (sem citar Gemini) e permitir outros provedores no futuro.
  - Na versão da loja ela continua desligada, porque o app promete não usar internet.
- [ ] **Registrar tocando em botões, sem precisar digitar:**
  - botões com comidas básicas e genéricas, ex.: bife, frango, peixe, ovo, carne moída, porco, arroz, feijão,
    macarrão, batata, salada, legumes, pão, queijo, iogurte, fruta, **sobremesa, doce**;
  - porção como pouco / médio / muito, em vez de gramas;
  - **"+ adicionar item"** para pôr mais de uma coisa na mesma refeição;
  - [x] **calorias e proteína opcionais** (feito na 1.4): hoje são obrigatórias e travam o registro; o app estima pelos botões ou
    deixa em branco.
- [ ] **Velocidade ao comer:** rápido / normal / devagar. Com a caneta, comer rápido costuma causar enjoo, então
  é útil para a nutricionista.
- [ ] **Montador rápido** com mais opções genéricas ("bife" em vez de só "filé mignon").
- [ ] **Sair sem salvar:** o registro aberto pelo "+" precisa de um botão para fechar/cancelar sem preencher nada.
- [ ] **"O que comer agora"** vira "Sugestões para completar o dia":
  - acrescentar o botão "Comi outra coisa", que abre os botões de comida;
  - opção "Sigo o cardápio da nutricionista", que esconde as sugestões e mostra só quanto falta de proteína,
    fibras e água.
- [x] **Telas longas:** botão "↑" para voltar ao topo, que aparece ao rolar. Era o menu superior.

### Dia a dia
- [x] **Atividades:** acrescentar **bicicleta**, e também corrida, natação/hidroginástica, dança, pilates/yoga.
- [ ] **Dia de festa:** um botão que marca o dia como festa. O app:
  - não trata o dia como "falha";
  - dá dicas (proteína primeiro, comer devagar, beber água, cuidado com álcool e enjoo);
  - registra no relatório.
- [ ] **Bebida alcoólica** (opcional): quantas doses no dia. É relevante com a caneta: enjoo, calorias e risco de
  hipoglicemia em quem usa remédio para diabetes.
- [ ] **Cigarro** como condição no perfil (fumante / ex-fumante), não como registro diário. Opcional, sem
  julgamento.
- [ ] **Jejum intermitente e outras rotinas alimentares** (opcional; a mensagem do usuário veio cortada em "vamos considerar que a pessoa pode…" — confirmar): registrar a janela de alimentação.
  - Mostrar o aviso: "combine com seu médico/nutricionista", porque com a caneta aumenta o risco de pouca
    proteína e de hipoglicemia em diabéticos.
  - O app não incentiva o jejum.
- [ ] **Peso e medidas:** tirar o campo "manhã / tarde / noite" (o horário já diz isso). Manter só "em jejum? sim
  / não".
- [ ] **Glicemia capilar:** simplificar a tela:
  - valor + momento (jejum, antes de comer, 2 h depois, ao deitar) e cor da faixa;
  - aparece só para quem marcou diabetes ou pré-diabetes, ou ativa por conta própria.

### Caneta, exames e registros
- [ ] **Editar qualquer registro** (aplicação, refeição, peso, glicemia, exame, consulta) em vez de apagar e
  refazer. Ex.: incluir depois o local da primeira aplicação.
- [ ] **Estoque também para frasco com seringa:** total em mg (ex.: 10 mg) menos a dose (2,5 mg), dá quantas
  aplicações restam.
  - O app só faz a conta; não orienta preparo nem diluição.
  - Medicamento manipulado é tema regulatório sensível na ANVISA; não promover.
- [ ] **Mais exames:**
  - o HDL já existe entre os 6 principais; os demais ficam em "Outros exames" — deixar isso mais visível;
  - acrescentar: hemograma (hemoglobina), insulina e HOMA-IR, TSH, ácido úrico, ureia, potássio, sódio, PCR,
    ácido fólico, zinco, GGT, fosfatase alcalina, amilase/lipase.

### Navegação e relatório
- [ ] **Ordem do menu:** primeiro um **Resumo** com os meus dados (nome, dias de tratamento, próxima dose, peso,
  metas), depois o **Diário**, depois os demais, e **Evolução por último**.
- [x] **Relatório com gráficos coloridos** (peso, proteína, água, fome × ciclo, glicemia, exames), também na impressão/PDF; dá para desligar.
  No Android o app não imprime, então os gráficos aparecem só na tela.
- [x] **Formatos do relatório:** "Consulta nutricional" primeiro, "Consulta médica" depois.
- [x] **Aviso de que as informações são só recomendações** no topo do relatório, logo abaixo da identificação.

### Estilo alimentar (pedido de 26/11/2026)
- [ ] No perfil, escolher o estilo alimentar (pode marcar mais de um): onívoro, vegetariano, vegano, low carb,
  sem glúten, sem lactose, jejum intermitente.
  - **Vegetariano / vegano:** é o que mais muda, porque bater a meta de proteína fica mais difícil.
    - Sugestões e montador sem carne (tofu, lentilha, grão-de-bico, ervilha, proteína de soja, whey vegano).
    - Lembrete de vitamina B12 para o vegano.
  - **Low carb / cetogênica:** ajusta o teto de carboidratos exibido. Aviso: com a caneta e remédios para
    diabetes há risco de hipoglicemia; combinar com o profissional.
  - **Sem glúten / sem lactose:** filtra a tabela, o montador e as sugestões.
  - **Jejum intermitente:** janela de alimentação, com aviso (ver acima).

### Versão em inglês (testador na Europa)
- **Testadora:** trabalha em Luxemburgo e mora na França. Nos dois países a emergência é 112 (na França também
  15, SAMU) e a bula oficial é a da EMA. Exames: Luxemburgo costuma usar mg/dL; laboratórios franceses
  costumam mostrar glicemia e colesterol em g/L (1,00 g/L = 100 mg/dL), então aceitar mg/dL, g/L e mmol/L.
  Falta saber **qual caneta** ela usa.
- Precisa saber o **país** do testador (unidades da glicemia e do colesterol, telefone de emergência) e **qual
  caneta** ele usa.
- Caminho mais barato para um testador: uma cópia do link de teste em inglês (ex.: `.../nutripen/en/`), com os
  textos traduzidos, a bula citada pela EMA (agência europeia), emergência 112, alimentos genéricos e a política
  de privacidade em inglês (GDPR).
- Depois, se o mercado se confirmar, montar a estrutura de tradução de verdade, para manter as duas línguas.
