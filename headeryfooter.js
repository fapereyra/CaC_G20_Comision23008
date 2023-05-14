class Header{
    constructor(index, deportes, consultas, institucional){
        this.index = index
        this.deportes = deportes
        this.consultas = consultas
        this.institucional = institucional
    }
}
var miheader = new Header("<a href=index.html>INDEX</a>", "<a href=deportes.html>DEPORTES</a>", "<a href=consultas.html>CONSULTAS</a>", "<a href=institucional.html>INSTITUCIONAL</a>")

//INICIO DE BOTONES DE HEADER//
//BOTON INDEX//
function linkIndex(){
    var link = `${miheader.index}`
    return link
}
function botonIndex(){
    document.write(linkIndex())
}

//BOTON DEPORTES//
function linkDeportes(){
    var link = `${miheader.deportes}`
    return link
}
function botonDeportes(){
    document.write(linkDeportes())
}

//BOTON CONSULTAS//
function linkConsultas(){
    var link = `${miheader.consultas}`
    return link
}
function botonConsultas(){
    document.write(linkConsultas())
}

//BOTON INSTITUCIONAL//
function linkInstitucional(){
    var link = `${miheader.institucional}`
    return link
}
function botonInstitucional(){
    document.write(linkInstitucional())
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

var mifooter = new Footer("Francisco pereyra - Fabricio Denuncio", "club social deportivo", crearFecha())

function crearFecha(){
    var fecha = new Date()
    return fecha
}

function crearFooter(){
    var texto = `Trabajo realizado por ${mifooter.integrantes} para el sitio ${mifooter.sitio}. - ${mifooter.fecha}`
    return texto
}

function mostrarFooter(){
    document.write(crearFooter())   
}