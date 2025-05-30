
function toggleEdicion() {
    const form = document.getElementById('formPerfil');
    const inputs = form.querySelectorAll('input:not([type="file"]), textarea');
    const acciones = form.querySelector('.perfil-acciones');
    const fotoCampo = form.querySelector('.foto-campo');
    
    inputs.forEach(input => {
        input.disabled = !input.disabled;
    });
    
    acciones.style.display = inputs[0].disabled ? 'none' : 'flex';
    fotoCampo.style.display = inputs[0].disabled ? 'none' : 'block';
}

function cancelarEdicion() {
    const form = document.getElementById('formPerfil');
    const inputs = form.querySelectorAll('input:not([type="file"]), textarea');
    const acciones = form.querySelector('.perfil-acciones');
    const fotoCampo = form.querySelector('.foto-campo');
    
    inputs.forEach(input => {
        input.disabled = true;
        input.value = input.defaultValue;
    });
    
    acciones.style.display = 'none';
    fotoCampo.style.display = 'none';
}