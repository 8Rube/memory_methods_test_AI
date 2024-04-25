# memory_methods_test_AI
Metodos de memoria a largo y corto plazo: 

# Metodo de almacenamient y carga de logs
El metodo de logs almacena el input y el output del chatbot para sumarlo al siguiente input esto debe ser previamente entrenado ya que los modelos transformers suelen repetirse con facilidad y podria repetir la misma respuesta indiscriminadamente, en el entrenamiento se debe tener en cuenta como sera el formato que se use para almacenar y cargar los logs como por ejemplo {"usuario": "hola que tal", "chatbot": "buenas tardes, estoy bien"} como informacion adicional se tiene que mencionar que este metodo solo es viable a corto plazo o quizas con otro enfoque ya que dependiendo de la memoria de la GPU acabara fallando por falta de recursos.

# Metodo de carga de Datasets
Este metodo tiene menos problemas y es mas simple esto de misma forma almacena informacion de inputs y outputs anteriores pero en vez de sumarlos lo une en un archivo Dataset que en termino simples seria un entrenamiento cargado para la sesion, tambien se debe recordar que se debe usar el formate previamente entrenado para evitar repeticion, lado positivo es que no ocupa tanta memoria de la gpu, este metodo es incapaz de recordar con exactitud los datos pero le dara contexto y le permite aprender de si misma en tiempo real, cualquier clase de aprendisaje requiere supervision o algun metodo de control para evitar contaminacion en los datos que puedan volver propenso texto no deseado en la generacion


# Sobre los modelos
Se esta usando como base el modelo gpt2-medium el cual entrene para poder funcionar como chatbot, el codigo del repositorio es con fin educativo no demostrativo ya que requiere integracion de base de datos y hosting, para ser usado requiere previa preparacion y fine-tuning, ademas de permisos de administrador.

