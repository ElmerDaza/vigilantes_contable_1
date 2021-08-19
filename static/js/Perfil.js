ID_perfil = document.getElementById('ID_perfil');
ID_transacciones = document.getElementById('ID_transacciones');
ID_Estado = document.getElementById('ID_Estado')

ID_perfil.addEventListener('click',()=>{
    ventana_vew('perfil')
});
ID_transacciones.addEventListener('click',()=>{
    ventana_vew('transacciones')
});
ID_Estado.addEventListener('click',()=>{
    ventana_vew('estado')
});



function ventana_vew(e) {
    perfil_usuario = document.getElementById('perfil_usuario');
    Transacciones = document.getElementById('Transacciones');
    Estado_Cuenta = document.getElementById('Estado_Cuenta');
    if (e==='perfil') {
        perfil_usuario.classList.remove('off');
        Transacciones.classList.add('off')
        Estado_Cuenta.classList.add('off')
    }else if(e==='transacciones'){
        perfil_usuario.classList.add('off')
        Transacciones.classList.remove('off');
        Estado_Cuenta.classList.add('off')

    }else if(e==='estado'){
        perfil_usuario.classList.add('off')
        Transacciones.classList.add('off');
        Estado_Cuenta.classList.remove('off');
    }
}