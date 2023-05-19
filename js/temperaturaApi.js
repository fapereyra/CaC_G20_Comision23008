function traerDatosAPI() {
    fetch('https://yandex.com/dev/weather/') // API a leer
        // Cuando ha finalizado la lectura
        // guardo en datos el texto leido:
        .then(datos => datos.json()) //res va a guardar el dato mediante el método .json()
        .then(datos => {
            // Y luego copio ese texto en #contenido.
            console.log(datos)
        })
}
