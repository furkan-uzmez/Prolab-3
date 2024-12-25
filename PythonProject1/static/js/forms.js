// Form Validation Utility Functions
function validateInput(input) {
    const group = input.closest('.input-group');
    const successIcon = group.querySelector('.validation-icon.success');
    const errorIcon = group.querySelector('.validation-icon.error');
    const message = group.querySelector('.validation-message');

    // Remove digit-only restriction
    const trimmedValue = input.value.trim();
    const isNotEmpty = trimmedValue.length > 0;

    input.classList.toggle('valid', isNotEmpty);
    input.classList.toggle('invalid', !isNotEmpty);

    successIcon.style.display = isNotEmpty ? 'inline-block' : 'none';
    errorIcon.style.display = !isNotEmpty ? 'inline-block' : 'none';

    if (!isNotEmpty) {
        message.textContent = 'Bu alan boş bırakılamaz';
    } else {
        message.textContent = '';
    }

    return isNotEmpty;
}

function checkFormValidity(inputs, submitButton) {
    const isValid = Array.from(inputs).every(input =>
        input.value.trim().length > 0
    );

    submitButton.disabled = !isValid;
    submitButton.classList.toggle('active', isValid);
}

function validateForm(form) {
    const inputs = form.querySelectorAll('input[type="text"]');
    return Array.from(inputs).every(input => validateInput(input));
}

// Form Submission Handler
function handleFormSubmit(isterNumber, formData) {
    const data = {
        authorA: formData.get('authorA'),
        authorB: formData.get('authorB') || null,
        isterNumber: isterNumber
    };

    console.log('İster ${isterNumber} submitted:', data);


fetch('/submit_form', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
})
.then(response => {
    if (!response.ok) {
        throw new Error(`Network response was not ok: ${response.statusText}`);
    }
    return response.json();
})
.then(data => {
    console.log('Received data:', data);

    // Validate data structure
    if (!data || typeof data !== 'object') {
        throw new Error('Invalid data received from server');
    }

    // Update output display
    const outputElement = document.getElementById('output');
    if (data.htmlOutput) {
        outputElement.innerHTML = data.htmlOutput;
    } else if (typeof data === 'string') {
        outputElement.innerHTML = data;
    } else {
        outputElement.innerHTML = `
            ${data.result || 'N/A'}<br>
        `;
    }

    // Handle path visualization if valid
    if (data.path && Array.isArray(data.path)) {
        d3.selectAll("circle")
            .filter(d => data.path.includes(d.orcid))
            .transition()
            .attr("fill", "red")
            .attr("r", function() {
                return parseFloat(d3.select(this).attr("r"));
            });
        // Highlight edges
        d3.selectAll("line")
            .filter(d => {
                // Ardışık nodeları kontrol et
                for(let i = 0; i < data.path.length - 1; i++) {
                    let currentNode = data.path[i];
                    let nextNode = data.path[i + 1];

                    // Her iki yönü de kontrol et
                    if ((d.source.orcid === currentNode && d.target.orcid === nextNode) ||
                        (d.source.orcid === nextNode && d.target.orcid === currentNode)) {
                            console.log("Match found!"); // Eşleşme bulunduğunda log
                            console.log(`Matching edge: ${currentNode} -> ${nextNode}`);
                            console.log("Edge source:", d.source.orcid, "Edge target:", d.target.orcid);
                            return true;
                    }
                }
                return false;
            })
            .style("stroke", "red")           // transition yerine direkt style kullan
            .style("stroke-width", "3px");

        }
})
.catch(error => {
    console.error('Error:', error);
    document.getElementById('output').innerHTML = `Error: ${error.message}`;
});
}

// Form Closing Function
function closeForm(form) {
    if (form) {
        form.classList.add('closing');
        setTimeout(() => {
            form.remove();
        }, 300);
    }
}

// Form Generation Function
function showInputForm(container, isterNumber) {
    // Create form HTML
    const formHTML = `
        <form class="input-form">
            ${isterNumber !== 6 ? ` 
            <div class="input-group">
                <h3>${isterNumber}.İSTER için Yazar ID'leri</h3>
                <input type="text" 
                       name="authorA" 
                       placeholder="A Yazarının ID'si" 
                       required>
                <span class="validation-icon success">✓</span>
                <span class="validation-icon error">✗</span>
                <div class="validation-message"></div>
            </div>
            ` : ''}
            ${isterNumber === 1 ? ` 
            <div class="input-group">
                <input type="text" 
                       name="authorB" 
                       placeholder="B Yazarının ID'si" 
                       required>
                <span class="validation-icon success">✓</span>
                <span class="validation-icon error">✗</span>
                <div class="validation-message"></div>
            </div>
            ` : ''}
            <button type="submit" class="submit-button" ${isterNumber === 6 ? 'enabled' : 'disabled'}>Gönder</button>
        </form>
    `;

    // Create form element
    const formWrapper = document.createElement('div');
    formWrapper.innerHTML = formHTML;
    const form = formWrapper.firstElementChild;

    // Insert form after description
    const description = container.querySelector('.ister-description');
    description.insertAdjacentElement('afterend', form);

    // Get inputs and submit button
    const inputs = form.querySelectorAll('input[type="text"]');
    const submitButton = form.querySelector('.submit-button');

    // Input validation listeners
    inputs.forEach(input => {
        input.addEventListener('input', () => {
            const isValid = validateInput(input);
            checkFormValidity(inputs, submitButton);
        });

        // Focus and blur effects
        input.addEventListener('focus', () => {
            input.parentElement.classList.add('focused');
        });

        input.addEventListener('blur', () => {
            input.parentElement.classList.remove('focused');
        });
    });

    // Form submission
    form.addEventListener('submit', (e) => {
        e.preventDefault(); // Sayfanın yenilenmesini engeller
        console.log('Form gönderiliyor...');
        if (validateForm(form)) {
            handleFormSubmit(isterNumber, new FormData(form));
            form.classList.add('success');
            setTimeout(() => {
                closeForm(form);
            }, 1000);
        }
    });

    return form;
}