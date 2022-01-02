from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

ss_url = 'https://w6.seg-social.es/ProsaInternetAnonimo/OnlineAccess?ARQ.SPM.ACTION=LOGIN&ARQ.SPM.APPTYPE=SERVICE&ARQ.IDAPP=XV106001'

def send_email(ImgFileName):
    with open(ImgFileName, 'rb') as f:
        img_data = f.read()

    msg = MIMEMultipart()
    msg['Subject'] = 'Disponibilidad para citas SS'
    msg['From'] = 'youremail@gmail.com'
    msg['To'] = 'user1@hotmail.com,user2@gmail.com'

    text = MIMEText("Pantallazo con citas disponibles")
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
    msg.attach(image)

    # SMTP server
    server=smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("youremail@gmail.com","yourpass")

    # Send 
    server.sendmail(msg['From'], msg["To"].split(","), msg.as_string())
    server.quit()

    print('Email sent')

def convierte_cifra(numero,sw):
    lista_centana = ["",("CIEN","CIENTO"),"DOSCIENTOS","TRESCIENTOS","CUATROCIENTOS","QUINIENTOS","SEISCIENTOS","SETECIENTOS","OCHOCIENTOS","NOVECIENTOS"]
    lista_decena = ["",("DIEZ","ONCE","DOCE","TRECE","CATORCE","QUINCE","DIECISEIS","DIECISIETE","DIECIOCHO","DIECINUEVE"),
                    ("VEINTE","VEINTI"),("TREINTA","TREINTA Y "),("CUARENTA" , "CUARENTA Y "),
                    ("CINCUENTA" , "CINCUENTA Y "),("SESENTA" , "SESENTA Y "),
                    ("SETENTA" , "SETENTA Y "),("OCHENTA" , "OCHENTA Y "),
                    ("NOVENTA" , "NOVENTA Y ")
                ]
    lista_unidad = ["",("UN" , "UNO"),"DOS","TRES","CUATRO","CINCO","SEIS","SIETE","OCHO","NUEVE"]
    centena = int (numero / 100)
    decena = int((numero -(centena * 100))/10)
    unidad = int(numero - (centena * 100 + decena * 10))
    #print "centena: ",centena, "decena: ",decena,'unidad: ',unidad

    texto_centena = ""
    texto_decena = ""
    texto_unidad = ""

    #Validad las centenas
    texto_centena = lista_centana[centena]
    if centena == 1:
        if (decena + unidad)!=0:
            texto_centena = texto_centena[1]
        else :
            texto_centena = texto_centena[0]

    #Valida las decenass
    texto_decena = lista_decena[decena]
    if decena == 1 :
        texto_decena = texto_decena[unidad]
    elif decena > 1 :
        if unidad != 0 :
            texto_decena = texto_decena[1]
        else:
            texto_decena = texto_decena[0]
    #Validar las unidades
    #print "texto_unidad: ",texto_unidad
    if decena != 1:
        texto_unidad = lista_unidad[unidad]
        if unidad == 1:
            texto_unidad = texto_unidad[sw]

    return "%s %s %s"%(texto_centena,texto_decena,texto_unidad)

def numero_to_letras(numero):
	indicador = [("",""),("MIL","MIL"),("MILLON","MILLONES"),("MIL","MIL"),("BILLON","BILLONES")]
	entero = int(numero)
	contador = 0
	numero_letras = ""
	while entero >0:
		a = entero % 1000
		if contador == 0:
			en_letras = convierte_cifra(a,1).strip()
		else :
			en_letras = convierte_cifra(a,0).strip()
		if a==0:
			numero_letras = en_letras+" "+numero_letras
		elif a==1:
			if contador in (1,3):
				numero_letras = indicador[contador][0]+" "+numero_letras
			else:
				numero_letras = en_letras+" "+indicador[contador][0]+" "+numero_letras
		else:
			numero_letras = en_letras+" "+indicador[contador][1]+" "+numero_letras
		numero_letras = numero_letras.strip()
		contador = contador + 1
		entero = int(entero / 1000)

	return numero_letras.strip().replace(' ','').capitalize() if not numero_letras.startswith(('TREINTA Y', 'CUARENTA Y')) else numero_letras.strip().capitalize()

def fill_form(driver):
    # Name
    elem = driver.find_element_by_xpath('//*[@id="nombre"]')
    elem.send_keys('#pon aqui tu nombre')
    sleep(0.2)

    # Document type
    select = Select(driver.find_element_by_xpath('//*[@id="tipo"]'))
    select.select_by_visible_text("NIF")
    sleep(0.2)

    # Fill DNI
    elem = driver.find_element_by_xpath('//*[@id="ipfnumero"]')
    elem.send_keys('#pon aqui tu dni')
    sleep(0.2)

    # Fill Phone number
    elem = driver.find_element_by_xpath('//*[@id="telefono"]')
    elem.send_keys('#pon aqui tu num de telefono')
    sleep(0.2)

    # Select appointment type
    elem = driver.find_element_by_xpath('//*[@id="radioDiaHoraProvincia"]').click()
    sleep(0.2)

    # Select province
    select = Select(driver.find_element_by_xpath('//*[@id="provincia1"]'))
    select.select_by_visible_text('MALAGA')
    sleep(0.2)

    # Put email
    elem = driver.find_element_by_xpath('//*[@id="email"]')
    elem.send_keys('youremail@gmail.com')
    sleep(0.2)

if __name__ == '__main__':
    try:
        driver = webdriver.Chrome(executable_path=r'/absolutepathtochromedriver/chromedriver')
        driver.get(ss_url)

        sleep(1)

        # Obtener portal SS
        elem = driver.find_element_by_xpath('//*[@id="SELECCIONAR1"]').click()

        sleep(1)

        for i in range(10):
            # Checkear captcha numerico
            elem = driver.find_element_by_xpath('//*[@id="ARQcapaPrincipal"]/fieldset/p[1]')
            captcha_text = elem.text.split()
            operation = captcha_text[len(captcha_text) - 1].strip()

            result = set(operation).intersection(set(['+','-','x','/']))
            if result:
                print('Captcha is numeric. Solving ...')
                result = eval(operation.replace('x', '*'))
                final_captcha = numero_to_letras(result)

                # Fill captcha
                elem = driver.find_element_by_xpath('//*[@id="ARQ.CAPTCHA"]')
                elem.send_keys(final_captcha)

                sleep(0.5)

                # Fill form
                fill_form(driver)

                # Click next
                elem = driver.find_element_by_xpath('//*[@id="SPM.ACC.SIGUIENTE"]').click()
                sleep(2)

                # Select "Pensiones" and "Siguiente"
                elem = driver.find_element_by_xpath('//*[@id="335"]').click()
                sleep(0.2)
                elem = driver.find_element_by_xpath('//*[@id="SPM.ACC.CONTINUAR_TRAS_SELECCIONAR_SERVICIO"]').click()
                sleep(2)

                # Verify if there is appointment available
                try:
                    table = driver.find_element_by_xpath('//*[@id="ARQcapaPrincipal"]/fieldset/div[2]/table')
                    driver.execute_script("document.body.style.zoom = '0.5'")
                    driver.save_screenshot('screenshot.png')
                    send_email('screenshot.png')
                    sleep(120)
                    break
                except NoSuchElementException:
                    print('There are no appointments now')
                    sleep(10)
                    break

            else:
                print('Captcha is not numeric. Retrying ...')
                driver.refresh()
                sleep(2)

    except Exception as excp:
        print('Unexpected error' + str(excp))
    finally:
        driver.close()