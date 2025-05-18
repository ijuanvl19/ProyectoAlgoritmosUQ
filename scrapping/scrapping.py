
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv


load_dotenv()


def donwloadDataIEE():

    # TODO: cambiar la ruta de descarga dependiendo del sistema
    # operativo winndows o mac os cada ruta depdende de donde almaceno el proyecto
    # Cambia a la ruta correcta#
    download_dir = r"E:\celuweb\ProyectoAlgoritmosUQ\assets\IEEE"

    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,  # Carpeta de descargas
        "download.prompt_for_download": False,  # No mostrar cuadros de diálogo
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        # Deshabilitar ventanas emergentes para descargas
        "profile.default_content_settings.popups": 0
    })

    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=chrome_options)

    # Abrir la página
    driver.get("https://ieeexplore-ieee-org.crai.referencistas.com/search/searchresult.jsp?newsearch=true&queryText=computational%20thinking")

    # Espera implícita para cargar elementos de la página
    # driver.implicitly_wait(10)

    # Buscar y hacer clic en el botón para iniciar sesión con Google
    element = driver.find_element(by=By.ID, value="btn-google")
    element.click()

# Buscar el campo de correo electrónico
    element = driver.find_element(by=By.ID, value="identifierId")
    element.send_keys(os.getenv('EMAIL'))


# Hacer clic en el botón "Siguiente"
    element = driver.find_element(by=By.ID, value="identifierNext")
    element.click()

    time.sleep(4)
    element = driver.find_element(
        By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
    element.send_keys(os.getenv('PSWD'))
# Hacer clic en el botón "Siguiente"2
    element = driver.find_element(
        by=By.XPATH, value='//*[@id="passwordNext"]/div/button')
    element.click()

    driver.implicitly_wait(10)

# results_per_page_100 = driver.find_element(By.CSS_SELECTOR, "a[data-aa-name='srp-100-results-per-page']")
# results_per_page_100.click()

    time.sleep(25)

    total_results_span = driver.find_element(
        By.XPATH, "(//span[@class='strong'])[2]")
# Extraer el texto del elemento
    total_results = total_results_span.text.replace(",", "")

    max_pages = int(total_results)/25
    i = 1

    while i <= int(max_pages):
        checkbox = driver.find_element(
            By.CLASS_NAME, 'results-actions-selectall')
        checkbox.click()

        export_btn = driver.find_element(
            By.XPATH, '//*[@id="xplMainContent"]/div[1]/div[1]/ul/li[3]/xpl-export-search-results')
        export_btn.click()
        if i == 1:
            citation_btn = driver.find_element(
                By.XPATH, '//*[@id="ngb-nav-0"]')
            citation_btn.click()

        time.sleep(4)

        radio_button = driver.find_element(
            By.CSS_SELECTOR, "label[for='download-bibtex'] input")
        radio_button.click()

        radio_type = driver.find_element(
            By.CSS_SELECTOR, "label[for='citation-abstract'] input")
        radio_type.click()

        download_button = driver.find_element(
            By.CSS_SELECTOR, "button.stats-SearchResults_Citation_Download")
        download_button.click()

        time.sleep(4)

    #  Localizar el ícono
        close_icon = driver.find_element(By.CSS_SELECTOR, "i.fas.fa-times")

    # Usar JavaScript para forzar el clic en el ícono
        driver.execute_script("arguments[0].click();", close_icon)
        print('cerrando ventana')
        close_icon = driver.find_element(By.CSS_SELECTOR, "i.fas.fa-times")

        close_icon.click()

        try:
            next_button = driver.find_element(
                By.XPATH, "//button[contains(text(), '>')]")

    # Hacer clic en el botón "Next"
            next_button.click()
        except:
            print('No hay mas paginas')
            break
        i += 1
        time.sleep(4)

    time.sleep(20)


def download_sage_articles():
    # TODO: cambiar la ruta de descarga dependiendo del sistema
    # operativo winndows o mac os cada ruta depdende de donde almaceno el proyecto

    # Cambia a la ruta correcta#
    download_dir = r"E:\celuweb\ProyectoAlgoritmosUQ\assets\sage"

    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,  # Carpeta de descargas
        "download.prompt_for_download": False,  # No mostrar cuadros de diálogo
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        # Deshabilitar ventanas emergentes para descargas
        "profile.default_content_settings.popups": 0
    })

    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=chrome_options)


# Abrir la página
    driver.get("https://journals-sagepub-com.crai.referencistas.com/action/doSearch?field1=AllField&text1=computational+thinking&field2=AllField&text2=&Ppub=&access=user&startPage=1&pageSize=200&AfterYear=1950&BeforeYear=2025&queryID=2%2F4707166868")

# Espera implícita para cargar elementos de la página
# driver.implicitly_wait(10)

# Buscar y hacer clic en el botón para iniciar sesión con Google
    element = driver.find_element(by=By.ID, value="btn-google")
    element.click()

# Buscar el campo de correo electrónico
    element = driver.find_element(by=By.ID, value="identifierId")
    element.send_keys(os.getenv('EMAIL'))


