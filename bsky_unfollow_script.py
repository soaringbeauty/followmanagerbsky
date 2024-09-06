# bsky_unfollow_script.py by luizatheworld
# v2.1: ease of use
# requeriments: Python 3.6+, Selenium, Microsoft Edge, Microsoft Edge Webdriver.

# * Extract "msedgedriver.exe" from WebDriver Zip *
# * pip install selenium *

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time

# Defina seus dados de login e caminho do Webdriver
bluesky_username = 'seu usuário'
bluesky_password = 'sua senha'
edge_driver_path = r"C:\NetTools\webdrivers\msedgedriver.exe"

# Configurar o serviço do WebDriver do Edge
service = Service(executable_path=edge_driver_path)

# Iniciar o WebDriver do Edge
driver = webdriver.Edge(service=service)

# Registrar o tempo de início
start_time = time.time()

# Acesse a página inicial do Bsky
driver.get("https://bsky.app/")

# Aguarde até que o botão "Sign in" esteja clicável e clique nele
sign_in_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Sign in']"))
)
sign_in_button.click()

# Preencha o campo de usuário (substitua pelo seu nome de usuário ou e-mail)
username_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Username or email address']"))
)
username_input.send_keys(bluesky_username)

# Preencha o campo de senha (substitua pela sua senha)
password_input = driver.find_element(By.XPATH, "//input[@aria-label='Password']")
password_input.send_keys(bluesky_password)

# Aguarde 1 segundos para garantir que o bot ja tenha preenchido
time.sleep(1)

# Envie o formulário de login
password_input.send_keys(Keys.RETURN)

try:
    # Aguarde até que o botão "Profile" esteja visível e clicável
    profile_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Profile']"))
    )
except TimeoutException:
    print("\033[31mUsuário ou senha incorretos!\033[m")
else:
    profile_button.click()

    # Aguarde a navegação para a página do perfil (substitua pelo seu username)
    WebDriverWait(driver, 15).until(
        EC.url_contains(f"/profile/{bluesky_username}")
    )

    # Navegue para a página de "Following" clicando no link
    following_link = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@data-testid='profileHeaderFollowsButton']"))
    )
    following_link.click()

    # Função para verificar e clicar em "Unfollow" se necessário
    def check_and_unfollow():
        unfollow_count = 0  # Contador para o número de unfollows
        pending_unfollows = set()  # Conjunto para armazenar perfis que devem receber unfollow
        profile_urls = set()  # Conjunto para rastrear URLs de perfis únicos
        last_height = driver.execute_script("return document.body.scrollHeight")  # Altura inicial da página
        total_profiles = 0  # Contador para o número total de perfis percorridos
        try:
            while True:
                # Role a página para baixo
                driver.execute_script("window.scrollBy(0, 10000);")  # Rolagem mais rápida
                time.sleep(1)  # Menos tempo de espera para carregamento

                # Encontre todos os elementos de perfil
                profile_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'css-175oi2r r-1awozwy r-18u37iz')]")

                if not profile_elements:
                    break  # Se não houver perfis na página, saia do loop

                for profile in profile_elements:
                    # Tente capturar o username do perfil
                    try:
                        username_element = profile.find_element(By.XPATH, ".//a[contains(@href, '/profile/')]")
                        username = username_element.get_attribute("href")
                    except:
                        continue  # Se não conseguir capturar o username, continue para o próximo perfil

                    # Se o perfil é novo, adicione ao conjunto de URLs de perfis
                    if username not in profile_urls:
                        profile_urls.add(username)
                        total_profiles += 1  # Incrementa o contador de perfis únicos

                        # Verifique se "Follows You" não está presente
                        try:
                            profile.find_element(By.XPATH, ".//div[text()='Follows You']")
                        except:
                            # Se o texto "Follows You" não for encontrado, considere para unfollow
                            if username not in pending_unfollows:
                                pending_unfollows.add(username)
                                print(f"Perfil a receber unfollow: {username}")

                                # Encontre o botão "Unfollow" e clique
                                try:
                                    unfollow_button = profile.find_element(By.XPATH, ".//button[contains(., 'Unfollow')]")
                                    if unfollow_button:
                                        unfollow_button.click()
                                        unfollow_count += 1
                                        print(f"Unfollow realizado em {username}")
                                        time.sleep(1)  # Aguarde um pouco após o clique
                                except Exception as e:
                                    print(f"Erro ao tentar clicar em Unfollow para {username}: {str(e)}")
                                    pass  # Se o botão "Unfollow" não for encontrado, continue

                # Verifique se a página foi rolada até o fim
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break  # Se a altura da página não mudou, você chegou ao final

                last_height = new_height  # Atualize a altura da página
        # Dita o procedimento a ser executado caso o usuário interrompa o processo
        except KeyboardInterrupt:
            print("Processo encerrado manualmente pelo usuário.")
        # Anuncia um erro inesperado (caso ocorra) e mostra na tela em vermelho
        except Exception as error:
            print(f"Ocorreu um erro inesperado durante a execução:\n \033[31m{error}\033[m")
        # Garante que o programa mostre os resultados finais mesmo que um erro ocorra durante o processo
        finally:
            # Informe o número de unfollows realizados e o total de perfis únicos percorridos
            print(f"Unfollow realizado em {unfollow_count} perfil(is).")
            print(f"Número total de perfis únicos percorridos: {total_profiles}")

if __name__ == "__main__":
    try:
        # Execute a função para verificar e clicar em "Unfollow"
        check_and_unfollow()
    # Garante que o trecho de encerramento ocorra mesmo que haja um erro inesperado durante a execução
    finally:
        # Registrar o tempo de fim
        end_time = time.time()

        # Calcular o tempo total de execução
        execution_time = end_time - start_time
        print(f"Tempo total de execução: {execution_time:.2f} segundos")

        # Mantenha o navegador aberto por 1 minuto (60 segundos)
        time.sleep(60)

        # Feche o navegador após a pausa
        driver.quit()
