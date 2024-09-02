# bsky_follow_script.py by luizatheworld

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

# Defina o caminho para o Edge WebDriver (substitua pelo caminho no seu computador)
edge_driver_path = "caminho/para/seu/edgedriver/msedgedriver.exe"

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
username_input.send_keys("seu_username")

# Preencha o campo de senha (substitua pela sua senha)
password_input = driver.find_element(By.XPATH, "//input[@aria-label='Password']")
password_input.send_keys("sua_senha")

# Envie o formulário de login
password_input.send_keys(Keys.RETURN)

# Aguarde até que o botão "Profile" esteja visível e clicável
profile_button = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Profile']"))
)
profile_button.click()

# Aguarde a navegação para a página do perfil (substitua pelo seu username)
WebDriverWait(driver, 15).until(
    EC.url_contains("/profile/seu_username")
)

# Navegue para a página de "Followers" clicando no link
followers_link = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.XPATH, "//a[@data-testid='profileHeaderFollowersButton']"))
)
followers_link.click()

# Função para verificar e clicar em "Follow" se necessário
def check_and_follow():
    follow_count = 0  # Contador para o número de follows
    last_height = driver.execute_script("return document.body.scrollHeight")  # Altura inicial da página
    total_profiles = 0  # Contador para o número total de perfis percorridos

    while True:
        # Role a página para baixo
        driver.execute_script("window.scrollBy(0, 10000);")  # Rolagem mais rápida
        time.sleep(1)  # Menos tempo de espera para carregamento

        # Encontre todos os elementos de perfil
        profile_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'css-175oi2r r-1awozwy r-18u37iz')]")

        if not profile_elements:
            break  # Se não houver perfis na página, saia do loop

        for profile in profile_elements:
            # Verifique se "Follows You" está presente e se o botão de follow está disponível
            try:
                profile.find_element(By.XPATH, ".//div[text()='Follows You']")
                follow_button = profile.find_element(By.XPATH, ".//button//div[contains(text(), 'Follow')]")
                if follow_button and "Follow" in follow_button.text:
                    # Extraia o nome de usuário
                    username_element = profile.find_element(By.XPATH, ".//a[contains(@href, '/profile/')]")
                    username = username_element.get_attribute("href").split("/")[-1]
                    
                    # Execute o follow
                    follow_button.click()
                    follow_count += 1
                    total_profiles += 1
                    print(f"Follow realizado em @{username}")
                    time.sleep(1)
            except:
                continue  # Se o botão "Follow" não for encontrado ou já foi seguido, continue

        # Verifique se a página foi rolada até o fim
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # Se a altura da página não mudou, você chegou ao final

        last_height = new_height  # Atualize a altura da página

    # Informe o número de follows realizados e o total de perfis únicos percorridos
    print(f"Follow realizado em {follow_count} perfil(is).")

# Execute a função para verificar e clicar em "Follow"
check_and_follow()

# Registrar o tempo de fim
end_time = time.time()

# Calcular o tempo total de execução
execution_time = end_time - start_time
print(f"Tempo total de execução: {execution_time:.2f} segundos")

# Mantenha o navegador aberto por 1 minuto (60 segundos)
time.sleep(60)

# Feche o navegador após a pausa
driver.quit()
