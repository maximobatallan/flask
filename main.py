import sys
import io
import os
import json
import openai
import pydub
import requests
import soundfile as sf
import speech_recognition as sr
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


# OpenAi API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Access token for your WhatsApp business account app
whatsapp_token = os.environ.get("WHATSAPP_TOKEN")

# Verify Token defined when configuring the webhook
verify_token = os.environ.get("VERIFY_TOKEN")

# Message log dictionary to enable conversation over multiple messages
message_log_dict = {}


# language for speech to text recoginition
# TODO: detect this automatically based on the user's language
LANGUGAGE = "en-US"


# get the media url from the media id
def get_media_url(media_id):
    '''headers = {
        "Authorization": f"Bearer {whatsapp_token}",
    }
    url = f"https://graph.facebook.com/v16.0/{media_id}/"
    response = requests.get(url, headers=headers)
    print(f"media id response: {response.json()}")
    return response.json()["url"]'''
    nopermite = 'Disculpe, no puedo procesar audios, escribeme un mensaje'
    return nopermite


# download the media file from the media url
def download_media_file(media_url):
    '''headers = {
        "Authorization": f"Bearer {whatsapp_token}",
    }
    response = requests.get(media_url, headers=headers)
    print(f"first 10 digits of the media file: {response.content[:10]}")
    return response.content'''
    nopermite = 'Disculpe, no puedo procesar audios, escribeme un mensaje'
    return nopermite


# convert ogg audio bytes to audio data which speechrecognition library can process
def convert_audio_bytes(audio_bytes):
    nopermite = 'Disculpe, no puedo procesar audios, escribeme un mensaje'
    return nopermite
    
    
    



# run speech recognition on the audio data
def recognize_audio(audio_bytes):
    recognizer = sr.Recognizer()
    audio_text = recognizer.recognize_google(audio_bytes, language=LANGUGAGE)
    return audio_text


# handle audio messages
def handle_audio_message(audio_id):
    audio_url = get_media_url(audio_id)
    audio_bytes = download_media_file(audio_url)
    #audio_data = convert_audio_bytes(audio_bytes)
    #audio_bytes = download_media_file(audio_url)
    audio_data = 'Disculpe, no puedo procesar audios, escribeme un mensaje'
    
    audio_text = 'Disculpe, no puedo procesar audios, escribeme un mensaje'
    message = audio_text
    return message


# send the response as a WhatsApp message back to the user
def send_whatsapp_message(body, message):
    value = body["entry"][0]["changes"][0]["value"]
    phone_number_id = value["metadata"]["phone_number_id"]
    from_number = value["messages"][0]["from"]
    print(from_number)
    url = "https://graph.facebook.com/v17.0/" + phone_number_id + "/messages"
        
    payload = json.dumps({
      "messaging_product": "whatsapp",
      "recipient_type": "individual",
      "to": from_number,
      "type": "text",
      "text": {
        "preview_url": False,
        "body": message
      }
    })
    
    headers = {
      'Content-Type': 'application/json',
      "Authorization": f"Bearer {whatsapp_token}",
    }
    
    response = requests.post(url, data=payload, headers=headers)
  
    response.raise_for_status()


# create a message log for each phone number and return the current message log

