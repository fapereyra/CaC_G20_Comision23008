//INICIO DE BOTONES DEL HEADER
function backHome(){
    var backhome = '<a href= "index.html" link ></a>'
    return backhome
}

function consultas(){
    var consultas = '<a href= "consultas.html" link ></a>'
    return consultas
}

function deportes(){
    var deportes = '<a href= "deportes.html" link ></a>'
    return deportes
}

function institucional(){
    var institucional = `<a href= "institucional.html">INSTITUCIONAL</a>` 
    return institucional
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