# Hacer clic en el botón "Siguiente"
    element = driver.find_element(by=By.ID, value="identifierNext")
    element.click()

    time.sleep(5)
    driver.implicitly_wait(10)

    element = driver.find_element(
        By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
    element.send_keys(os.getenv('PSWD'))
# Hacer clic en el botón "Siguiente"2
    element = driver.find_element(
        by=By.XPATH, value='//*[@id="passwordNext"]/div/button')
    element.click()

    driver.implicitly_wait(10)
    time.sleep(5)

# Localizar el elemento que contiene el número total de resultados (95214) por su clase
    result_count_element = driver.find_element(
        By.CSS_SELECTOR, "span.result__count")

# Obtener el texto que contiene el número
    result_count = result_count_element.text

# max_pages = int(result_count)/100
    i = 0
    max_retries = 10  # Número máximo de reintentos por página
    try:
        while i < 250:
            try:
                checkbox = driver.find_element(By.ID, "action-bar-select-all")

            # Asegurarse de que el checkbox esté marcado
                while not checkbox.is_selected():
                    checkbox.click()
                    time.sleep(2)

                print("Checkbox marcado.")
                if not checkbox.is_selected():
                    print("Checkbox marcado.")
                    while not checkbox.is_selected():
                        checkbox.click()
                        time.sleep(2)

            # Continuar con el resto del código
                export = driver.find_element(
                    By.CSS_SELECTOR, "a[data-id='srp-export-citations']")
                export.click()

                select_element = driver.find_element(By.ID, "citation-format")
                select = Select(select_element)
                time.sleep(3)
                select.select_by_value("bibtex")

                time.sleep(2)
                try:
                    download_button = driver.find_element(
                        By.CSS_SELECTOR, "a.download__btn")
                    download_button.click()
                except:
                    wait = WebDriverWait(driver, 10)
                    modal = wait.until(EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, "div.modal__header")))

                    close_button = modal.find_element(
                        By.CSS_SELECTOR, "button.close")
                    driver.execute_script(
                        "arguments[0].click();", close_button)

                time.sleep(2)
                wait = WebDriverWait(driver, 10)
                modal = wait.until(EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "div.modal__header")))

                close_button = modal.find_element(
                    By.CSS_SELECTOR, "button.close")
                driver.execute_script("arguments[0].click();", close_button)

                time.sleep(2)

            # Hacer clic en el botón "Next"
                next_button = driver.find_element(
                    By.CSS_SELECTOR, "a[aria-label='next']")
                next_button.click()
                time.sleep(2)

            # Incrementar i solo si la iteración se completa sin errores
                i += 1

            except Exception as e:
                # Manejar la excepción, por ejemplo, registrar el error y reintentar
                print(f"Error en la página {i+1}: {str(e)}. Reintentando...")
                retries = 0
                while retries < max_retries:
                    try:
                        # Intentar nuevamente después del error
                        time.sleep(5)
                        retries += 1
                        break  # Si tiene éxito, salir del bucle de reintentos
                    except Exception as e:
                        print(
                            f"Reintento {retries}/{max_retries} fallido: {str(e)}")

                if retries == max_retries:
                    print(
                        f"No se pudo procesar la página {i+1} después de {max_retries} reintentos. Continuando...")
                    i += 1  # Si no tuvo éxito después de reintentar, aumentar i y continuar
    except Exception as e:
        print(f"Fin de la paginación o error crítico: {str(e)}")


def download_sciense_articles():
    # TODO: cambiar la ruta de descarga dependiendo del sistema
    # operativo winndows o mac os cada ruta depdende de donde almaceno el proyecto

    # Cambia a la ruta correcta#
    download_dir = r"E:\celuweb\ProyectoAlgoritmosUQ\assets\sciense"

    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,  # Carpeta de descargas
        "download.prompt_for_download": False,  # No mostrar cuadros de diálogo
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        # Deshabilitar ventanas emergentes para descargas
        "profile.default_content_settings.popups": 0
    })

    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=chrome_options)


# Abrir la página
    driver.get(
        "https://www-sciencedirect-com.crai.referencistas.com/search?qs=computational%20thinking&show=100")

# Espera implícita para cargar elementos de la página
# driver.implicitly_wait(10)

# Buscar y hacer clic en el botón para iniciar sesión con Google
    element = driver.find_element(by=By.ID, value="btn-google")
    element.click()

    # Buscar el campo de correo electrónico
    element = driver.find_element(by=By.ID, value="identifierId")
    element.send_keys(os.getenv('EMAIL'))

  # Hacer clic en el botón "Siguiente"
    element = driver.find_element(by=By.ID, value="identifierNext")
    element.click()

    time.sleep(5)
    element = driver.find_element(
        By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
    element.send_keys(os.getenv('PSWD'))
# Hacer clic en el botón "Siguiente"2
    element = driver.find_element(
        by=By.XPATH, value='//*[@id="passwordNext"]/div/button')
    element.click()

    driver.implicitly_wait(10)

# results_per_page_100 = driver.find_element(By.CSS_SELECTOR, "a[data-aa-name='srp-100-results-per-page']")
# results_per_page_100.click()

    pagination_info = driver.find_element(
        By.CSS_SELECTOR, "ol#srp-pagination li")

# Extraer el texto del elemento
    pagination_text = pagination_info.text

# Extraer el número máximo de páginas del texto "Page 1 of 60"
# Dividimos la cadena para obtener el número final
    max_pages = pagination_text.split(' ')[-1]

    i = 1

    while i <= int(max_pages):
        # checkbox = driver.find_element(By.ID, "select-all-results")
        label = driver.find_element(
            By.CSS_SELECTOR, "label[for='select-all-results']")

        label.click()
        if i > 1:
            label.click()
    # checkbox.click()

        export_btn = driver.find_element(
            By.XPATH, '//*[@id="srp-toolbar"]/div[1]/span/span[1]/span[2]/div[2]')
        export_btn.click()
        export_button = driver.find_element(
            By.CSS_SELECTOR, "button[data-aa-button='srp-export-multi-bibtex']")
    # Hacer clic en el botón
        export_button.click()
        time.sleep(2)
    # driver.implicitly_wait(5)
        next_button = driver.find_element(
            By.CSS_SELECTOR, 'a[data-aa-name="srp-next-page"]')

# Forzar el clic en el botón "Next" utilizando JavaScript
        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(2)
        i += 1

    time.sleep(40)
