from flask import Flask, render_template, request, jsonify
from datetime import datetime
import requests
import csv
import os

app = Flask(__name__)

# ========================================================
# CONFIGURACIÓN DEL CLIMA Y RUTA DEL DOCUMENTO DEFINITIVA
# ========================================================
API_KEY = "d03feba7e9e5a419f3c4e6d26f351f55" 
# Nombre exacto de tu archivo CSV convertido
CSV_FILE_PATH = "Pokedex_Nayarit.csv"  

def obtener_clima_tepic():
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q=Tepic,MX&appid={API_KEY}&units=metric&lang=es"
        respuesta = requests.get(url)
        datos = respuesta.json()

        if respuesta.status_code != 200:
            print(f"Error de la API: {datos.get('message', 'Error desconocido')}")
            return "¡Szzzt! Mis sensores no pueden conectarse al satélite del clima en este momento... ¡Revisa tu conexión!"

        temperatura = datos["main"]["temp"]
        descripcion = datos["weather"][0]["description"]
        
        # Guardamos el ID del clima para detectar lluvia (Códigos 5xx son lluvia, 3xx llovizna, 2xx tormenta)
        clima_id = datos["weather"][0]["id"]
        es_lluvioso = (300 <= clima_id <= 599) or "lluvia" in descripcion or "llovizna" in descripcion

        mensaje_clima = f"¡Szzzt! ¡Mis sensores climáticos reportan que la temperatura actual en Tepic es de {temperatura}°C con {descripcion}, Entrenador!"
        
        # INTERACCIÓN BASADA EN EL CLIMA (EFECTO POKÉDEX)
        if es_lluvioso:
            mensaje_clima += "<br><br>🌧️ ¡ALERTA! ¡Está lloviendo! Mis algoritmos detectan que la humedad ha aumentado drásticamente la probabilidad de avistar Pokémon de tipo <strong>Agua</strong> en los manglares de La Tovara o Marismas Nacionales, como <strong>Wooper</strong> o <strong>Lotad</strong>. ¡Prepara tus Net Balls! ¡Szzzt!"
        
        return mensaje_clima

    except Exception as e:
        print(f"Error de conexión o código: {e}")
        return "¡Szzzt! Hubo un cortocircuito en mis sistemas y no pude obtener el clima de Tepic."

# ========================================================
# LECTURA DINÁMICA DE LA POKÉDEX DE NAYARIT (ULTRA BLINDADA)
# ========================================================
def obtener_pokemons_nayarit():
    # Aseguramos la ruta absoluta para que Flask siempre encuentre el archivo en su misma carpeta
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_limpia = os.path.join(directorio_actual, CSV_FILE_PATH.strip())
    
    if not os.path.exists(ruta_limpia):
        return f"¡Szzzt! Error en mi base de datos. No encuentro el archivo '{CSV_FILE_PATH}'. ¡Asegúrate de que esté en la misma carpeta que este script!"
    
    # Probamos con múltiples codificaciones por seguridad
    codificaciones = ['utf-8-sig', 'latin-1', 'utf-8']
    lista_pokemon = []
    archivo_leido = False

    for codificacion in codificaciones:
        try:
            with open(ruta_limpia, mode='r', encoding=codificacion) as f:
                lector_csv = csv.reader(f)
                filas = list(lector_csv)
                
                if not filas:
                    continue
                
                # Normalizamos los encabezados de la primera fila: minúsculas y sin acentos
                encabezados_originales = [h.strip() for h in filas[0]]
                encabezados_normalizados = [
                    h.lower().replace('ó', 'o').replace('á', 'a').replace('í', 'i').replace('ú', 'u').replace('é', 'e').replace('/', '') 
                    for h in encabezados_originales
                ]
                
                # Buscamos la posición de cada columna de manera flexible e inteligente
                try:
                    idx_pkmn = encabezados_normalizados.index("pokemon")
                except ValueError:
                    idx_pkmn = 2
                    
                try:
                    idx_tipo = encabezados_normalizados.index("tipo")
                except ValueError:
                    idx_tipo = 3
                    
                try:
                    idx_lugar = encabezados_normalizados.index("ubicacion")
                except ValueError:
                    idx_lugar = 1
                    
                try:
                    idx_ecosistema = encabezados_normalizados.index("ecosistema")
                except ValueError:
                    idx_ecosistema = 0

                lista_pokemon = []
                # Procesamos el contenido saltando la fila de encabezados
                for fila in filas[1:]:
                    if len(fila) > max(idx_pkmn, idx_tipo, idx_lugar, idx_ecosistema):
                        pkmn = fila[idx_pkmn].strip()
                        tipo = fila[idx_tipo].strip()
                        lugar = fila[idx_lugar].strip()
                        ecosistema = fila[idx_ecosistema].strip()
                        
                        if pkmn:
                            # CAMBIADO: Ahora usa etiquetas HTML limpias (<strong> y <i>) en lugar de asteriscos de Markdown
                            lista_pokemon.append(f"• <strong>{pkmn}</strong> ({tipo}) - Habita en el ecosistema {ecosistema} de <i>{lugar}</i>.")
                
                if lista_pokemon:
                    archivo_leido = True
                    break
        except Exception as e:
            print(f"Intento fallido con codificación {codificacion}: {e}")
            continue

    if not archivo_leido:
        return "¡Szzzt! Error crítico de energía: No pude procesar los datos de tu archivo Pokédex. Revisa que el formato sea correcto."

    # Armamos la respuesta estructurada usando <br> para tu HTML
    texto_final = "¡Szzzt! ¡Accediendo a los archivos locales de la región! Aquí están los Pokémon registrados en Nayarit:<br><br>"
    texto_final += "<br>".join(lista_pokemon)
    texto_final += "<br><br>¡Increíble biodiversidad, verdad, Entrenador! ¡Szzzt!"
    return texto_final

