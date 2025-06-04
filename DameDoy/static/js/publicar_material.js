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

$(document).ready(function() {
    // Inicializar Select2
    $('.select2').select2({
        width: '100%',
        placeholder: 'Buscar...',
        allowClear: true
    });

    // Función para eliminar duplicados y actualizar select
    function actualizarSelectSinDuplicados($select, url, params) {
        $select.empty().prop('disabled', true);
        $select.append('<option value="">Seleccione una opción</option>');

        if (!params) return;

        $.ajax({
            url: url,
            data: params,
            success: function(data) {
                // Usar Map para mantener solo una opción por texto mostrado
                const opcionesUnicas = new Map();

                data.forEach(function(item) {
                    let texto = item.siglas ? 
                        `${item.siglas} - ${item.nombre}` : 
                        item.codigo ? 
                        `${item.codigo} - ${item.nombre}` : 
                        item.apellido ?
                        `${item.apellido}, ${item.nombre}` :
                        item.nombre;

                    // Si el texto ya existe, no lo agregamos
                    if (!opcionesUnicas.has(texto)) {
                        opcionesUnicas.set(texto, item);
                    }
                });

                // Convertir el Map a Array y ordenar
                const opcionesOrdenadas = Array.from(opcionesUnicas.values())
                    .sort((a, b) => {
                        const textoA = a.codigo || a.siglas || a.apellido || a.nombre;
                        const textoB = b.codigo || b.siglas || b.apellido || b.nombre;
                        return textoA.localeCompare(textoB);
                    });

                // Agregar las opciones ordenadas y únicas
                opcionesOrdenadas.forEach(function(item) {
                    let texto = item.siglas ? 
                        `${item.siglas} - ${item.nombre}` : 
                        item.codigo ? 
                        `${item.codigo} - ${item.nombre}` : 
                        item.apellido ?
                        `${item.apellido}, ${item.nombre}` :
                        item.nombre;

                    $select.append(
                        `<option value="${item.id}">${texto}</option>`
                    );
                });

                $select.prop('disabled', false);
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                $select.append('<option value="">Error al cargar datos</option>');
            }
        });
    }

    // Universidad -> Facultad
    $('#universidad').change(function() {
        const universidadId = $(this).val();
        $('#facultad, #carrera, #materia, #docente').empty().prop('disabled', true);
        
        if (universidadId) {
            actualizarSelectSinDuplicados($('#facultad'), '/api/facultades/', {
                universidad: universidadId
            });
        }
    });

    // Facultad -> Carrera
    $('#facultad').change(function() {
        const facultadId = $(this).val();
        $('#carrera, #materia, #docente').empty().prop('disabled', true);
        
        if (facultadId) {
            actualizarSelectSinDuplicados($('#carrera'), '/api/carreras/', {
                facultad: facultadId
            });
        }
    });

    // Carrera -> Materia
    $('#carrera').change(function() {
        const carreraId = $(this).val();
        $('#materia, #docente').empty().prop('disabled', true);
        
        if (carreraId) {
            actualizarSelectSinDuplicados($('#materia'), '/api/materias/', {
                carrera: carreraId
            });
        }
    });

    // Materia -> Docente
    $('#materia').change(function() {
        const materiaId = $(this).val();
        $('#docente').empty().prop('disabled', true);
        
        if (materiaId) {
            actualizarSelectSinDuplicados($('#docente'), '/api/docentes/', {
                materia: materiaId
            });
        }
    });
});