// API Key from OpenWeatherMap
let apiUrl = 'http://api.openweathermap.org/data/2.5/';
let apiKey = '40c60293d9deac2ecec6b9d7cfdcf6a1';

let cityElement = document.getElementById('city');
let weatherElement = document.getElementById('weather');
let searchInput = document.getElementById('search');
let searchBtn = document.getElementById('search-btn');
let searchOptions = document.getElementById('search-options');

// Get the user's location
navigator.geolocation.getCurrentPosition(position => {
  let lat = position.coords.latitude;
  let lon = position.coords.longitude;
  getWeather(lat, lon);
});

// Search for a new location
searchInput.addEventListener('input', () => {
  let cityName = searchInput.value;
  if (cityName.length > 2) {
    searchCities(cityName);
  }
});

function searchCities(cityName) {
  let url = `${apiUrl}find?q=${cityName}&type=like&sort=population&cnt=10&appid=${apiKey}`;
  fetch(url)
    .then(response => response.json())
    .then(data => {
      let cities = data.list;
      searchOptions.innerHTML = '';
      cities.forEach(city => {
        let option = document.createElement('option');
        option.value = city.id;
        option.text = `${city.name}, ${city.sys.country}`;
        searchOptions.appendChild(option);
      });
    })
    .catch(error => console.error(error));
}

searchBtn.addEventListener('click', () => {
  let selectedCityId = searchOptions.value;
  if (selectedCityId) {
    getWeather(null, null, selectedCityId);
  }
});

function getWeather(lat, lon, cityId) {
  let params = {};
  if (lat && lon) {
    params.lat = lat;
    params.lon = lon;
  } else if (cityId) {
    params.id = cityId;
  }

  let url = `${apiUrl}weather?appid=${apiKey}&units=metric`;
  for (let key in params) {
    url += `&${key}=${params[key]}`;
  }

  fetch(url)
    .then(response => response.json())
    .then(data => {
      cityElement.innerText = data.name;
      let temperature = Math.round(data.main.temp * 10) / 10;
      weatherElement.innerText = `${data.weather[0].main} (${temperature.toString().replace('\u00B0', '')}°C)`;

      // Get the animated weather icon
      let iconCode = data.weather[0].icon;
      let iconUrl = `http://openweathermap.org/img/w/${iconCode}.gif`;
      let img = document.createElement('img');
      img.src = iconUrl;
      document.body.appendChild(img);
    })
    .catch(error => console.error(error));
}