document.addEventListener('DOMContentLoaded', () => {
    const priceRange = document.getElementById('price_range');
    const priceValue = document.getElementById('price_value');
    const duration = document.getElementById('duration');
    const durationValue = document.getElementById('duration_value');
    const airline = document.getElementById('airline');

    if (priceRange) {
        priceRange.addEventListener('input', () => {
            priceValue.textContent = priceRange.value;
            filterFlights();
        });
    }

    if (duration) {
        duration.addEventListener('input', () => {
            durationValue.textContent = duration.value;
            filterFlights();
        });
    }

    if (airline) {
        airline.addEventListener('change', filterFlights);
    }
});

function filterFlights() {
    const priceRange = document.getElementById('price_range').value;
    const duration = document.getElementById('duration').value;
    const airline = document.getElementById('airline').value;
    const flights = document.querySelectorAll('tbody tr');

    flights.forEach(flight => {
        const flightPrice = parseInt(flight.children[5].textContent);
        const flightDuration = parseInt(flight.children[4].textContent);
        const flightAirline = flight.children[0].textContent;

        const priceMatch = flightPrice <= priceRange;
        const durationMatch = flightDuration <= duration;
        const airlineMatch = airline === '' || flightAirline === airline;

        if (priceMatch && durationMatch && airlineMatch) {
            flight.style.display = '';
        } else {
            flight.style.display = 'none';
        }
    });
}