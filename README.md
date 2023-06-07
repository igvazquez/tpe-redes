# Grafana &amp; Prometheus demo
## Consigna
1) Crear una red virtual o real a monitorear, de al menos 4 hosts.
2) Configurar el monitoreo de al menos dos características de hardware de un servidor.
3) Configurar el monitoreo de un servicio web, usando pasos secuenciales dentro de la navegación de sitio.
4) Configurar alertas por tiempos de respuestas en un sitio web.
5) Configurar monitoreo de al menos 2 servicios (API REST, HTTP, SMTP, etc.)
6) Configurar alarmas con distintos niveles según el tiempo de caída de servicio a distintos administradores u operadores.

Realizaremos una demo de Grafana en la cual implementamos la siguiente arquitectura

![Diagrama](/images/docker.png)

## Requerimientos
### Docker
Es necesario tener Docker instalado en su sistema y tener el servicio corriendo. Recomendamos visitar en el [Sitio oficial de Docker](https://docs.docker.com/get-docker/) la guía de instalación adecuada para el sistema operativo de su ordenador. 
### Docker Compose
Docker Compose está disponible para Windows, Mac OS y Linux. En el [Sitio oficial de Docker Compose](https://docs.docker.com/compose/install/) podemos encontrar una guía para instalar el mismo.
### Web Browser
Google Chrome, Firefox u cualquier otro navegador desde el cual acceder a la interfaz web de usuario de Grafana

## Set up
```
git clone https://github.com/igvazquez/tpe-redes.git
```

```
docker compose up
```

## Implementacion

Para ello, usamos Docker Compose para definir de manera declarativa los contenedores a utilizar, los puertos a exponer y las redes para compartir datos entre los servicios.Podemos ver que optamos por dividir los containers dentro de 3 redes intentando aislarlos para que tengan visibilidad mínima cuando no fuese necesario que sean observados.

Si clonamos el repositorio y corremos el comando ```docker compose up``` se correrán todos los contenedores necesarios para el funcionamiento de Grafana y los servicios a monitorear. Una vez levantados, podemos verificar el funcionamiento de Grafana accediendo a ```localhost:3000```. Se debería encontrar configurado el datasource, en este caso Prometheus.

Grafana necesita un datasource que se encargue de disponer los datos para que pueda graficarlos, existen múltiples opciones pero la más utilizada y la elegida por nosotros es Prometheus, la misma registra las métricas en una base de datos de series temporales y tiene una interfaz gráfica a la cual podemos acceder en ```localhost:9090```. Prometheus se encarga de scrapear las métricas y para esto es necesario declarar los targets que debe observar y cada cuanto hacer el scrape, en nuestro caso se observan los exporters y el endpoint de la API de Python que se explicará más adelante. En la pestaña de targets verificamos que se están consiguiendo correctamente los datos. 

Este datasource tiene su propio lenguaje de querys llamado PromQL (Prometheus query language), que nos permite acceder a las métricas y disponerlas a Grafana para realizar los gráficos.
 
Para cumplir con el objetivo del trabajo, primero nos encargamos de adquirir métricas de hardware para luego poder generar dashboards dentro de Grafana. Para esto encontramos Node Exporter, los "exporters" que vamos a estar mencionando son los encargados de exponer un endpoint, generalmente "/metrics", en donde se pueden acceder a las métricas de datos de un servicio en particular en el formato que Prometheus necesita.

Luego, para el monitoreo de un sitio web utilizamos BlackBox Exporter que nos permite sondear múltiples endpoints con diferentes protocolos e ir verificando, por ejemplo, el código de respuesta. Con esta herramienta observamos al servidor de apache y le pedimos distintas páginas estáticas además de realizar un request a un endpoint lento dentro de la API de Python, simulando el uso de un usuario dentro de un sitio web y capturando las métricas.

Las alertas son configuradas a través de reglas. Podemos crear una alerta administrada por Grafana a partir de una query con PromQL sobre alguno de los datasource configurados y enlazar condicionales de distintos tipos que activan la alarma. Además se puede configurar el tiempo de evaluación de estos condicionales.

![](/images/alerts.png)

y también se pueden setear etiquetas que funcionan como triggers para las políticas de notificación.

![](/images/labels.png)

Puntualmente configuramos notificaciones para enviar mensajes por mail vía el servidor smtp de google informando a distintos usuarios dependiendo el tiempo de caída del servicio. Si está caído durante 10 segundos se le informa al operador y si está caído por más de 30 segundos se le informa al administrador de la red. La configuracion global de Grafana se describe en el archivo defaults.ini.

```ini
...
#################################### SMTP / Emailing #####################
[smtp]
enabled = true
host = smtp.gmail.com:587
user = alertas.grafana.redes@gmail.com
password = cvqqkieykenjzmdx
cert_file =
key_file =
skip_verify = false
from_address = alertas.grafana.redes@gmail.com
from_name = Grafana
ehlo_identity =
startTLS_policy =
...
``` 


Los servicios que vamos a monitorear son una API en Python utilizando Flask y su base de datos Postgres, utilizando Postgres Exporter. Para las métricas de la API existe un cliente de Prometheus para Python y también un exporter particular para Flask, esto nos permite tener métricas como el tiempo de respuesta, cantidad de requests al endpoint, etc.

