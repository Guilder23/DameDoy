django.jQuery(function($) {
    var $universidad = $('#id_universidad');
    var $facultad = $('#id_facultad');
    var $carrera = $('#id_carrera');
    var $materia = $('#id_materia');

    function actualizarSelect($target, url, data) {
        $.get(url, data, function(response) {
            $target.empty().append($('<option>').val('').text('---------'));
            response.forEach(function(item) {
                var texto = item.siglas ? `${item.siglas} - ${item.nombre}` : 
                           item.codigo ? `${item.codigo} - ${item.nombre}` : 
                           item.nombre;
                $target.append($('<option>').val(item.id).text(texto));
            });
            $target.prop('disabled', false);
        });
    }

    function limpiarSelects($selects) {
        $selects.empty()
                .append($('<option>').val('').text('---------'))
                .prop('disabled', true);
    }

    // Universidad -> Facultad
    $universidad.change(function() {
        var universidadId = $(this).val();
        limpiarSelects($facultad.add($carrera).add($materia));
        
        if (universidadId) {
            actualizarSelect($facultad, '/api/facultades/', {universidad: universidadId});
        }
    });

    // Facultad -> Carrera
    $facultad.change(function() {
        var facultadId = $(this).val();
        var universidadId = $universidad.val();
        limpiarSelects($carrera.add($materia));
        
        if (facultadId && universidadId) {
            actualizarSelect($carrera, '/api/carreras/', {
                universidad: universidadId,
                facultad: facultadId
            });
        }
    });

    // Carrera -> Materia
    $carrera.change(function() {
        var carreraId = $(this).val();
        var facultadId = $facultad.val();
        var universidadId = $universidad.val();
        limpiarSelects($materia);
        
        if (carreraId && facultadId && universidadId) {
            actualizarSelect($materia, '/api/materias/', {
                universidad: universidadId,
                facultad: facultadId,
                carrera: carreraId
            });
        }
    });

    // Si estamos editando, pre-seleccionar los valores
    if ($universidad.val()) {
        var universidadId = $universidad.val();
        var facultadId = $facultad.data('initial');
        var carreraId = $carrera.data('initial');
        var materiaId = $materia.data('initial');

        // Cargar facultades
        actualizarSelect($facultad, '/api/facultades/', {universidad: universidadId});

        if (facultadId) {
            setTimeout(function() {
                $facultad.val(facultadId).trigger('change');
                
                // Cargar carreras
                actualizarSelect($carrera, '/api/carreras/', {
                    universidad: universidadId,
                    facultad: facultadId
                });

                if (carreraId) {
                    setTimeout(function() {
                        $carrera.val(carreraId).trigger('change');
                        
                        // Cargar materias
                        actualizarSelect($materia, '/api/materias/', {
                            universidad: universidadId,
                            facultad: facultadId,
                            carrera: carreraId
                        });

                        if (materiaId) {
                            setTimeout(function() {
                                $materia.val(materiaId);
                            }, 500);
                        }
                    }, 500);
                }
            }, 500);
        }
    }
});