new Vue({
    el: '#app',
    data: {
        reservas: [],
        reserva: {},
        filtroId: '',
        formTitle: 'Crear Reserva',
        buttonLabel: 'Guardar'
    },
    created() {
        this.obtenerReservas();
    },
    computed: {
        reservasFiltradas() {
            if (this.filtroId.trim() !== '') {
                return this.reservas.filter(reserva => reserva.id === parseInt(this.filtroId));
            }
            return this.reservas;
        }
    },
    methods: {
        obtenerReservas() {
            axios.get('https://turismomardel2023.pythonanywhere.com/reservas')
                .then(response => {
                    this.reservas = response.data;
                })
                .catch(error => {
                    console.log(error);
                    alert('Ocurrió un error al obtener las reservas.');
                });
        },
        guardarReserva() {
            if (this.reserva.id) {
                // Editar reserva existente
                axios.put(`https://turismomardel2023.pythonanywhere.com/reservas\${this.reserva.id}`, this.reserva)
                    .then(response => {
                        console.log(response.data);
                        this.limpiarFormulario();
                        this.obtenerReservas();
                        alert('Reserva actualizada exitosamente.');
                    })
                    .catch(error => {
                        console.log(error);
                        alert('Ocurrió un error al actualizar la reserva.');
                    });
            } else {
                // Crear nueva reserva
                axios.post('https://turismomardel2023.pythonanywhere.com/reservas', this.reserva)
                    .then(response => {
                        console.log(response.data);
                        this.limpiarFormulario();
                        this.obtenerReservas();
                        alert('Reserva creada exitosamente.');
                    })
                    .catch(error => {
                        console.log(error);
                        alert('Ocurrió un error al crear la reserva.');
                    });
            }
        },
        editarReserva(reserva) {
            this.reserva = { ...reserva };
            this.formTitle = 'Editar Reserva';
            this.buttonLabel = 'Actualizar';
        },
        eliminarReserva(id) {
            if (confirm('¿Está seguro de eliminar esta reserva?')) {
                axios.delete(`https://turismomardel2023.pythonanywhere.com/reservas/${id}`)
                    .then(response => {
                        console.log(response.data);
                        this.obtenerReservas();
                        alert('Reserva eliminada exitosamente.');
                    })
                    .catch(error => {
                        console.log(error);
                        alert('Ocurrió un error al eliminar la reserva.');
                    });
            }
        },
        limpiarFormulario() {
            this.reserva = {};
            this.formTitle = 'Crear nueva Reserva';
            this.buttonLabel = 'Guardar';
        }
    }
});