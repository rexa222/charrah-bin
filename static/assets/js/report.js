document.addEventListener('DOMContentLoaded', (event) => {
    const updateCount = (vehicle, direction) => {
        const counter = document.getElementById(`${vehicle}-${direction}-count`);
        let count = parseInt(counter.innerText);
        counter.innerText = count + 1;
    };

    const buttons = document.querySelectorAll('.count-button');
    buttons.forEach(button => {
        button.addEventListener('click', () => {
            const vehicle = button.dataset.vehicle;
            const direction = button.dataset.direction;
            updateCount(vehicle, direction);
        });
    });
});
