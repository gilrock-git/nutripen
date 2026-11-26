# NutriPen na Google Play — roteiro passo a passo

App: **NutriPen: Diário da Caneta** · pacote `br.com.nutripen.app` · **pago, R$ 14,90** · conta **pessoal**

> As telas do Play Console mudam com frequência. Os nomes abaixo podem variar um pouco;
> quando algo não bater, procure pelo assunto (ex.: "Segurança dos dados").

---

## Etapa 0 — Contas (uma vez só)

1. **Conta de desenvolvedor**: play.google.com/console → criar conta **pessoal** → pagar a taxa única (US$ 25) → verificar identidade (documento com foto), e-mail e telefone.
2. **Perfil de pagamentos** (obrigatório para vender): Play Console → *Configurar → Perfil de pagamentos* → dados bancários e fiscais. Sem ele, a opção "Pago" fica bloqueada.
3. **E-mail de suporte**: use um e-mail só para o app (ex.: criar `nutripen.app@gmail.com`). Ele aparece publicamente na loja.

## Etapa 1 — Chave de assinatura no GitHub (uma vez só)

Abra **github.com/gilrock-git/nutripen/settings/secrets/actions** → *New repository secret* e cadastre os 4 valores do arquivo `SECRETS-GITHUB.txt`:

| Name | Secret |
|---|---|
| `NUTRIPEN_KEYSTORE_BASE64` | conteúdo inteiro de `keystore-base64.txt` |
| `NUTRIPEN_KEYSTORE_PASSWORD` | senha do arquivo |
| `NUTRIPEN_KEY_ALIAS` | `nutripen-upload` |
| `NUTRIPEN_KEY_PASSWORD` | mesma senha |

Depois: *Actions → Android (Google Play) → Run workflow*. Ao terminar, baixe o artefato `nutripen-android-N` (zip) — dentro estão:
- `nutripen-play.aab` → para enviar ao Google Play
- `nutripen-teste.apk` → para instalar direto no seu celular e conferir antes
- `versao.txt` → deve dizer `assinado para a Play Store: true`

**Guarde o `.jks` e as senhas** (Drive pessoal + gerenciador de senhas). Se perder, dá para pedir ao Google a troca da chave de envio, mas leva alguns dias.

## Etapa 2 — Criar o app

*Todos os apps → Criar app*
- Nome: **NutriPen: Diário da Caneta**
- Idioma padrão: **Português (Brasil)**
- App ou jogo: **App** · Gratuito ou pago: **Pago** (⚠️ não dá para mudar de gratuito para pago depois)
- Aceitar as declarações.

## Etapa 3 — Conteúdo do app (*Política → Conteúdo do app*)

| Item | Resposta |
|---|---|
| Política de privacidade | `https://gilrock-git.github.io/nutripen/privacidade.html` |
| Acesso ao app | Todas as funções estão disponíveis sem acesso especial |
| Anúncios | **Não** contém anúncios |
| Classificação do conteúdo | Categoria "Todos os outros tipos de app"; responda **Não** a violência, sexo, drogas, apostas, interação entre usuários, compartilhamento de localização. Compras digitais: **Não** (o app é pago na loja, sem compras dentro dele) |
| Público-alvo | **18 anos ou mais** (só essa faixa) |
| App de notícias | Não |
| Apps de saúde (declaração) | Marque as funções que mais se aproximam: *nutrição/controle de peso*, *gerenciamento de medicamentos/tratamento*, *acompanhamento de condições (glicemia)*. Informe que **não é dispositivo médico** e que não faz diagnóstico |
| Apps governamentais / financeiros | Não |

### Segurança dos dados
- O app coleta ou compartilha algum dos tipos de dados exigidos? → **Não**
  (tudo fica no aparelho; o app não tem permissão de internet; compartilhar relatório/backup é ação do próprio usuário, com o app que ele escolher)
- Resultado na loja: **"Nenhum dado coletado"** e **"Nenhum dado compartilhado com terceiros"**.
- A permissão de **notificações** (lembrete) não muda essas respostas: os lembretes são agendados no próprio celular.
- O app **não** usa "alarme exato" — não há declaração de permissão de alarme a fazer.

## Etapa 4 — Página da loja (*Crescer → Presença na loja → Página principal*)

**Nome:** NutriPen: Diário da Caneta (26 caracteres; o limite é 30)

**Descrição curta (até 80 caracteres):**
> Para quem usa caneta emagrecedora: proteína, água, peso e dia da aplicação.

