document.addEventListener("DOMContentLoaded", function() {
    function toggleCiteField() {
        var tipoSelect = document.querySelector("#id_tipo");
        var citeField = document.querySelector(".form-row.field-cite");

        if (tipoSelect && citeField) {
            if (tipoSelect.value === "saliente") {
                citeField.style.display = "block";  // Mostrar cite
            } else {
                citeField.style.display = "none";   // Ocultar cite
            }
        }
    }

    var tipoField = document.querySelector("#id_tipo");
    if (tipoField) {
        tipoField.addEventListener("change", toggleCiteField);
        toggleCiteField();  // Ejecutar al cargar la página
    }
});
