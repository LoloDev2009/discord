from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# ---------- SCRAPER ----------
def scrapear(url):
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1, 1)     # Tamaño pequeño
    driver.get(url)
    time.sleep(5)
    precio_descuento = ''
    descuento = ''
    precio_original = ''
    estado = ''
    try:
        nombre = driver.find_element(By.CSS_SELECTOR, "h1.text-2xl").text
    except:
        nombre = "SIN NOMBRE"

    try:
        bloque_precio = driver.find_element(By.ID, "product-price").text.strip()
        partes = bloque_precio.split('\n')

        if len(partes) >= 3:
            # Caso con descuento
            precio_original = partes[0]
            precio_descuento = partes[1]
            descuento = partes[2]
        else:
            # Caso sin descuento, buscar campos alternativos
            precio_original = bloque_precio
            try:
                precio_descuento = driver.find_element(By.ID, "product-price-por").text.strip()
            except:
                precio_descuento = "notFound"
            try:
                descuento = driver.find_element(By.ID, "product-price-desconto").text.strip()
            except:
                descuento = "notFound"
    except:
        
    # En caso de que siga siendo 'notFound', se intenta por separado
        if precio_descuento == "notFound":
            try:
                precio_descuento = driver.find_element(By.ID, "product-price-por").text.strip()
            except:
                pass

        if descuento == "notFound":
            try:
                descuento = driver.find_element(By.ID, "product-price-desconto").text.strip()
            except:
                pass


        try:
            boton_agregar = driver.find_element(By.XPATH, "//button[contains(., 'agregar a mi bolsa')]")
            estado = "Disponible" if boton_agregar.is_enabled() else "No disponible"
        except:
            estado = "No disponible"


    print(precio_original,precio_descuento)
    if precio_original:
        precio_original = precio_original.replace('$','')
        precio_original = precio_original.replace(' ','')
        precio_original = precio_original.replace('.','')
        precio_original = precio_original.replace(',','.')
        precio_original = float(precio_original)

    if precio_descuento != 'notFound' and precio_descuento != '':
        precio_descuento = precio_descuento.replace('$','')
        precio_descuento = precio_descuento.replace(' ','')
        precio_descuento = precio_descuento.replace('.','')
        precio_descuento = precio_descuento.replace(',','.')
        precio_descuento = float(precio_descuento)
    
    if descuento.count('\n'):
        descuento = descuento.split('\n')[1]
        descuento = descuento.replace('-','')
        descuento = descuento.replace('%','')
        descuento = float(descuento)
    elif descuento:
        descuento = descuento.replace('-','')
        descuento = descuento.replace('%','')
        descuento = descuento.replace(' ','')
        descuento = descuento.replace('etiqueta','')
        descuento = float(descuento)

    if precio_original:
        porcentaje = validarPorcentaje(precio_original,precio_descuento,descuento)
    else: porcentaje = 'Agotado'
    if porcentaje == 'True':
        datosProducto = {
            "nombre": nombre,
            "precio_original": precio_original,
            "precio_descuento": precio_descuento,
            "descuento": descuento,
            "estado": estado,
        }
    elif porcentaje == 'False':
        datosProducto = {
            "nombre": nombre,
            "precio_original": precio_original,
            "precio_descuento": None,
            "descuento": None,
            "estado": estado,
        }
    else: datosProducto = {}

    driver.quit()
    print("🎉 Scraping completo con toda la página cargada.")
    return datosProducto

def validarPorcentaje(precio_original, precio_descuento, porcentaje_descuento):
    # Calcular el descuento en plata a partir del porcentaje
    descuento_calculado = precio_original * (porcentaje_descuento / 100)
    
    # Calcular el precio que debería quedar después del descuento
    precio_calculado = precio_original - descuento_calculado
    
    # Verificar que el precio con descuento que te pasaron sea cercano al calculado
    if abs(precio_descuento - precio_calculado) > 0.01:  # tolerancia de 1 centavo
        print(f"El precio con descuento no coincide. Esperado: {precio_calculado}, dado: {precio_descuento}")
        return 'False' 
    else:
        print("El descuento y precio con descuento son consistentes.")
        return 'True'
    