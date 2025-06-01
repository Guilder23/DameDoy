function mostrarQR(vendedor) {
    const modal = document.getElementById(`qrModal${vendedor}`);
    modal.style.display = "block";
}

function cerrarQR(vendedor) {
    const modal = document.getElementById(`qrModal${vendedor}`);
    modal.style.display = "none";
}

// Cerrar al hacer clic fuera del modal
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = "none";
    }
}