**Descrição completa:**
> Para quem usa caneta emagrecedora (Mounjaro, Ozempic, Wegovy, Saxenda e outras): o NutriPen é o seu diário da caneta. Ele ajuda você a comer proteína suficiente, se hidratar, acompanhar o peso e não esquecer a aplicação — tudo em um só lugar.
>
> METAS CALCULADAS PARA VOCÊ
> • Proteína, água, fibras e calorias a partir de idade, sexo, peso, altura e atividade física
> • Ajustes automáticos para diabetes/pré-diabetes, bariátrica, sem vesícula, refluxo, hipertensão, pós-operatório e idade acima de 60 anos
> • Tetos de carboidrato e gordura com alertas por refeição
>
> REGISTRO RÁPIDO
> • Montador de prato e tabela com 50 alimentos brasileiros (com porção ajustável)
> • Botões rápidos de proteína, água e fibras
> • Peso, cintura, abdômen, braço e coxa, com gráficos
> • Glicemia capilar com alertas de hipo e hiperglicemia
>
> CANETA E SINTOMAS
> • Lembrete no dia da aplicação (e na véspera), no horário que você escolher
> • Doses fracionadas e intervalo do seu jeito: semanal, a cada 10 ou 14 dias
> • Contagem para a próxima aplicação, aviso de atraso e sugestão de rodízio do local
> • Diário de evacuação e sintomas (náusea, refluxo, empachamento) com dicas práticas
>
> RELATÓRIO PARA A CONSULTA
> • Resumo para médico ou nutricionista: evolução, titulação de dose, glicemia, tolerância e adesão
> • Compartilhe por WhatsApp ou e-mail com um toque
>
> PRIVACIDADE DE VERDADE
> • Sem cadastro, sem anúncios, sem rastreamento
> • Funciona 100% offline: seus dados ficam só no seu celular
> • Backup quando você quiser
>
> Importante: o NutriPen é uma ferramenta de apoio e não substitui a orientação do seu médico ou nutricionista. Doses só devem ser alteradas pelo médico.

**Imagens** (arquivos já prontos):
- Ícone 512×512: `icone-512.png`
- Imagem de destaque 1024×500: `destaque-1024x500.png`
- Capturas de tela do telefone (2 a 8): `01-hoje.png` … `06-relatorio.png`

**Categoria:** Saúde e fitness · **Tags:** saúde, nutrição, controle de peso
**Contato:** o e-mail de suporte da Etapa 0

> ⚠️ Não use "Mounjaro", "Ozempic" ou "Wegovy" no nome, ícone ou descrição curta (marcas de terceiros). Na descrição completa, como referência de uso, costuma ser aceito.
> ⚠️ Evite "emagrecedora" no **nome** (pode soar como promessa de resultado); na descrição está ok.

## Etapa 5 — Preço

*Monetizar → Produtos → Preço do app* → **R$ 14,90** → aplicar a todos os países ou só ao Brasil (recomendado no início: **só Brasil**, em *Alcance → Países/regiões*).

## Etapa 6 — Teste fechado (obrigatório para conta pessoal nova)

1. *Testar e lançar → Teste fechado → Criar faixa* → enviar o `nutripen-play.aab` → nota da versão ("Primeira versão de teste").
2. *Testadores*: crie uma lista com os e-mails Google de **pelo menos 12 pessoas** (sugestão: 15, para ter folga).
3. Envie a eles o **link de participação** da faixa. Cada um precisa aceitar o convite e **instalar pela Play Store**.
4. *Configurações → Teste de licença*: adicione os mesmos e-mails para que **não precisem pagar**. (Se alguém acabar pagando, você pode reembolsar em *Gestão de pedidos*.)
5. Os 12 precisam continuar inscritos por **14 dias seguidos**. Peça que abram o app de vez em quando e mandem sugestões.

## Etapa 7 — Produção

Depois dos 14 dias, o Console libera *Painel → Solicitar acesso à produção* (perguntas sobre o teste: quem testou, o que mudou). Aprovado:
1. *Produção → Criar versão* → enviar um `.aab` **novo** (cada envio precisa de versão nova — o GitHub Actions já aumenta o número sozinho a cada execução).
2. Enviar para revisão. Costuma levar de 1 a 7 dias.

## Depois de publicado

- **Atualizar o app**: edite → o GitHub gera um novo `.aab` → *Produção → Criar versão*.
- **Torne o repositório privado** só depois de mover a política de privacidade para outro endereço (o GitHub Pages gratuito para quando o repositório fica privado — e a loja exige o link funcionando).
- **Impostos**: os pagamentos do Google vêm do exterior; confirme com seu contador (carnê-leão como pessoa física).
