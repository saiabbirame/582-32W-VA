// NAVIGATION
const navToggle = document.querySelector('.nav-toggle');
const navMenu = document.querySelector('.nav-menu');

navToggle.addEventListener('click', () => {
    navMenu.classList.toggle('open');
});

// MAP
const mapContainer = document.querySelector('#map');

if (mapContainer) {
    const latitude = mapContainer.dataset.latitude;
    const longitude = mapContainer.dataset.longitude;

    const map = L.map('map').setView([latitude, longitude], 15);

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    const marker = L.marker([latitude, longitude]).addTo(map);
}

// SEARCH
const placeSearch = document.querySelector('#place-search');
const placeCards = document.querySelectorAll('.place-card');

if (placeSearch && placeCards.length > 0) {
    placeSearch.addEventListener("input", () => {
        const searchTerm = placeSearch.value
            .trim()
            .toLowerCase();

        placeCards.forEach((card) => {
            const placeName = card
                .querySelector("h3")
                .textContent
                .toLowerCase();

            if (placeName.includes(searchTerm)) {
                card.style.display = "";
            } else {
                card.style.display = "none";
            }
        });
    });
}