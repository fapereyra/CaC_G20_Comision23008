//INICIO DE BOTONES DEL HEADER
function backHome(){
    var backhome = <a href="index,html"></a>
    return backhome
}

function consultas(){
    var consultas = <a href="consultas.html"></a>
    return consultas
}

function deportes(){
    var deportes = <a href="deportes.html"></a>
    return deportes
}

function institucional(){
    var institucioanl = <a targert="_blank" href="institucioanl.html"></a>
    return institucioanl
}

//FIN DE BOTONES DEL HEADER
//INICIO DEL SCRIPT FOOTER

class Footer{
    constructor(integrantes, sitio, fecha){
    this.integrantes = integrantes
    this.sitio = sitio
    this.fecha = fecha
    }
}

var mifooter = new Footer("Francisco pereyra - Hugo Fotunato - David Frias - Fabricio Denuncio", "club social deportivo", crearFecha())

function crearFecha(){
    var fecha = new Date()
    return fecha
}

function crearHeader(){
    var texto = "soy el header"
    return texto
}

function mostrarHeader(){
    document.write(crearHeader())
}
//ANTES FUNCIONABA ESTA FUNCTION, PERO POR ALGUNA RÁZON NO ME DEJA ACCEDER AL OBJETO
function crearFooter(){
    var texto = `Trabajo realizado por ${this.integrantes} para el sitio ${this.sitio}.`
    return texto
}

function mostrarFooter(){
    document.write(crearFooter())   
}