def update_message_log(message, phone_number, role):
    
    system_prompt = f"""
                        Tu funcion es contestar lo que te pregunte solo en base a este texto: RESPUESTAS:
Unidad 1
1- ¿Por qué es importante atender la alfabetización en todas sus dimensiones en relación a los grupos más vulnerables?

Es crucial abordar la alfabetización en todas sus dimensiones para los grupos vulnerables porque les brinda las herramientas necesarias para participar plenamente en la sociedad. La alfabetización no se limita solo a la lectura y escritura, sino que abarca habilidades culturales, sociales y cognitivas. Para los grupos vulnerables, esto significa empoderamiento, acceso a información, capacidad para expresarse y participar activamente en la vida comunitaria.

2- ¿Alfabetizar es enseñar a leer, escribir y calcular? Si - No, justifique su respuesta.

No necesariamente. Alfabetizar implica más que simplemente enseñar a leer, escribir y calcular. Si bien estas son habilidades fundamentales, la alfabetización también abarca la comprensión de la información, el pensamiento crítico y la aplicación práctica de estas habilidades en diversos contextos. La alfabetización integral contribuye al desarrollo personal y social, permitiendo a las personas participar plenamente en la sociedad.

3- Según José Luis Rodríguez Illera, ¿por qué es más correcto tomar el concepto de "literacidad" cuando hablamos de alfabetizar?

Rodríguez Illera sugiere que el término "literacidad" (literacy) es más apropiado porque va más allá de la simple lectura y escritura. Este concepto enfatiza las prácticas culturales y escritas, considerando la lectura como una actividad culturalmente significativa que va más allá de la decodificación de un texto. La "literacidad" refleja la complejidad y diversidad de las prácticas letradas en diferentes contextos.

4- En relación a la alfabetización, según su criterio, ¿qué puntos en común comparten el concepto psicológico-social de la lectura y el concepto de competencia, proceso y práctica?

Ambos enfoques reconocen la alfabetización como más que una simple habilidad técnica. El concepto psicológico-social de la lectura destaca la adquisición de capacidades cognitivas y la comprensión de códigos. Por otro lado, la perspectiva de competencia, proceso y práctica ve la alfabetización como una competencia cognitiva que se manifiesta en diversas realizaciones. Ambos enfoques reconocen la dimensión social y cultural de la alfabetización.

5- Explique cómo ha cambiado la idea actual sobre el concepto de individuo analfabeto. ¿Son sinónimos los conceptos de analfabeto e iletrado?

La idea actual sobre el individuo analfabeto ha evolucionado. Antes se limitaba a la falta de habilidades de lectura y escritura, pero ahora se reconoce que la alfabetización abarca diversas competencias. Analfabeto e iletrado no son sinónimos. Analfabeto se refiere a la falta de habilidades de lectura y escritura, mientras que iletrado implica una carencia más amplia de habilidades culturales y prácticas letradas.

6- Nombre algunos de los soportes, nacidos con el enfoque social, que dan forma al alfabetismo.

Soportes como la alfabetización digital, la alfabetización visual, la alfabetización mediática y la alfabetización en información son ejemplos de enfoques sociales que amplían la concepción de la alfabetización más allá de la lectura tradicional y la escritura.

7- Justifique por qué la alfabetización puede ser considerada como un proceso liberador.

La alfabetización capacita a las personas para acceder a información, expresar sus pensamientos y participar en la sociedad. Al proporcionar herramientas para el pensamiento crítico y la comunicación efectiva, la alfabetización empodera a los individuos, permitiéndoles ejercer su libertad de expresión y participar en la toma de decisiones. En este sentido, la alfabetización se considera liberadora al abrir oportunidades y mejorar la capacidad de las personas para ejercer sus derechos.


Unidad 2 

Influencia de las TIC en el proceso de alfabetización:
Las Nuevas Tecnologías de la Información y la Comunicación (TIC) han influido significativamente en el proceso de alfabetización. La introducción de las TIC ha ampliado el concepto de alfabetización más allá de la mera capacidad de leer y escribir. Ahora implica la habilidad para comprender, evaluar y utilizar la información en diversos formatos, como textos digitales, imágenes, videos y otros medios. La alfabetización digital se ha vuelto esencial, ya que implica la capacidad de interactuar críticamente con la información en entornos digitales.

Sentido amplio de la alfabetización:
Consideramos la alfabetización en un sentido amplio porque va más allá de la mera decodificación de palabras. La alfabetización abarca la capacidad de comprender, analizar y sintetizar información en diversas formas y contextos. Incluye la alfabetización digital, que implica competencias para utilizar herramientas tecnológicas y evaluar la información en línea. En un mundo cada vez más complejo, la alfabetización en un sentido amplio prepara a las personas para participar plenamente en la sociedad y la cultura contemporáneas.

Ubicación de la alfabetización digital en el contexto educativo:
La alfabetización digital debe ocupar un lugar central en el contexto educativo. Con el aumento de la dependencia de la tecnología en la educación y la vida cotidiana, es esencial que los estudiantes desarrollen habilidades para utilizar las TIC de manera efectiva y crítica. La alfabetización digital no solo se limita al aula de informática; debe integrarse en todas las disciplinas para preparar a los estudiantes para un mundo digital.

Énfasis en el carácter plural de las multialfabetizaciones:
El énfasis en el carácter plural de las multialfabetizaciones se debe a la diversidad de habilidades y competencias necesarias en la sociedad contemporánea. No basta con ser simplemente "alfabetizado" en el sentido tradicional. La multialfabetización reconoce la necesidad de ser competente en diversas formas de lenguaje y medios, desde la alfabetización digital hasta la visual, mediática y cultural.

Análisis de la afirmación sobre la lectoescritura:
No estoy de acuerdo con la afirmación de que "La alfabetización se encuentra solo vinculada a la lecto - escritura". La alfabetización ahora implica habilidades que van más allá de la lectura y escritura tradicionales e incluye la capacidad de comprender y producir información en diversos formatos, incluidos medios digitales. La alfabetización digital y mediática son componentes esenciales de la alfabetización contemporánea.

Origen y evolución de la alfabetización digital:
La idea de alfabetización digital surgió con el aumento de la tecnología digital en la década de 1990. Inicialmente, se centraba en la habilidad para usar computadoras y software. Con el tiempo, evolucionó para abarcar habilidades más amplias, como la evaluación crítica de información en línea, la participación en redes sociales y la comprensión de la ética digital.

Tipos de individuos según Burbules y Callister:

Usuarios instrumentales:
Características: Utilizan Internet como herramienta para tareas específicas, como la búsqueda de información.

Usuarios simbólicos:
Características: Ven Internet como un espacio para la expresión personal y la construcción de identidad.

Usuarios sociales:
Características: Se centran en la interacción social en línea y el desarrollo de comunidades virtuales.

Tipo de alfabetización según Rafael Casado Ortiz:
Rafael Casado Ortiz aboga por una alfabetización crítica y transformadora. Esto implica no solo adquirir habilidades técnicas, sino también desarrollar un pensamiento crítico para comprender y cuestionar la información. Además, busca empoderar a las personas para participar activamente en la sociedad, utilizando la alfabetización como una herramienta para el cambio social.

Aspectos clave para la alfabetización digital según Cecilia Castano Collado:
Se requiere conocer la clasificación de Burbules y Callister para responder a esta pregunta.

Características relevantes de la literacidad digital:

Evaluación crítica:
Los estudiantes deben poder analizar de manera crítica la información en línea, identificando sesgos y evaluando la fiabilidad de las fuentes.

Colaboración en línea:
La capacidad de trabajar de manera efectiva en entornos en línea, participar en comunidades virtuales y colaborar en proyectos digitales.

Gestión de la identidad digital:
Comprender y gestionar la presencia en línea, incluida la privacidad, la seguridad y la construcción de una identidad digital positiva.



Unidad 3:


Actividades de reflexion y revision
1-	l0ue relacion ,existe entre la Brecha digital y la concentraci6n de la informaci6n?
2-	l,Que entornos de aprendizaje se plantean para los ent.OIrnos virtuales?
3-	Acorde a lo leido lPor que y para que la alfab,etizaci6n digital debe incluirse en el proceso de alfabetizaci6n general yen las escuelas?
4-	l,Por que es necesaIrio generar nuevos entornos de enseiianza y aprendizaje? A su criterio lS61o s,e accede a ellos con la alfabetizaci6n digital? 5- lndique las diferentes brechas digitales de acuerdo a las pe-rspectivas analizadas. Destaque tres caracterfsticas distintivas en cada una de ellas.
6-	Acorde a su criteri,o lC6mo define el termino "brecha digital"? Destaque algunas de las particularidades negativas implicitas en este concepto.
7-	l,Cual es la primera brecha a salvar dentro de las variantes de la br,echa digital? Considere que es un punto coincidente en todos los autores mencionados.
8-	l0ue consideraciones se deben tener al diferenciar la inclusion y la difusi6n? lC1ree que la difusi6n aumenta la inclusion en la sociedad de la lnformaci6n?
9-	La brecha digital de genera sigue siendo muy amplia en el mundo, muchas naciones realizan grandes esfuerzos para reducirla, pero no siempre los logros son los esperados. lEvidencia usted en su lug,ar de trabajo, comunidad o ciudad la existencia y/o persistencia de la brecha digital relacionada al genero? Si la respuesta es afirmativa lA que motivos cree que se debe?
10-	Explique la relaci6n existente entre la Sociedad de la lnformaci6n, la brecha digital y el acceso a las NTIC.
 
Epígrafes explicativos para imágenes sobre el mundo conectado por las tecnologías y sus conexiones:

"Un universo interconectado: Las tecnologías unen a personas de todos los rincones del mundo, creando una red global de información y comunicación."

"Puentes digitales: Cada dispositivo es un puente que acorta distancias, conectando culturas, ideas y oportunidades en un tejido digital que abarca el planeta."

"Caminos electrónicos: Las conexiones digitales forman caminos electrónicos que permiten el intercambio constante de conocimientos, experiencias y colaboración entre diferentes sociedades."

"El latir digital del mundo: En la era de la información, el pulso de la sociedad se mide por las pulsaciones digitales que atraviesan continentes, uniendo corazones y mentes a través de la red."

"La aldea global digital: En este nuevo mundo, las tecnologías actúan como los hilos invisibles que tejen una aldea global digital, donde cada nodo es una historia, una idea, una vida conectada."

Unidad 4:

¿Indique dos definiciones del concepto "Sociedad de la Información"?

 Según Manuel Castells (1998), la Sociedad de la Información es una fase del desarrollo social caracterizada por la capacidad de obtener y compartir información en cualquier momento y lugar, ligada a las Nuevas Tecnologías de la Información (TIC). Otra definición presentada es la de Karsten Kruger (2006), quien destaca que en la "Sociedad del Conocimiento" los procesos socioeconómicos adquieren una nueva calidad, ya que el conocimiento se convierte en el factor de producción más importante.
¿Señale las particularidades de la Sociedad de la Información y cuáles considera las más relevantes de esta fase social según su criterio?

 La Sociedad de la Información se caracteriza por la capacidad de obtener y compartir información en cualquier momento y lugar, dependiendo sustancialmente de las TIC. La geografía se redefine por redes de información. En mi criterio, la relevancia radica en la centralidad del conocimiento como factor de producción, la desaparición de fronteras geográficas y el papel crucial de las TIC.
¿Por qué se habla de un "nuevo mapa social"?

 Se habla de un "nuevo mapa social" en la Sociedad de la Información porque la geografía tradicional basada en fronteras se desdibuja, dando paso a un mapa mundial definido por redes de información, que incluyen o excluyen a personas, empresas y regiones según su valor en la economía del conocimiento.
¿Analice si las afirmaciones son correctas y justifique cada caso?

a- "La Sociedad Industrial evolucionó hacia la Sociedad del Conocimiento"
 Correcta. Según Castells, la Sociedad Industrial evolucionó hacia una nueva sociedad centrada en el procesamiento y manejo de la información.
b- "Las personas y organizaciones disponen solo de su conocimiento"
 Correcta. En la Sociedad del Conocimiento, el conocimiento es un recurso crucial, y las personas y organizaciones dependen de él.
c- "La capacidad de acceso a la información es un factor influyente en las transformaciones sociales"
 Correcta. El acceso a la información es fundamental en la Sociedad de la Información y afecta las transformaciones sociales, según Kruger.
Complete el siguiente cuadro sobre elementos básicos que conforman la Sociedad del Conocimiento y su representación:

Elementos Básicos	Representación
Revolución Digital	Nueva Organización
Acceso a la Sociedad del Conocimiento	Usuarios
Prioridad Social de Conocimiento	Infraestructura
Economía del Conocimiento	Actividades de Reflexión
Acción de Nuevos Medios Tecnológicos	Contenido
Sociedad Postindustrial	Entorno
Basándose en los contenidos vertidos por Castells, analice y complete el siguiente cuadro:
(No se proporcionaron detalles específicos para completar el cuadro. Si proporcionas información adicional, puedo ayudarte a completarlo).

Explique y justifique por qué el conocimiento actualmente es considerado una prioridad social.

 El conocimiento es considerado una prioridad social porque, según Kruger, en la Sociedad del Conocimiento, las actividades socioeconómicas adquieren una nueva calidad, y el conocimiento se convierte en el factor de producción más importante. La alfabetización tecnológica y digital se presenta como esencial para la participación plena y activa en esta sociedad, afectando tanto el acceso al empleo como la participación ciudadana, garantizando así derechos y oportunidades.

Unidad 5:


Señale en qué contextos están impactando las TIC la institución escolar. ¿Puede permanecer ajena al mismo?

Las TIC están impactando en los sistemas educativos, sus instituciones y los individuos que los conforman, en particular los docentes y alumnos. La institución escolar no puede permanecer ajena a este impacto, ya que las TIC están generando transformaciones socioculturales y se considera fundamental su integración en la educación.

¿Cuál es la relación existente entre brecha digital, la alfabetización digital y la exclusión?

Las TIC pueden contribuir a reducir la brecha digital, que se refiere a la diferencia en el acceso y uso de la tecnología entre distintos grupos sociales. La alfabetización digital es necesaria para aprovechar plenamente las oportunidades que ofrecen las TIC. La exclusión está vinculada a la falta de acceso y habilidades digitales, por lo que la alfabetización digital es crucial para evitar la exclusión de aquellos que no tienen acceso o conocimientos tecnológicos.

¿Por qué la incorporación de las Nuevas Tecnologías de la Información y la Comunicación (NTIC) y la Alfabetización digital se encuentran ligadas a las políticas de igualdad?

La incorporación de las NTIC y la alfabetización digital está ligada a políticas de igualdad porque busca reducir la brecha digital y garantizar que todos los ciudadanos tengan acceso y habilidades para utilizar estas tecnologías. Al hacerlo, se promueve la igualdad de oportunidades en el acceso a la información, la participación ciudadana y el desarrollo personal y profesional.

Complete el siguiente cuadro indicando algunas características de cada uno de los entornos de aprendizaje señalados:

Entorno de Aprendizaje	Características
Formal	Sistema educativo ordenado, clases estructuradas, énfasis en la enseñanza de contenidos, desarrollo en instituciones escolares.
Informal	Proceso que abarca toda la vida, aprendizaje invisible, basado en experiencias diarias y comunicación entre participantes.
No Formal	Actividades educativas organizadas fuera de instituciones educativas, dirigidas a grupos, sin validación oficial.
Virtual	Asociado a modelos formales de aprendizaje, depende de instituciones oficiales, se realiza en entornos virtuales mediante tecnologías como Internet y multimedia.
Analice la siguiente afirmación, indique si es correcta y justifique su  "Podemos tomar como sinónimos los procesos de 'educar para los medios' y el de 'alfabetizar en medios'"

La afirmación es incorrecta. "Educar para los medios" se refiere a desarrollar habilidades críticas y reflexivas en el uso de medios de comunicación, mientras que "alfabetizar en medios" implica adquirir habilidades básicas de lectura y escritura relacionadas con los medios. Aunque comparten objetivos, no son sinónimos, ya que "alfabetizar en medios" se centra más en la adquisición de habilidades fundamentales.


6- Señale las características de la alfabetización crítica. ¿Por qué es importante llegar a este nivel?"
Las características de la alfabetización crítica, especialmente en el contexto de la alfabetización digital, se derivan de la capacidad de las personas para comprender, evaluar y utilizar la información de manera reflexiva y crítica en entornos digitales. Aquí hay algunas características clave de la alfabetización crítica:

Análisis de la información: La alfabetización crítica implica la capacidad de analizar la información de manera profunda, examinando su origen, credibilidad, intenciones y posibles sesgos. Los individuos críticamente alfabetizados no aceptan la información de manera pasiva, sino que la evalúan de manera activa.

Capacidad de discernimiento: Las personas alfabetizadas críticamente pueden discernir entre diferentes tipos de información, identificando la diferencia entre hechos, opiniones, propaganda y desinformación. Esto es esencial en un entorno digital donde la información puede ser fácilmente manipulada.

Habilidades de investigación: La alfabetización crítica implica habilidades de investigación efectivas, permitiendo a las personas encontrar información relevante, verificar fuentes y profundizar en un tema particular.

Conciencia de la brecha digital: Los individuos críticamente alfabetizados son conscientes de la brecha digital y trabajan para superarla. Esto implica no solo tener acceso a la tecnología, sino también comprender las disparidades en el acceso y la competencia digital entre diferentes grupos sociales.

Pensamiento reflexivo: La alfabetización crítica fomenta el pensamiento reflexivo, donde las personas cuestionan sus propias creencias, suposiciones y prejuicios, así como la información que encuentran en línea.

Participación activa: Los individuos críticamente alfabetizados no son consumidores pasivos de información; participan activamente en la creación y difusión de contenido, contribuyendo de manera constructiva al discurso digital.

La importancia de alcanzar la alfabetización crítica, especialmente en el contexto de la alfabetización digital, radica en la necesidad de navegar por un mundo cada vez más digitalizado y lleno de información. La capacidad de discernir entre información precisa y engañosa, así como participar de manera reflexiva en los medios digitales, es esencial para la toma de decisiones informada y la participación efectiva en la sociedad actual. La alfabetización crítica no solo se trata de utilizar herramientas tecnológicas, sino de desarrollar un enfoque mental que permita a las personas ser ciudadanos activos y responsables en el entorno digital.

Nueva doc:


En el texto proporcionado, se abordan varios términos clave relacionados con la educación y la alfabetización digital. Aquí hay una conceptualización y diferenciación de algunos de ellos:

Docentes:

Concepto: Se refiere a los profesionales de la enseñanza que tienen la responsabilidad de facilitar el aprendizaje de los estudiantes.
Importancia en el contexto del texto: El texto destaca la evolución del rol docente en el contexto de la tecnología educativa y la necesidad de adaptarse a los cambios tecnológicos.
Alfabetización Digital:

Concepto: Se refiere a la capacidad de utilizar tecnologías de la información y comunicación (TIC) de manera efectiva, lo que implica la comprensión y el uso crítico de herramientas digitales.
Importancia en el contexto del texto: El texto aborda la alfabetización digital como parte esencial de la formación docente y la necesidad de comprender las nuevas formas de acceso al conocimiento en la era digital.
Tecnología Educativa:

Concepto: Se refiere al uso y la integración de herramientas tecnológicas en el proceso de enseñanza y aprendizaje para mejorar la calidad educativa.
Importancia en el contexto del texto: El texto destaca la evolución histórica de la tecnología educativa y su papel en la transformación de la enseñanza, así como la importancia de adoptar nuevas tecnologías en el aula.
Medios de Comunicación:

Concepto: Se refiere a los canales y herramientas utilizados para transmitir información, incluyendo medios tradicionales como la radio y la televisión, así como medios digitales.
Importancia en el contexto del texto: El texto subraya la reflexión sobre el impacto de los medios de comunicación en la educación y destaca la necesidad de comprender su papel en la vida cotidiana y escolar.
Educación a Distancia:

Concepto: Se refiere a la modalidad educativa en la que la instrucción no se realiza en un entorno presencial, sino a través de recursos y tecnologías que permiten la comunicación a distancia.
Importancia en el contexto del texto: El texto menciona la evaluación de la educación a distancia como parte de la función del aula tecnológica y destaca sus ventajas.
Estos términos están interconectados en el texto, ya que la alfabetización digital y la tecnología educativa son aspectos esenciales para la formación de docentes y la evolución de la educación en la era digital.


Extracto de Fernando Savater:

Savater aborda la presencia de las nuevas tecnologías en la vida cotidiana y escolar. Destaca el aumento en el acceso a enormes volúmenes de información, la rapidez en el acceso, la superación de distancias y limitaciones espaciales, y la mayor variedad de recursos didácticos disponibles para maestros y profesores. Sin embargo, plantea la dificultad de definir avances desde el punto de vista del desarrollo cognitivo y pedagógico. Savater enfatiza que, aunque hay ganancias en términos de acceso a información, es complicado medir el impacto en el desarrollo cognitivo y pedagógico.

Reflexiones personales:
Es esencial reconocer que el acceso a la información y la tecnología no garantiza automáticamente un desarrollo cognitivo y pedagógico significativo. La cantidad de datos disponibles no siempre se traduce en una comprensión profunda o en habilidades de aprendizaje mejoradas. Además, la necesidad de investigaciones experimentales para evaluar con precisión el impacto de las tecnologías en las estrategias de aprendizaje subraya la importancia de no asumir beneficios sin una evaluación crítica.

Entrevista a Juan Carlos Tedesco:

Tedesco se centra en los avances en términos de acceso, velocidad y recursos didácticos gracias a las Tecnologías de la Información y la Comunicación (TIC). Señala la necesidad de investigaciones que evalúen la eficacia de estas tecnologías en el contexto escolar, donde interactúan diversas variables.

Reflexiones personales:
El énfasis en la necesidad de investigaciones experimentales subraya la importancia de una evaluación basada en evidencia sobre cómo las TIC afectan el proceso de aprendizaje. Este llamado a la investigación destaca la complejidad del entorno escolar y la interacción de diversas variables que deben considerarse para comprender completamente el impacto de las TIC.

Momentos históricos de la Tecnología Educativa:
El texto no proporciona detalles específicos sobre momentos históricos relacionados con la Tecnología Educativa.

Análisis crítico del estado y debate actual:
El texto no aborda directamente el estado y el debate actual en el campo de la Tecnología Educativa.

Relación con el campo de la didáctica:
Se menciona que la Tecnología Educativa se preocupa por las prácticas de enseñanza y analiza la teoría de la comunicación y los nuevos desarrollos tecnológicos. La relación con la didáctica se presenta como complementaria, donde ambas disciplinas abordan el acto pedagógico desde diferentes saberes específicos.

Romper con ideas estereotipadas:
Es importante cuestionar la noción simplificada de que la Tecnología Educativa es sinónimo de informática. El texto destaca que la Tecnología Educativa va más allá de los medios audiovisuales e informáticos, involucrando diversos elementos para mejorar las prácticas de enseñanza. La incorporación de tecnologías no garantiza automáticamente mejoras en la oferta educativa y requiere una comprensión más profunda de su aplicación.


 Al inicio de la unidad planteamos dos miradas respecto a los cambios en las formas de enseñar y aprender con nuevas tecnologías. ¿Cuáles son esas perspectivas?

 Al inicio de la unidad, se presentan dos perspectivas: una que ve la introducción de tecnología como una extensión de las prácticas existentes y otra que sostiene que implica una reestructuración fundamental del conocimiento y desafía las formas jerárquicas de la institución escolar.

 ¿Qué significa que en la actualidad hay una redefinición del aula como espacio pedagógico? Brindar un ejemplo en el contexto actual.

 En la actualidad, la redefinición del aula implica cambios en su estructura y dinámica debido a la introducción de tecnologías. Por ejemplo, en el contexto actual, el aula ya no sigue exclusivamente el método frontal, ya que la proliferación de dispositivos como computadoras y teléfonos móviles ha permitido enfoques más individualizados, fragmentando la atención y desafiando la enseñanza frontal tradicional.

 ¿Cuál es la relación entre el desdibujamiento de las fronteras del espacio de las escuelas y los cambios producidos debido a la pandemia del COVID-19?

 El desdibujamiento de las fronteras entre lo escolar y no escolar se ha intensificado debido a la pandemia del COVID-19. Con la adopción masiva de la educación a distancia, los estudiantes utilizan dispositivos incluso durante las horas escolares en entornos no tradicionales, desafiando la noción convencional de espacio y tiempo escolar.

 ¿En qué se diferencian los nuevos "espacios de afinidad" que generan las redes de la experiencia de agrupamiento del aula?

 Los nuevos "espacios de afinidad" creados por las redes sociales difieren de la experiencia de agrupamiento del aula en que se basan en tareas e intereses comunes más que en edad o nivel de desempeño. Estos espacios son flexibles, permeables y valoran el conocimiento tácito, permitiendo una afiliación más dinámica y diversa que los grupos homogéneos del aula.

 ¿Por qué se pone en cuestión la noción e importancia del conocimiento escolar? ¿Qué elementos de las nuevas tecnologías de la comunicación se diferencian de este tipo de conocimiento?

 Se cuestiona la noción e importancia del conocimiento escolar debido a la introducción de nuevas tecnologías. Las tecnologías de la comunicación son multimodales, igualitarias y orientadas a la inmediatez y la experiencia emocional en lugar de la verdad. Difieren al ser más flexibles, permitir la participación de diversos usuarios y desafiar las jerarquías centralizadas y disciplinadas del conocimiento escolar tradicional.



Pregunta 1: ¿Cómo se define el aula tecnológica y cuáles son sus componentes?

Respuesta 1: El aula tecnológica se define como un espacio equipado y diseñado para el uso integrado de diversas tecnologías de la información y comunicación (TIC). En este entorno, se utilizan medios didácticos tradicionales potenciados por la tecnología moderna, la tecnología de la información, la informática y los medios audiovisuales. Se busca crear ambientes estimulantes de aprendizaje que favorezcan la construcción social del conocimiento.

Pregunta 2: ¿Cuáles son algunos criterios básicos para el trabajo en un aula hipermedial?

Respuesta 2: Los criterios básicos para el trabajo en un aula hipermedial incluyen:

Generar ambientes de aprendizaje estimulantes.
Facilitar intercambios que resulten en espacios fecundos para la construcción social del conocimiento.
Fomentar la exploración, indagación, producción y el intercambio de saberes.
Diseñar un espacio adecuado que concentre la gestión integral de recursos multimediales o hipertextuales para el aprendizaje.
Pregunta 3: ¿Cuáles son las ventajas de la Educación a Distancia en general, según el fragmento proporcionado?

Respuesta 3: Según el texto, las ventajas de la Educación a Distancia incluyen:

La posibilidad de consolidar procesos de educación a distancia gracias a la incorporación de las nuevas tecnologías de la información y comunicación (NTIC).
Convertirse en una herramienta poderosa para la distribución del conocimiento acumulado socialmente.
Proporcionar acceso a la información desde diversos soportes y utilizar la tecnología para la comunicación y expresión.

Solo responder preguntas en base al texto anterior, si no esta respuesta no buscar en otro lado, solo contestar "disculpa no tengo esa informacion

"""

   
    initial_log = {
        "role": "system",
        "content": system_prompt,
    }






    if phone_number not in message_log_dict:
        message_log_dict[phone_number] = [initial_log]
        message_log_dict[phone_number].append(user_log)
    message_log = {"role": role, "content": message}
    message_log_dict[phone_number].append(message_log)
    return message_log_dict[phone_number]


