# CryptoAware
### Instalacion:
- Instalar las libs necesarias corriendo el siguiente comando:
    ```
    pip install -r libs.txt
    ```
### Distribucion de los directorios:
- CryptoAPIs:
    - Contiene el sitio desarrollado en django
        - CryptoAPIs: contiene la configuracion de django
        - historial: contiene las vistas del sitio
- Historial:
    - Contiene el data collector de los precios de las criptomonedas.
    - GetData.py:
        - Genera archivos csv cada 24 horas. Cada 1 hora consulta la API.
    - PlotData.py:
        - Genera graficos a partir de los csv generados por GetData.py

### Ejecucion local
Para correr la pagina de manera local se debe ejecutar el siguiente comando en /CyptoAPIs/:
```
python manage.py runserver
```
### Pendientes/Trabajo futuro
- Pendiente: Integrar codigo Raul , algoritmos miguel
- Pendiente: Pasarlo a ingles PoC
