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

    function updateDateConstraints() {
        if (dateFrom.value) {
            dateTo.min = dateFrom.value;
        }

        if (dateTo.value) {
            dateFrom.max = dateTo.value;
        }
    }

    dateFrom.addEventListener('change', updateDateConstraints);
    dateTo.addEventListener('change', updateDateConstraints);
});

// funkce pro aktualizaci a ukladani vybranych prvku z formulare
document.addEventListener('DOMContentLoaded', function () {
    var okButton, machineType, dateFrom, dateTo, errorMessage;

    // funkce pro aktualizaci prvku formulare
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

    // pokud se klikne na OK ve formulari
    okButton.addEventListener('click', function(event) {
        event.preventDefault();
        var machineSelected = machineType.value === 'Sekačka' || machineType.value === 'Kombajn';
        var datesSelected = dateFrom.value && dateTo.value;

        // kontrola zda je vybran typ stroje a oba datumy
        if (machineSelected && datesSelected) {
            // pokud je aktualni stranka index.html vytvori query se zadanymi hodnotami
            if (window.location.pathname.endsWith('/')) {
                var queryParams = new URLSearchParams({
                    machine: machineType.value,
                    dateFrom: dateFrom.value,
                    dateTo: dateTo.value
                }).toString();

                window.location.href = 'nabidka-stroju?' + queryParams;
            }
            // pokud je stranka nabidka-stroju.html aktaulizuji se prvky ve formulari
            else if (window.location.pathname.endsWith('/nabidka-stroju')) {
                updateDisplayedValues();
            }
            errorMessage.style.display = 'none';
        }
        // pokud nektery z prvku formulare neni vybran, zobrazi se chybova hlaska
        else {
            errorMessage.style.display = 'block';
            errorMessage.textContent = 'Vyberte prosím typ stroje a obě data.';
        }
    });

    // pokud jsme na strance nabidka-stroju.html a query je nastavene, tak se jeho prvky nastavi jako vybrane hodnoty
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

document.addEventListener("DOMContentLoaded", function(){
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


function toggleReserveForm(formId) {
    var x = document.getElementById(formId);
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
};

function zobrazPracovniciPopup(button, objednavkaId) {
    var popup = document.getElementById('pracovniciPopup');
    var buttonRect = button.getBoundingClientRect();

    popup.style.top = (window.scrollY + buttonRect.bottom) + 'px';
    popup.style.left = buttonRect.left + 'px';

    popup.style.display = 'block';
    fetch('/get-pracovnici')
        .then(response => response.json())
        .then(data => {
            var pracovniciList = popup.querySelector('.pracovnici-list');
            pracovniciList.innerHTML = '';

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

    popup.querySelector('button').setAttribute('data-objednavka-id', objednavkaId);
}

function potvrditPracovnika() {
    var popup = document.getElementById('pracovniciPopup');
    var objednavkaId = popup.querySelector('button').getAttribute('data-objednavka-id');
    var selectedUcetIds = Array.from(popup.querySelectorAll('input[name="ucet"]:checked'))
        .map(input => input.value);
    var requestData = {
        objednavka_id: objednavkaId,
        ucet_ids: selectedUcetIds
    };

    fetch('/vytvorit_rezervaci', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
    })
        .then(response => response.json())
        .then(data => {
            window.location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function closePracovniciPopup() {
    document.getElementById('pracovniciPopup').style.display = 'none';
}