# ==========================
# RUTA PRINCIPAL
# ==========================
@app.route('/')
def inicio():
    return render_template('index.html')

# ==========================
# CHATBOT (ROTOMDEX DE ALOLA)
# ==========================
@app.route('/chat', methods=['POST'])
def chat():
    if not request.json or 'mensaje' not in request.json:
        return jsonify({"respuesta": "¡Szzzt! ¡Error crítico! No recibí ningún mensaje de tu parte."}), 400

    mensaje = request.json['mensaje'].lower().strip()

    # Saludos
    if any(palabra in mensaje for palabra in ["hola", "buenas", "saludos", "que tal"]):
        respuesta = "¡Szzzt! ¡Hola, Entrenador! ¡Mi pantalla está encendida y lista para la aventura! ¿Qué necesitas consultar hoy?"

    # Presentación
    elif "quien eres" in mensaje or "cómo te llamas" in mensaje or "como te llamas" in mensaje:
        respuesta = "¡Szzzt! ¡Soy tu RotomDex! Un Pokémon de tipo Eléctrico/Fantasma habitando esta increíble enciclopedia digital. ¡Mucho gusto!"

    # CONSULTAR LOS POKÉMON DE NAYARIT
    elif "que pokemons podemos encontrar" in mensaje or "qué pokémon" in mensaje or "pokemon en nayarit" in mensaje or "pokémones podemos encontrar" in mensaje:
        respuesta = obtener_pokemons_nayarit()

    # Función
    elif "que haces" in mensaje or "para que sirves" in mensaje:
        respuesta = "¡Szzzt! Registro datos de Pokémon, analizo el mapa de la región, reviso el clima y te guío en todo lo que necesites en Tepic."

    # Servicios
    elif "servicios" in mensaje:
        respuesta = "¡Szzzt! En este Centro Técnico te ayudamos con asesoría informática, desarrollo web de alta velocidad como un Jolteon y excelente soporte técnico."

    # Ubicación
    elif "ubicados" in mensaje or "direccion" in mensaje or "donde estan" in mensaje:
        respuesta = "¡Szzzt! Nuestras coordenadas están fijadas en el mapa de Alola... ¡Digo, nos encontramos en Tepic, Nayarit!"

    # Horario
    elif "horario" in mensaje or "abren" in mensaje:
        respuesta = "¡Szzzt! Nuestro laboratorio está activo de lunes a viernes desde las 8:00 AM hasta las 4:00 PM. ¡No llegues tarde!"

    # Contacto
    elif any(palabra in mensaje for palabra in ["telefono", "teléfono", "comunicarme", "contacto", "llamar", "correo"]):
        respuesta = "¡Szzzt! ¡Entendido! Si quieres comunicarte con nuestro equipo, puedes llamar directo al 311-123-4567. ¡O también puedes enviarnos una señal digital por correo electrónico!"

    # Hora actual
    elif "hora" in mensaje:
        hora_actual = datetime.now().strftime("%H:%M:%S")
        respuesta = f"¡Szzzt! ¡Mis relojes internos dicen que la hora actual es {hora_actual}! El tiempo vuela en la aventura."

    # Fecha actual
    elif "fecha" in mensaje or "dia es hoy" in mensaje:
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        respuesta = f"¡Szzzt! Mirando el calendario de la Pokédex... ¡Hoy es {fecha_actual}!"

    # Día de la semana
    elif "que dia es" in mensaje:
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        respuesta = f"¡Szzzt! ¡Hoy es {dias[datetime.now().weekday()]}! Un día perfecto para registrar nuevos datos."

    # Clima 
    elif "temperatura" in mensaje or "clima" in mensaje:
        respuesta = obtener_clima_tepic()

    # Nombre del usuario
    elif "me llamo" in mensaje:
        nombre = mensaje.split("me llamo")[-1].strip()
        nombre = nombre.replace(".", "").replace("!", "").title() 
        respuesta = f"¡Szzzt! ¡Qué gran nombre! ¡Mucho gusto, Entrenador {nombre}! Registrando tu perfil en mi base de datos."

    # Agradecimientos
    elif "gracias" in mensaje:
        respuesta = "¡Szzzt! ¡No hay de qué! ¡Para eso están los amigos y las Pokédex!"

    # Despedida
    elif "adios" in mensaje or "hasta luego" in mensaje or "bye" in mensaje:
        respuesta = "¡Szzzt! ¡Nos vemos, Entrenador! ¡Cuídate allá afuera en las rutas altas y que tengas un excelente día!"

    # Ayuda 
    elif "ayuda" in mensaje:
        respuesta = (
            "¡Szzzt! ¡Aquí tienes la lista de comandos que puedo procesar, Entrenador!:<br>"
            "- ¿Quién eres?<br>"
            "- ¿Qué Pokémon podemos encontrar en Nayarit?<br>"
            "- ¿Qué servicios ofrecen?<br>"
            "- ¿Cómo puedo comunicarme o cuál es su teléfono?<br>"
            "- ¿Dónde están ubicados?<br>"
            "- ¿Cuál es su horario?<br>"
            "- ¿Qué hora es o qué día es hoy?<br>"
            "- ¿Cuál es la temperatura de Tepic?"
        )

    else:
        respuesta = "¡Szzzt! Mis algoritmos no procesaron esa frase... Escribe 'ayuda' para ver qué comandos puedo entender en este modo."

    return jsonify({"respuesta": respuesta})

if __name__ == '__main__':
    app.run(debug=True)