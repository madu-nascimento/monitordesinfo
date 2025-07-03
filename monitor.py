from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import random
import pandas as pd
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()
usuario = os.getenv("INSTAGRAM_USUARIO")
senha = os.getenv("INSTAGRAM_SENHA")

# Lista de perfis para monitorar
perfis = [
    "dicas___naturais",
    "anti_bolsonarismo",
    "patriotaprasempre",
    "despertandoleoesoficial",
    "drdavirodrigues",
    "zeballos59",
    "nicolaspix",
    "direitalivremito",
    "anistia_ja_",
    "ademaraguiar_oficial",
    "eita_faz_o_l",
    "nordestinoconservador",
    "emagrecendo.saudavelmenteaqui",
]

# Inicializa o navegador
navegador = webdriver.Chrome()
wait = WebDriverWait(navegador, 20)

# Acessa a página de login do Instagram
navegador.get("https://www.instagram.com/accounts/login/")
time.sleep(random.uniform(8, 12))

# Preenche usuário e senha
input_usuario = wait.until(EC.presence_of_element_located((By.NAME, "username")))
input_senha = navegador.find_element(By.NAME, "password")
input_usuario.send_keys(usuario)
input_senha.send_keys(senha)
input_senha.send_keys(Keys.ENTER)

# Aguarda login
time.sleep(random.uniform(12, 18))

dados = []

# Percorre todos os perfis
for perfil in perfis:
    try:
        url = f"https://www.instagram.com/{perfil}/"
        navegador.get(url)
        time.sleep(random.uniform(8, 12))

        # Coleta os links dos posts
        post_links = navegador.find_elements(By.TAG_NAME, "a")
        post_urls = [
            link.get_attribute("href")
            for link in post_links
            if link.get_attribute("href")
            and (
                "/p/" in link.get_attribute("href")
                or "/reel/" in link.get_attribute("href")
            )
        ]

        if post_urls:
            posts_validos = []

            for post_url in post_urls[:8]:
                try:
                    navegador.get(post_url)
                    time.sleep(random.uniform(2, 4))

                    html = navegador.page_source
                    soup = BeautifulSoup(html, "html.parser")

                    # Extrai a data da publicação
                    time_tag = soup.find("time")
                    data_publicacao = (
                        time_tag.get("datetime")
                        if time_tag
                        else "0000-00-00T00:00:00.000Z"
                    )

                    # Extrai a legenda
                    try:
                        legenda_tag = soup.find("h1", class_="_ap3a")
                        if legenda_tag:
                            legenda = legenda_tag.get_text(separator="\n").strip()
                        else:
                            meta_tag = soup.find("meta", property="og:description")
                            legenda = (
                                meta_tag["content"].strip()
                                if meta_tag
                                else "Legenda não encontrada"
                            )
                    except:
                        legenda = "Erro ao extrair legenda"

                    # Extrai a imagem ou capa de vídeo
                    try:
                        # Primeiro tenta usar a meta tag 'og:image', que traz a thumbnail ou imagem principal
                        meta_img = soup.find("meta", property="og:image")
                        if meta_img and meta_img.get("content"):
                            imagem_url = meta_img["content"]
                        else:
                            # Fallback para caso a meta não esteja disponível
                            img_tags = soup.find_all("img", alt=True)
                            imagem_url = "Imagem não encontrada"
                            for img in img_tags:
                                src = img.get("src")
                                alt = img.get("alt", "").lower()
                                if src and "scontent" in src and "profile" not in src:
                                    imagem_url = src
                                    break
                    except:
                        imagem_url = "Erro ao extrair imagem"

                    # Extrai visualizações e curtidas
                    try:
                        visualizacoes = "Não encontrado"
                        curtidas = "Não encontrado"

                        # Primeiro tenta identificar visualizações
                        for span in soup.find_all("span"):
                            texto = span.get_text(strip=True).lower()
                            if "visualiz" in texto or "views" in texto:
                                visualizacoes = span.get_text(strip=True)
                                break

                        # Agora tenta identificar curtidas sem confundir com comentários
                        # Busca spans dentro de divs ou seções que contenham 'curtidas'
                        candidatos = soup.select("section span, div span")
                        for span in candidatos:
                            texto = span.get_text(strip=True)
                            texto_lower = texto.lower()

                            # Ignora spans com texto longo ou que mencionam comentários
                            if (
                                len(texto) < 15
                                and "coment" not in texto_lower
                                and "resposta" not in texto_lower
                                and "visualiz" not in texto_lower
                                and (
                                    texto.replace(".", "").replace(",", "").isdigit()
                                    or "mil" in texto_lower
                                    or "k" in texto_lower
                                )
                            ):
                                curtidas = texto
                                break
                    except:
                        visualizacoes = "Erro ao extrair visualizações"
                        curtidas = "Erro ao extrair curtidas"

                    posts_validos.append(
                        {
                            "perfil": perfil,
                            "link": post_url,
                            "data": data_publicacao,
                            "legenda": legenda,
                            "imagem": imagem_url,
                            "visualizacoes": visualizacoes,
                            "curtidas": curtidas,
                        }
                    )

                except Exception as e:
                    print(f"Erro ao processar o post {post_url}: {e}")

            # Função que retorna a data de um post
            def pega_data(post):
                return post["data"]

            # Adiciona todos os posts publicados no dia atual
            if posts_validos:
                posts_hoje = []

                for post in posts_validos:
                    try:
                        data_post = datetime.fromisoformat(
                            post["data"].replace("Z", "+00:00")
                        ).date()
                        if data_post == datetime.today().date():
                            posts_hoje.append(post)
                    except Exception as e:
                        print(f"Erro ao comparar datas: {e}")

                if posts_hoje:
                    dados.extend(posts_hoje)
                else:
                    # Caso não tenha nenhum post do dia, adiciona o mais recente
                    post_mais_recente = max(posts_validos, key=pega_data)
                    dados.append(post_mais_recente)

        else:
            print(f"Nenhum post encontrado no perfil {perfil}")
            dados.append(
                {
                    "perfil": perfil,
                    "link": "Nenhum post encontrado",
                    "legenda": "",
                    "imagem": "",
                    "visualizacoes": "",
                    "curtidas": "",
                }
            )

        # Intervalo aleatório entre perfis para evitar bloqueios
        time.sleep(random.uniform(10, 20))

    except Exception as erro:
        print(f"Erro ao processar o perfil {perfil}: {erro}")
        dados.append(
            {
                "perfil": perfil,
                "link": "Erro ao acessar perfil",
                "legenda": str(erro),
                "imagem": "Erro ao acessar imagem",
                "visualizacoes": "",
                "curtidas": "",
            }
        )

# Encerra o navegador
navegador.quit()

# Exporta os dados para CSV
df = pd.DataFrame(dados)
df.to_csv("instagram_posts_completo.csv", index=False)

print("Coleta finalizada. Dados salvos em 'instagram_posts_completo.csv'.")
