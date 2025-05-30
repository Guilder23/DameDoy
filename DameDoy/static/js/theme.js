// Función para establecer el tema
function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
}

// Función para alternar el tema
function toggleTheme() {
    const currentTheme = localStorage.getItem('theme') || 'light';
    const newTheme = currentTheme === 'light' ? 'modoOscuro' : 'light';
    setTheme(newTheme);
}

// Inicializar el tema
document.addEventListener('DOMContentLoaded', () => {
    // Verificar preferencia guardada
    const savedTheme = localStorage.getItem('theme');
    // Verificar preferencia del sistema
    const prefersDark = window.matchMedia('(prefers-color-scheme: modoOscuro)').matches;
    
    // Establecer tema inicial
    if (savedTheme) {
        setTheme(savedTheme);
    } else {
        setTheme(prefersDark ? 'modoOscuro' : 'light');
    }
});

function updateThemeIcon() {
    const theme = localStorage.getItem('theme') || 'light';
    const icon = document.getElementById('theme-icon');
    
    if (icon) {
        icon.className = theme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
    }
}

// Actualizar el observer para el cambio de tema
const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        if (mutation.attributeName === 'data-theme') {
            updateThemeIcon();
        }
    });
});

observer.observe(document.documentElement, {
    attributes: true
});

// Actualizar el icono inicial
document.addEventListener('DOMContentLoaded', updateThemeIcon);