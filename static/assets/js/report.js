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

    // const submitCounts = async () => {
    //     const carLeftCount = document.getElementById('car-left-count').innerText;
    //     const carStraightCount = document.getElementById('car-straight-count').innerText;
    //     const carRightCount = document.getElementById('car-right-count').innerText;
    //     const taxiLeftCount = document.getElementById('taxi-left-count').innerText;
    //     const taxiStraightCount = document.getElementById('taxi-straight-count').innerText;
    //     const taxiRightCount = document.getElementById('taxi-right-count').innerText;
    //
    //     const address = "{{ address }}";
    //     const position = "{{ position }}";
    //     const start_datetime = "{{ start_datetime }}";
    //
    //     const data = {
    //         car: {
    //             left: carLeftCount,
    //             straight: carStraightCount,
    //             right: carRightCount
    //         },
    //         taxi: {
    //             left: taxiLeftCount,
    //             straight: taxiStraightCount,
    //             right: taxiRightCount
    //         },
    //         address: address,
    //         position: position,
    //         start_datetime: start_datetime
    //     };
    //
    //     try {
    //         const response = await fetch('/submit-counts', {
    //             method: 'POST',
    //             headers: {
    //                 'Content-Type': 'application/json'
    //             },
    //             body: JSON.stringify(data)
    //         });
    //
    //         if (response.ok) {
    //             window.location.href = '/submit-counts'; // Redirect to results page
    //         } else {
    //             console.error('Failed to submit counts');
    //         }
    //     } catch (error) {
    //         console.error('Error:', error);
    //     }
    // };
    //
    // document.getElementById('submit-button').addEventListener('click', submitCounts);
});
