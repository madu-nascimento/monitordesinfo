# 🕵️‍♀️ CheckPost – Monitor de Desinformação

**CheckPost** é uma ferramenta desenvolvida para auxiliar repórteres de verificação de fatos na identificação de possíveis pautas e no monitoramento de conteúdos publicados por perfis que frequentemente disseminam desinformação, especialmente sobre temas como política e saúde.

## 🛠️ Como funciona

O script, desenvolvido em **Python**, utiliza a biblioteca **Selenium** para automatizar o acesso a perfis no Instagram. A coleta é feita por meio de uma conta de dedicada ao projeto e realiza as seguintes ações:

- Acessa automaticamente **13 perfis selecionados**
- Coleta as **postagens publicadas no dia**
- Extrai as seguintes informações de cada post:
  - 📆 Data e hora da publicação  
  - ✍️ Legenda  
  - 🖼️ Imagem da postagem ou **capa do vídeo (reel/post)**  
  - ❤️ Número de curtidas  
  - 👁️ Número de visualizações (em desenvolvimento)  
  - 🔗 Link direto da postagem

Todas essas informações são organizadas em um **arquivo `.csv`**, que pode ser facilmente aberto no Google Sheets para facilitar a navegação e leitura dos conteúdos.

---

## 🧩 Por que essa ferramenta é útil?

Embora ainda seja necessário acessar os links manualmente para leitura completa, o **CheckPost** oferece vantagens importantes:

- Agiliza o processo de ronda ao evitar a checagem manual de perfil em perfil;
- Centraliza informações relevantes para avaliar o potencial desinformativo de publicações;
- Facilita a identificação de temas que estão sendo impulsionados;
- Permite identificar:
  - Assuntos com **potencial de viralização**
  - Perfis associados em postagens conjuntas
  - Oportunidades de aplicar **estratégias de prebunking** (abordar temas antes que mentiras se espalhem)

---

## 🚧 Próximos passos

O **CheckPost** ainda está em fase de desenvolvimento. Algumas funcionalidades futuras já estão planejadas para tornar a ferramenta ainda mais útil:

- [ ] Capturar corretamente o número de **visualizações de vídeos e reels**
- [ ] Adicionar alertas para:
  - 🚨 **Palavras-chave sensíveis**
  - 🔥 Postagens com **alto engajamento (curtidas/visualizações)**
- [ ] Automatizar a execução do script usando GitHub Actions, permitindo que o monitor rode automaticamente 1 ou 2 vezes por dia

### 📚 Sobre o projeto

Projeto final do **Master em Jornalismo de Dados, Automação e Data Storytelling** do **Insper**.
