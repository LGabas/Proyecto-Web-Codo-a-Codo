new Vue({
    el: '#appclima',
    data() {
      return {
        loading: true,
        temperature: null,
        description: null,
        iconLink: null,
        apiKey: 'aef6a177b652a823651cb4bffc06e0cf',
        city: 'Mar del Plata'
      };
    },
    mounted() {
      this.fetchWeather();
    },
    methods: {
      fetchWeather() {
        const apiUrl = `https://api.openweathermap.org/data/2.5/weather?q=${this.city}&lang=sp&appid=${this.apiKey}`;

        axios.get(apiUrl)
          .then(response => {
            this.loading = false;
            this.temperature = Math.round(response.data.main.temp - 273.15);
            this.description = response.data.weather[0].description;
            this.iconLink = `https://openweathermap.org/img/wn/${response.data.weather[0].icon}.png`;
          })
          .catch(error => {
            console.error(error);
            this.loading = false;
          });
      }
    }
  });