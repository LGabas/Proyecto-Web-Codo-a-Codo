(function () {
    'use strict'
    const forms = document.querySelectorAll('.requires-validation')
    Array.from(forms)
      .forEach(function (form) {
        form.addEventListener('submit', function (event) {
          if (!form.checkValidity()) {
            event.preventDefault()
            event.stopPropagation()
          }
    
          form.classList.add('was-validated')
        }, false)
      })
    })()
    
/*function validar() {
      console.log("se envio el formulario")

      formulatio.reset();

      return false;
    }

function confirmar() {

  window.alert("Reserva confirmada, Muchas Gracias")*/  
