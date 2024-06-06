# Prueba-Atix

## Proyecto: Automatización de Obtención de Certificados de EPS
### Descripción General
La empresa Atix Digital S.A.S necesita obtener los certificados de la EPS de varios usuarios para confirmar datos personales en sus bases de datos y validar la identidad de las personas. Para realizar este trabajo de manera óptima y eficiente, se requiere una solución automática para la obtención de dichos certificados.

### Objetivo
El objetivo del proyecto es desarrollar un RPA (Robotic Process Automation) que realice las siguientes tareas:

- Ingresar a la URL: https://www.adres.gov.co/consulte-su-eps.
- Digitar el tipo y el número de identificación de una persona y realizar la verificación CAPTCHA del sitio.
- Guardar la respuesta en formato PDF o en un archivo HTML.
## Requerimientos
- Automatización de Navegación: Utilizar un RPA para acceder a la página web especificada.
- Ingreso de Datos: Automatizar la digitación del tipo y número de identificación.
- Verificación CAPTCHA: Resolver el CAPTCHA presente en la página web.
- Almacenamiento de Resultados: Guardar la respuesta obtenida en formato PDF o HTML.
## Tecnologías Utilizadas
- Python: Lenguaje de programación principal para desarrollar el RPA.
- Selenium: Biblioteca para la automatización de navegadores web.
Anti-CAPTCHA API: Servicio para resolver CAPTCHA automáticamente.
