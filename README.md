[![uclm](https://img.shields.io/badge/uclm-esi-red.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAPCAYAAAA71pVKAAAC9UlEQVR42o3S3UtTYRwH8F//QhBE3WT0elGr6CZUCLzoRUQt6ibICrESS1MDi7pJwcSXgsCGlG+1LFFzzpzONqduTp3TqVO36V7OzubZ2TznbDvn7NW5nmlXWdADPzg8/D6c3/N9HohSDPCrDgg53bDJByERj0OEpCCEE8cjXlrJaBbOcys2iHpp1OOBgN4MaG/b/BXHfKxgkwuaNvkQE6X8WNDiTI16qP/AicTlMElPeeXTtdTY7G1Kpa/iLU5dnONvhHDyH9hBJGEGu2RV2t93PWaXrb2xAO/kTJgMb5EUM9MGWZQJ5PrnTH9gMwYx2n865PLOrr5uK+XXcLV/YfUD3t5fFFgwN0Y89JzlTUcxb3PNc2YsjVHrdzAKBX1gh+KhsIXokgtJqbopxvIvEa7y600i38xSnXd4qpwa1zcTvcqGqNdHMBPzpzijHSDGcic2WV4Xj0QTGwptBd4meejTGb+gKcS+acMD1mj7Ro3OfcWE3fddnbJnKMRExMuYglbXWUCjjCTQitEBu2dQU05rFp6gsOrJftXzqI9d8gxpajzDk9XUqK6MVs+Xx9igLtnPmewz4GiRnEFprmxtbSXWO4crUCgVrs7hfDTyeLIpiBG29a6fBTxGlPkX116grQBrwnBHq+QCOD9LwflpQIDSNVAjM8IQSVWQfWN1lgZRQRLjH8WF7h5FJW9brww63I2c2WG0N/WkOUVSAHJADZ6BCXAIu/eiP9ehs79Do97xzxrbk5hdsYo9UlVejAnU0lOGFnvT932ubsW2A01WMUxml8Bo2l3QZD7ai+6wnLc5XyGnSuyslTC5UYOOUTJz/enBifR80GaXgjanDGAoJRMGU67Cj/0ZMJZ+DyzVrYdplT4PocXf2B4wWIrwVslJzcUCkB+4AiNHc1HlAMgFN7dr6EgWqC8VgrVeBI7mPkBPUZuUYfeGlehR7HGhbKYzi0F57BqMn7uVrN3Y9rYD0HMEontE4NMuK7yyyVS3WAmujqFd+Bcdh3NlWlsAggAAAABJRU5ErkJggg==&longCache=true&colorA=b30135&colorB=555555&style=for-the-badge)](https://www.esi.uclm.es)  

# Laboratorio de Sistemas Distribuidos (2019-2020)
## Autores:
[Mario Pérez](https://github.com/mapecode)  
[David Camuñas](https://github.com/dcamunas)

[Repositorio](https://github.com/mapecode/PerezCamunas)

## Requerimientos
* zeroc-ice: **sudo apt install python3-zeroc-ice**
* icebox: **sudo apt install zeroc-ice-icebox**
* ice-utils: **sudo apt install zeroc-ice-utils**
* youtube-dl: **pip3 install youtube-dl**
* ffmpeg: **sudo apt install ffmpeg**

## Manual de usuario
### Ejecución en un solo host
* Ejecutar el script [run_server.sh](run_server.sh): creará los directorios necesarios y lanzará los icegridnodes
* Ejecutar icegridgui
    * Conectar con el registry
    * Cargar aplicación [YoutubeDownloaderApp.xml](YoutubeDownloaderApp.xml) y guardar en el registry
    * Ejecutar los servidores en el siguiente orden:
        * registry-node
        * downloads-node
        * orchestrator-node
        
### Ejecución en dos hosts
* Copiar archivos de la práctica en ambos hosts
* Cambiar la dirección ip de las configuraciones del locator por la ip del host 1
* Crear los directorios necesarios en ambos hosts: **make app-workspace**
* Ejecutar el nodo registry-node y orchestrator-node en el host 1
* Ejecutar el nodo downloads-node en el host 2
* Ejecutar icegridgui en un host y realizar mismos pasos descritos anteriormente

### Realizar peticiones
* Petición de descarga: make run-client-download
* Petición de listar descagas: make run-client-list
* Petición de transferencia: make run-client-transfer (esta petición no tiene sentido si lanzamos el sistema en un solo host)

Para las peticiones de descarga y transferencia se pedirá por teclado la url en el primer caso y el nombre del archivo
a transferir en el segundo caso.

### Apagar sistema
* Matar los icegridnode: make stop
* Eliminar directorios creados: make clean     
