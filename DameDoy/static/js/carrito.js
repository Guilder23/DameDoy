document.addEventListener('DOMContentLoaded', function() {
    const carritoBtn = document.getElementById('carritoBtn');
    const carritoDropdown = document.getElementById('carritoDropdown');
    const carritoItems = document.getElementById('carritoItems');
    const carritoContador = document.getElementById('carritoContador');

    // Cargar cantidad inicial
    actualizarCarrito();

    // Toggle dropdown
    carritoBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        carritoDropdown.classList.toggle('show');
        if (carritoDropdown.classList.contains('show')) {
            actualizarCarrito();
        }
    });

    // Cerrar al hacer clic fuera
    document.addEventListener('click', function(e) {
        if (!carritoDropdown.contains(e.target) && !carritoBtn.contains(e.target)) {
            carritoDropdown.classList.remove('show');
        }
    });

    function actualizarCarrito() {
        fetch('/carrito/obtener/')
            .then(response => response.json())
            .then(data => {
                carritoContador.textContent = data.itemCount;
                
                if (data.items.length === 0) {
                    carritoItems.innerHTML = '<div class="carrito-vacio">Tu carrito está vacío</div>';
                    return;
                }
                
                carritoItems.innerHTML = data.items.map(item => `
                    <div class="carrito-item">
                        <img src="${item.imagen || '/static/img/placeholder.png'}" 
                             alt="${item.titulo}"
                             class="carrito-item-img">
                        <div class="carrito-item-info">
                            <div class="carrito-item-titulo">${item.titulo}</div>
                            <div class="carrito-item-precio">$${item.precio}</div>
                        </div>
                        <button onclick="eliminarDelCarrito(${item.id})" class="btn-eliminar-item">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                `).join('');
            });
    }

    // Agregar al carrito desde la lista de materiales
    document.querySelectorAll('.btn-agregar-carrito').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const materialId = this.dataset.materialId;
            
            fetch(`/carrito/agregar/${materialId}/`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        actualizarCarrito();
                        mostrarNotificacion('Material agregado al carrito', 'success');
                    } else {
                        mostrarNotificacion(data.message, 'error');
                    }
                });
        });
    });
});

function eliminarDelCarrito(materialId) {
    fetch(`/carrito/eliminar/${materialId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                actualizarCarrito();
                mostrarNotificacion('Material eliminado del carrito', 'success');
            }
        });
}

function mostrarNotificacion(mensaje, tipo) {
    // Implementar sistema de notificaciones
    alert(mensaje);
}