const btn = document.getElementById("pobierz");
const wynik = document.getElementById("wynik"); 
const selectMiasto = document.getElementById("wybierz-miasto"); 


window.addEventListener("load", () => {
    fetch('/api/lokalizacje')
        .then(response => response.json())
        .then(data => {
            console.log("Pełne dane:", data);

            data.forEach(miasto => {
                const option = document.createElement("option");
                option.value = miasto.id;
                option.textContent = miasto.city_name;
                selectMiasto.appendChild(option);
            });
        })
        .catch(error => {
            console.error("Błąd ładowania lokalizacji:", error);
            selectMiasto.innerHTML = '<option value="">Błąd ładowania</option>';
        });
});


btn.addEventListener("click", () => {
    const idmiasta = selectMiasto.value;
    
    
    if (!idmiasta) {
        wynik.innerHTML = `<p style="color: red;">Proszę wybrać miasto z listy!</p>`;
        return; 
    }
    
    const url = `/api/pogoda?id=${idmiasta}`;
    console.log("Wysyłam zapytanie dla ID:", idmiasta);
    
    fetch(url)
        .then(response => {
            
            if (!response.ok) {
                throw new Error(`Błąd serwera: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Pełne dane:", data);

            
            if (!data.current_weather) {
                throw new Error("Brak danych pogodowych w odpowiedzi");
            }

            wynik.innerHTML = `
                <ul>
                    <li>Temperatura: <strong>${data.current_weather.temperature}°C</strong></li>
                    <li>Wiatr: <strong>${data.current_weather.windspeed} km/h</strong></li>
                    <li>Kierunek wiatru: <strong>${data.current_weather.winddirection}°</strong></li>
                    <li>Czas pomiaru: <strong>${data.current_weather.time}</strong></li>
                </ul>
            `;
        })
        .catch(error => {
            wynik.innerHTML = `<p style="color: red;">Błąd: ${error.message}</p>`;
            console.error(error);
        });
});