var traerDatosAPI = function() {
    fetch("https://api.sportmonks.com/v3/football/fixtures?api_token=1LrICjXFK9DxRTljjUjO3uONgMg9EJs58p5V9qXqcJPBEgiXGotj9Rt1Q0Tn", 
        {
            headers: [
                {'Access-Control-Allow-Origin': '*'},
                {'Access-Control-Allow-Credentials': 'true'}
            ]
    }) // API a leer
        // Cuando ha finalizado la lectura
        // guardo en datos el texto leido:
        .then(datos => datos.json()) //res va a guardar el dato mediante el método .json()
        .then(datos => {
            // Y luego copio ese texto en #contenido.
            console.log(datos)
        })
}