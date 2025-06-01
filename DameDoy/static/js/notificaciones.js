document.addEventListener('DOMContentLoaded', function() {
    const notifBtn = document.getElementById('notifBtn');
    const notifDropdown = document.getElementById('notifDropdown');
    const notifContador = document.getElementById('notifContador');

    // Toggle dropdown
    notifBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        notifDropdown.classList.toggle('show');
        if (notifDropdown.classList.contains('show')) {
            cargarNotificaciones();
        }
    });

    // Cerrar al hacer clic fuera
    document.addEventListener('click', function(e) {
        if (!notifDropdown.contains(e.target) && !notifBtn.contains(e.target)) {
            notifDropdown.classList.remove('show');
        }
    });

    // Cargar notificaciones
    function cargarNotificaciones() {
        fetch('/notificaciones/recientes/')
            .then(response => response.json())
            .then(data => {
                actualizarNotificaciones(data.notificaciones);
                actualizarContador(data.no_leidas);
            });
    }

    // Actualizar notificaciones en el dropdown
    function actualizarNotificaciones(notificaciones) {
        const contenedor = document.getElementById('notifItems');
        
        if (notificaciones.length === 0) {
            contenedor.innerHTML = '<div class="notif-vacia">No hay notificaciones nuevas</div>';
            return;
        }

        contenedor.innerHTML = notificaciones.map(notif => {
            let accionHtml = '';
            
            if (notif.tipo === 'pago_recibido') {
                if (notif.compra && notif.compra.estado === 'pagado') {
                    accionHtml = `
                                    ${notif.imagen ? `<img src="${notif.imagen}" class="notif-img" alt="Imagen">` : ''}
                        <a href="/verificar-pago/${notif.referencia_id}/" class="btn-verificar">
                            <i class="fas fa-check"></i> Verificar pago
                        </a>`;
                } else if (notif.compra && notif.compra.estado === 'confirmado') {
                    accionHtml = `
                        <span class="estado-badge confirmado">
                            <i class="fas fa-check-circle"></i> Pago verificado
                        </span>`;
                } else if (notif.compra && notif.compra.estado === 'rechazado') {
                    accionHtml = `
                        <span class="estado-badge rechazado">
                            <i class="fas fa-times-circle"></i> Pago rechazado
                        </span>`;
                }
            }

            return `
                <div class="notif-item ${!notif.leida ? 'no-leida' : ''}">
                    ${notif.imagen ? `<img src="${notif.imagen}" class="notif-img" alt="Imagen">` : ''}
                    <div class="notif-content">
                        <h4>${notif.titulo}</h4>
                        <p>${notif.mensaje}</p>
                        <span class="notif-fecha">${notif.fecha_relativa}</span>
                    </div>
                    ${accionHtml}
                </div>
            `;
        }).join('');
    }

    // Actualizar contador
    function actualizarContador(cantidad) {
        const notifContador = document.getElementById('notifContador');
        if (cantidad > 0) {
            notifContador.textContent = cantidad;
            notifContador.style.display = 'flex';
        } else {
            notifContador.style.display = 'none';
        }
    }

    // Marcar todas como leídas
    window.marcarTodasComoLeidas = function() {
        fetch('/notificaciones/marcar-leidas/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                cargarNotificaciones();
            }
        });
    };

    // Función auxiliar para obtener cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Cargar notificaciones iniciales y actualizar cada minuto
    cargarNotificaciones();
    setInterval(cargarNotificaciones, 60000);
});