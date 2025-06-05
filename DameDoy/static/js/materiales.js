document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('materialModal');
    const modalClose = document.querySelector('.modal-close');

    // Función para abrir el modal
    function abrirModal(data) {
        // Actualizar contenido del modal
        document.getElementById('modalImagen').src = data.imagen;
        document.getElementById('modalTitulo').textContent = data.titulo;
        document.getElementById('modalTipo').textContent = data.tipo;
        document.getElementById('modalEstado').textContent = data.estado;
        document.getElementById('modalEstado').className = `estado estado-${data.estado.toLowerCase()}`;
        document.getElementById('modalFacultad').textContent = data.facultad;
        document.getElementById('modalCarrera').textContent = data.carrera;
        document.getElementById('modalMateria').textContent = data.materia;
        document.getElementById('modalDocente').textContent = data.docente;
        document.getElementById('modalDescripcion').textContent = data.descripcion;
        document.getElementById('modalPrecio').textContent = `$ ${data.precio}`;
        document.getElementById('modalAutor').textContent = data.autor;

        // Mostrar/ocultar botón de carrito
        const btnCarrito = document.getElementById('modalAgregarCarrito');
        if (data.estado.toLowerCase() === 'publicado' && data.autorId !== userId) {
            btnCarrito.style.display = 'flex';
            btnCarrito.dataset.materialId = data.id;
        } else {
            btnCarrito.style.display = 'none';
        }

        // Mostrar modal
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
    }

    // Cerrar modal
    modalClose.addEventListener('click', () => {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    });

    // Cerrar modal al hacer clic fuera
    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    });

    // Cerrar modal con tecla ESC
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.style.display === 'block') {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    });

    // Abrir modal al hacer clic en una tarjeta
    document.querySelectorAll('.material-card').forEach(card => {
        card.addEventListener('click', function(e) {
            // No abrir modal si se hace clic en botones o enlaces
            if (e.target.closest('.btn-agregar-carrito') || 
                e.target.closest('a') ||
                e.target.closest('.acciones')) {
                return;
            }

            // Abrir modal con los datos de la tarjeta
            abrirModal(this.dataset);
        });
    });
});