var map = L.map('map').setView([51.505, -0.09], 13);

L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
attribution: 'Map data &copy; <a href="http://openstreetmap.org">I am JS</a> contributors',
maxZoom: 18
}).addTo(map);

L.marker([51.5, -0.09], {
icon: L.icon({
  iconUrl: 'https://unpkg.com/leaflet@1.0.3/dist/images/marker-icon.png',
  className: 'blinking'
})
}).addTo(map);