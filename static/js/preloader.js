center_preloader = document.getElementById('center_preloader');
window.onload = function(){
    center_preloader.classList.add('off');
    center_preloader.classList.remove('flex')
    $('body').remove('#hidden');
    //eliminarElemento('center_preloader')
}
function cargando() {
    center_preloader.classList.add('flex');
    center_preloader.classList.remove('off')
    $('body').addClass('hidden');

}

function eliminarElemento(id){
	im = document.getElementById(id);	
	if (!im){
        console.log('el elemento no existe')
		//alert("El elemento selecionado no existe");
	} else {
		padre = imagen.parentNode;
		padre.removeChild(im);
	}
}