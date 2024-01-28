// Nastavení pro mobilní menu
function toggleMenu() {
    const navLinks = document.querySelector('.navigation-links');
    const hamburger = document.querySelector('.hamburger-menu');
    navLinks.classList.toggle('open');
    hamburger.classList.toggle('cross');
}

// Nastavení kalendáře, aby se nemohlo v "Do kdy" vybrat datum, které je před "Od kdy"
document.addEventListener('DOMContentLoaded', function () {
    var dateFrom = document.getElementById('date-from');
    var dateTo = document.getElementById('date-to');

    // Funkce pro aktualizaci omezení pro výběr data
    function updateDateConstraints() {
        // Nastavení minimálního data pro datum "Do kdy"
        if (dateFrom.value) {
            dateTo.min = dateFrom.value;
        }

        // Nastavení maximálního data pro datum "Od kdy"
        if (dateTo.value) {
            dateFrom.max = dateTo.value;
        }
    }

    // Event listenery pro změnu dat v kalendáři
    dateFrom.addEventListener('change', updateDateConstraints);
    dateTo.addEventListener('change', updateDateConstraints);
});

// Funkce pro aktualizaci a ukládání vybraných prvků z formuláře
document.addEventListener('DOMContentLoaded', function () {
    var okButton, machineType, dateFrom, dateTo, errorMessage;

    // Funkce pro aktualizaci zobrazených hodnot
    function updateDisplayedValues() {
        document.getElementById('display-machine').textContent = machineType.value || '';
        document.getElementById('display-date-from').textContent = dateFrom.value || '';
        document.getElementById('display-date-to').textContent = dateTo.value || '';
    }

    machineType = document.getElementById('machine-type');
    dateFrom = document.getElementById('date-from');
    dateTo = document.getElementById('date-to');
    errorMessage = document.querySelector('.form-section .error-message');
    okButton = document.querySelector('.form-section button');

    // Event listener pro kliknutí na tlačítko OK ve formuláři
    okButton.addEventListener('click', function(event) {
        event.preventDefault();
        // Kontrola výběru stroje a obou datumů
        var machineSelected = machineType.value === 'Sekačka' || machineType.value === 'Kombajn';
        var datesSelected = dateFrom.value && dateTo.value;

        // Podmínky pro zpracování dat formuláře
        if (machineSelected && datesSelected) {
            // Pokud jsou data správně vyplněna
            if (window.location.pathname.endsWith('/')) {
                var queryParams = new URLSearchParams({
                    machine: machineType.value,
                    dateFrom: dateFrom.value,
                    dateTo: dateTo.value
                }).toString();

                window.location.href = 'nabidka-stroju?' + queryParams;
            }
            // Aktualizace prvků ve formluáři
            else if (window.location.pathname.endsWith('/nabidka-stroju')) {
                updateDisplayedValues();
            }
            errorMessage.style.display = 'none';
        }
        // Pokud data nejsou správně vyplněna, zobrazí se chybová hláška
        else {
            errorMessage.style.display = 'block';
            errorMessage.textContent = 'Vyberte prosím typ stroje a obě data.';
        }
    });

    // Pokud jsme na stránce nabidka-stroju.html a query je nastavené, tak se jeho prvky nastaví jako vybrané hodnoty
    if (window.location.pathname.endsWith('/nabidka-stroju')) {
        var urlParams = new URLSearchParams(window.location.search);
        if (urlParams.has('machine') && urlParams.has('dateFrom') && urlParams.has('dateTo')) {
            machineType.value = urlParams.get('machine');
            dateFrom.value = urlParams.get('dateFrom');
            dateTo.value = urlParams.get('dateTo');
            updateDisplayedValues();
        }
    }
});

// Event listener pro načtení stránky
document.addEventListener("DOMContentLoaded", function(){
    // Event listener pro odeslání formuláře
    document.getElementById("filter-form").addEventListener("submit", function(e){
        e.preventDefault();

        var machineType = document.getElementById("machine-type").value;

        fetch('/nabidka-stroju', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'machine-type=' + encodeURIComponent(machineType)
        })
            .then(response => response.text())
            .then(data => {
                document.querySelector(".stroj-container").innerHTML = data;
            });
    });
});

// Funkce pro zobrazení/skrytí formuláře rezervace
function toggleReserveForm(formId) {
    var x = document.getElementById(formId);
    // Přepínání zobrazení formuláře
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
};

// Funkce pro zobrazení popup okna s pracovníky
function zobrazPracovniciPopup(button, objednavkaId) {
    var popup = document.getElementById('pracovniciPopup');
    var buttonRect = button.getBoundingClientRect();

    // Nastavení pozice popup okna na základě pozice tlačítka
    popup.style.top = (window.scrollY + buttonRect.bottom) + 'px';
    popup.style.left = buttonRect.left + 'px';
    popup.style.display = 'block';

    // Načtení seznamu pracovníků ze serveru
    fetch('/get-pracovnici')
        .then(response => response.json())
        .then(data => {
            // Vybrání elementu pro výpis seznamu pracovníků
            var pracovniciList = popup.querySelector('.pracovnici-list');
            pracovniciList.innerHTML = '';

            // Pro každého pracovníka vytvoření checkboxu a přidání do seznamu
            data.forEach(ucet => {
                pracovniciList.innerHTML += `
                    <div>
                        <input type="checkbox" id="ucet-${ucet.ucet_id}" name="ucet" value="${ucet.ucet_id}">
                        <label for="ucet-${ucet.ucet_id}">${ucet.ucet_jmeno}</label>
                    </div>`;
            });
        })
        .catch(error => {
            console.error('Error fetching pracovnici:', error);
        });

    // Nastavení atributu s ID objednávky pro další zpracování
    popup.querySelector('button').setAttribute('data-objednavka-id', objednavkaId);
}

// Funkce pro potvrzení výběru pracovníka
function potvrditPracovnika() {
    var popup = document.getElementById('pracovniciPopup');
    var objednavkaId = popup.querySelector('button').getAttribute('data-objednavka-id');
    var selectedUcetIds = Array.from(popup.querySelectorAll('input[name="ucet"]:checked'))
        .map(input => input.value);

    // Příprava dat pro odeslání na server
    var requestData = {
        objednavka_id: objednavkaId,
        ucet_ids: selectedUcetIds
    };

    // Odeslání dat na server pro vytvoření rezervace
    fetch('/vytvorit_rezervaci', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
    })
        .then(response => response.json())
        .then(data => {
            // Po úspěšném zpracování serverem, obnovit stránku
            window.location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function closePracovniciPopup() {
    document.getElementById('pracovniciPopup').style.display = 'none';
}