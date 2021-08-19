const mysql = require('mysql');
const squel = require('squel');

let conexion = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: '',
    database: 'vigilantes'
});

conexion.connect;
let consulta = squel.select()
    .field('Nombre')
    .from('usuarios')

conexion.query(consulta.toString(), function(error, registros,campo){
    if(error){
        throw error;
    }
    registros.forEach(function (registro, indice, arreglo) {
        console.log(registro.Nombre)
    });
    conexion.end();
})