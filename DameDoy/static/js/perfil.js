const inputs = document.querySelectorAll('input');
    const toggleBtn = document.getElementById('toggleBtn');
    let bloqueado = false;

    toggleBtn.addEventListener('click', () => {
      bloqueado = !bloqueado;
      inputs.forEach(el => el.disabled = bloqueado);
      toggleBtn.textContent = bloqueado ? 'Editar' : 'No editar';
    });

document.addEventListener('DOMContentLoaded', function() {
    const toggleBtn = document.getElementById('toggleBtn');
    const form = document.getElementById('form-perfil');
    let editando = false;

    // Configurar los input de archivos para autoguardado
    const fotoInput = document.getElementById('id_foto');
    const fotoPortadaInput = document.getElementById('id_foto_portada');

    fotoInput?.addEventListener('change', function() {
        subirImagen(this, 'foto', '.perfil-foto');
    });

    fotoPortadaInput?.addEventListener('change', function() {
        subirImagen(this, 'foto_portada', '.portada-img');
    });

    // Función para subir imagen
    function subirImagen(input, tipo, selector) {
        if (input.files && input.files[0]) {
            const formData = new FormData();
            formData.append(tipo, input.files[0]);
            formData.append('tipo', tipo);
            
            // Mostrar vista previa inmediata
            mostrarVistaPrevia(input, selector);

            // Enviar la imagen al servidor
            fetch('/actualizar-imagen/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Mostrar mensaje de éxito
                    mostrarNotificacion('Imagen actualizada con éxito', 'success');
                } else {
                    // Mostrar mensaje de error
                    mostrarNotificacion('Error al actualizar la imagen', 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                mostrarNotificacion('Error al actualizar la imagen', 'error');
            });
        }
    }

    // Función para mostrar notificaciones
    function mostrarNotificacion(mensaje, tipo) {
        const notificacion = document.createElement('div');
        notificacion.className = `notificacion ${tipo}`;
        notificacion.innerHTML = `
            <i class="fas ${tipo === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
            ${mensaje}
        `;
        document.body.appendChild(notificacion);

        // Remover la notificación después de 3 segundos
        setTimeout(() => {
            notificacion.remove();
        }, 3000);
    }

    // Resto del código existente para el formulario
    if (toggleBtn && form) {
        toggleBtn.addEventListener('click', function() {
            editando = !editando;
            // Mostrar/ocultar formulario
            form.style.display = editando ? 'block' : 'none';
            
            // Habilitar/deshabilitar campos
            const inputs = form.querySelectorAll('input:not([type="file"]), textarea, select');
            inputs.forEach(input => {
                input.disabled = !editando;
            });

            // Cambiar texto del botón
            toggleBtn.innerHTML = editando ? 
                '<i class="fas fa-times"></i> Cancelar' : 
                '<i class="fas fa-pencil-alt"></i> Editar información';
        });
    }
});

// Función para previsualizar imágenes
function mostrarVistaPrevia(input, selector) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const imagen = document.querySelector(selector);
            if (imagen) {
                imagen.src = e.target.result;
            }
        };
        reader.readAsDataURL(input.files[0]);
    }
}
