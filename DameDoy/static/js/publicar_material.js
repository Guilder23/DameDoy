document.addEventListener('DOMContentLoaded', function() {
    const formMaterial = document.getElementById('formMaterial');
    const inputImagen = document.getElementById('imagen');
    const previewContainer = document.getElementById('imagenPreview');

    // Validación del formulario
    formMaterial.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const campos = ['titulo', 'tipo', 'facultad', 'carrera', 'materia', 
                       'docente', 'descripcion', 'precio', 'imagen'];
        
        let valido = true;
        
        // Validar campos
        campos.forEach(campo => {
            const elemento = document.getElementById(campo);
            if (!elemento.value.trim()) {
                elemento.classList.add('invalid');
                valido = false;
            } else {
                elemento.classList.remove('invalid');
            }
        });

        // Validar imagen
        if (inputImagen.files.length > 0) {
            const file = inputImagen.files[0];
            if (file.size > 5 * 1024 * 1024) { // 5MB
                mostrarError('La imagen no debe superar los 5MB');
                valido = false;
            }
            if (!['image/jpeg', 'image/png'].includes(file.type)) {
                mostrarError('Solo se permiten imágenes JPG y PNG');
                valido = false;
            }
        }

        if (valido) {
            this.submit();
        } else {
            mostrarError('Por favor completa todos los campos obligatorios correctamente');
        }
    });

    // Preview de imagen
    inputImagen.addEventListener('change', function() {
        const file = this.files[0];
        
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                previewContainer.innerHTML = `
                    <img src="${e.target.result}" alt="Vista previa">
                `;
            }
            reader.readAsDataURL(file);
        }
    });

    // Remover clase invalid al escribir
    document.querySelectorAll('input, select, textarea').forEach(elemento => {
        elemento.addEventListener('input', function() {
            if (this.value.trim()) {
                this.classList.remove('invalid');
            }
        });
    });

    // Función auxiliar para mostrar errores
    function mostrarError(mensaje) {
        const alertContainer = document.querySelector('.alert-error') || 
                             crearAlertaError();
        alertContainer.innerHTML = `<div>${mensaje}</div>`;
    }

    function crearAlertaError() {
        const alerta = document.createElement('div');
        alerta.className = 'alert alert-error';
        formMaterial.insertBefore(alerta, formMaterial.firstChild);
        return alerta;
    }
});