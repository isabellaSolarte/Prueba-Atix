from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from anticaptchaofficial.imagecaptcha import *
from selenium.webdriver.support import expected_conditions as EC
import base64
import time
import requests


# Configuración del navegador
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
navegador = webdriver.Chrome(options=chrome_options)
navegador.maximize_window()

navegador.get("https://www.adres.gov.co/consulte-su-eps")
navegador.implicitly_wait(2)

frame = navegador.find_element(By.ID, "MSOPageViewerWebPart_WebPartWPQ3")
navegador.switch_to.frame(frame)

selector_tipo_doc = Select(navegador.find_element(By.XPATH, '//*[@id="tipoDoc"]'))
selector_tipo_doc.select_by_value("CC")

# Ingreso del número de documento
campo_num_doc = navegador.find_element(By.XPATH, '//*[@id="txtNumDoc"]')
campo_num_doc.send_keys('1002777704')

# Resolver el captcha
captcha_resuelto = False
while not captcha_resuelto:
    try:
        # Capturar la imagen del captcha
        imagen_captcha = navegador.find_element(By.XPATH, '//*[@id="Capcha_CaptchaImageUP"]')
        # Script de JavaScript
        imagen_captcha_guardada = navegador.execute_async_script("""
                var ele = arguments[0], callback = arguments[1];
                ele.addEventListener('load', function fn(){
                    ele.removeEventListener('load', fn, false);
                    var cnv = document.createElement('canvas');
                    cnv.width = this.width; cnv.height = this.height;
                    cnv.getContext('2d').drawImage(this, 0, 0);
                    callback(cnv.toDataURL('image/jpeg').substring(22));
                }, false);
                 ele.dispatchEvent(new Event('load'));
              """, imagen_captcha)

        with open(r"captcha.jpg", 'wb') as archivo_captcha:
            archivo_captcha.write(base64.b64decode(imagen_captcha_guardada))

        solver = imagecaptcha()
        solver.set_verbose(0)
        solver.set_key('a59d40aabee57e96838a4f338b2aca1d')
        solver.set_soft_id(0)
        # Resuelve el captcha y lo guarda en una variable
        texto_captcha = solver.solve_and_return_solution("captcha.jpg")
        print(texto_captcha)
        # Verifica que se haya resuelto correctamente el captcha
        if texto_captcha != 0:
            print("Captcha resuelto: " + texto_captcha)
            # Envía el captcha al input
            navegador.find_element(By.XPATH, '//*[@id="Capcha_CaptchaTextBox"]').send_keys(texto_captcha)
            navegador.find_element(By.XPATH, '//*[@id="btnConsultar"]').click()
            captcha_resuelto = True
        else:
            captcha_resuelto = False
            time.sleep(2)
    except Exception as e:
        print(f"Volviendo a intentar el captcha debido a: {e}")
        time.sleep(2)

# Esperar la apertura de una la nueva pestaña que es el resultado
WebDriverWait(navegador, 10).until(EC.number_of_windows_to_be(2))

# Cambiar al nuevo handle de la pestaña
for handle in navegador.window_handles:
    if handle != navegador.current_window_handle:
        navegador.switch_to.window(handle)
        break

time.sleep(5)

# Usar el comando de DevTools para guardar la página como PDF
opciones_impresion = {
    'paperWidth': 8.27,
    'paperHeight': 11.69,
    'marginTop': 0,
    'marginBottom': 0,
    'marginLeft': 0,
    'marginRight': 0,
    'printBackground': True
}

respuesta = navegador.execute_cdp_cmd('Page.printToPDF', opciones_impresion)
datos_pdf = base64.b64decode(respuesta['data'])

# Guardar el PDF en un archivo
with open("resultado.pdf", "wb") as archivo_pdf:
    archivo_pdf.write(datos_pdf)
print("Página guardada como resultado.pdf")
navegador.quit()
