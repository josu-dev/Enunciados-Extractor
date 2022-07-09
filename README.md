# Enunciados Extractor

Esta es una herramienta para reconocer y extraer enunciados desde archivos de texto plano con el objetivo de transformarlos a formato json para ser usados en otra aplicacion/herramienta que consuma estos datos.

Se extraen los tipos:

- Multiple choice
- En un futuro pueden haber mas

Indice

- [Requerimientos](#requerimientos)
- [Como usar](#como-usar)
- [Generar txt](#generar-txt)


&nbsp;

## Requerimientos

Se requiere:

- python >= 3.10

&nbsp;

## Como usar

1. Primero obtener el codigo:

    Clonar el ropositorio

    Descargar el .zip, en este caso descomprimirlo

1. Abrir la carpeta con el explorador de archivos

    Una vez abierta colocar los archivos de texto (estension .txt) que se quieren procesar en la carpeta ***input***

    > En [Generar txt](#generar-txt) hay ayuda para obtener archivos de texto de otros formatos

1. Abrir una terminal en la misma carpeta

1. Ejecutar el archivo ***enunciados.py***

    ```bash
    py enunciados.py
    ```

1. El resultado del procesamiento se encontrara en la carpeta ***output***

&nbsp;

## Generar txt

Si los datos de entrada no estan en formato de texto plano y no podes pasarlo a este, intenta con alguno de los siguientes metodos:

- .pdf

    Para pasar un pdf a texto plano una de las manera mas sencillas es usando [Google Docs](https://docs.google.com/document)

    Para hacerlo simplemente:

    1. Abri el pdf en docs

    1. Una vez abierto, solo usa la herramienta que se encuentra en la seccion Archivo -> Descargar -> Texto sin formato

    1. Solo revisa que el contenido del .txt generado tenga sentido y listo

- otros...