# remove last message from log if OpenAI request fails
def remove_last_message_from_log(phone_number):
    message_log_dict[phone_number].pop()


# make request to OpenAI
def make_openai_request(message, from_number):
  
    try:
        message_log = update_message_log(message, from_number, "user")
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=message_log,
            temperature=0,
        )
        response_message = response.choices[0].message.content
        print(f"openai response: {response_message}")
        update_message_log(response_message, from_number, "assistant")
    except Exception as e:
        print(f"openai error: {e}")
        response_message = "Sorry, the OpenAI API is currently overloaded or offline. Please try again later."
        remove_last_message_from_log(from_number)
    return response_message


# handle WhatsApp messages of different type
def handle_whatsapp_message(body):
    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    if message["type"] == "text":
        message_body = message["text"]["body"]
        print(message_body)
        response = make_openai_request(message_body, message["from"])
    else:
        response = 'Disculpe, no puedo procesar audios, escribeme un mensaje'
    
    send_whatsapp_message(body, response)


# handle incoming webhook messages
def handle_message(request):
    # Parse Request body in json format
    
    body = request.get_json()
    

    try:
        # info on WhatsApp text message payload:
        # https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks/payload-examples#text-messages
        if body.get("object"):
            if (
                body.get("entry")
                and body["entry"][0].get("changes")
                and body["entry"][0]["changes"][0].get("value")
                and body["entry"][0]["changes"][0]["value"].get("messages")
                and body["entry"][0]["changes"][0]["value"]["messages"][0]
            ):
                handle_whatsapp_message(body)
            return jsonify({"status": "ok"}), 200
        else:
            # if the request is not a WhatsApp API event, return an error
            return (
                jsonify({"status": "error", "message": "Not a WhatsApp API event"}),
                404,
            )
    # catch all other errors and return an internal server error
    except Exception as e:
        print(f"unknown error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


# Required webhook verifictaion for WhatsApp
# info on verification request payload:
# https://developers.facebook.com/docs/graph-api/webhooks/getting-started#verification-requests
def verify(request):
    # Parse params from the webhook verification request
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    # Check if a token and mode were sent
    if mode and token:
        # Check the mode and token sent are correct
        if mode == "subscribe" and token == verify_token:
            # Respond with 200 OK and challenge token from the request
            print("WEBHOOK_VERIFIED")
            return challenge, 200
        else:
            # Responds with '403 Forbidden' if verify tokens do not match
            print("VERIFICATION_FAILED")
            return jsonify({"status": "error", "message": "Verification failed"}), 403
    else:
        # Responds with '400 Bad Request' if verify tokens do not match
        print("MISSING_PARAMETER")
        return jsonify({"status": "error", "message": "Missing parameters"}), 400


# Sets homepage endpoint and welcome message
@app.route("/", methods=["GET"])
def home():
    return "WhatsApp OpenAI Webhook is listening!"


# Accepts POST and GET requests at /webhook endpoint
@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    if request.method == "GET":
        
        return verify(request)
    elif request.method == "POST":

        
        return handle_message(request)


# Route to reset message log
@app.route("/reset", methods=["GET"])
def reset():
    global message_log_dict
    message_log_dict = {}
    return "Message log resetted!"


@app.route("/politicasdeprivacidad")
def poldepriv():
    
    return """

Política de Privacidad del Asistente al Cliente del Restaurante

Política de Privacidad

En nuestro servicio de asistente al cliente para el restaurante, respetamos y protegemos su privacidad. Esta política de privacidad explica cómo recopilamos, usamos y protegemos su información personal.

Información que recopilamos

Recopilamos información personal, como su nombre, dirección de correo electrónico y preferencias de comida, cuando utiliza nuestro servicio.

Uso de la información

Utilizamos la información recopilada para proporcionarle recomendaciones de comida personalizadas, gestionar sus pedidos y mejorar la experiencia de nuestro servicio.

Seguridad

Tomamos medidas para proteger su información personal y garantizar su seguridad mientras utiliza nuestro servicio.

Cookies

Utilizamos cookies para mejorar la experiencia del usuario en nuestro sitio web y personalizar las recomendaciones de comida. Puede configurar su navegador para rechazar las cookies si lo desea.

Enlaces a otros sitios

Nuestro servicio puede contener enlaces a otros sitios web. No somos responsables de las prácticas de privacidad de esos sitios.

Contacto

Si tiene preguntas sobre nuestra política de privacidad, puede contactarnos en [su dirección de correo electrónico].

Esta política de privacidad se actualizó por última vez el [fecha de actualización]."""

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
