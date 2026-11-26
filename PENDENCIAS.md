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
