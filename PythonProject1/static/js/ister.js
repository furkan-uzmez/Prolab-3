document.addEventListener('DOMContentLoaded', () => {
    const isterContainer = document.querySelector('.ister-buttons');
    let activeIster = null;
    let activeForm = null;

    // Create İSTER buttons and descriptions
    for (let i = 1; i <= 7; i++) {
        const container = document.createElement('div');
        container.className = 'ister-container';
        container.id = `ister-container-${i}`;

        const button = document.createElement('button');
        button.className = 'ister-button';
        button.textContent = `${i}.İSTER`;
        button.dataset.ister = i;

        const description = document.createElement('div');
        description.className = 'ister-description';
        description.textContent = ISTER_DESCRIPTIONS[i];
        description.id = `description-${i}`;

        container.appendChild(button);
        container.appendChild(description);
        isterContainer.appendChild(container);

        // Add hover event listeners for description
        button.addEventListener('mouseenter', () => {
            description.classList.add('show');
        });

        button.addEventListener('mouseleave', () => {
            if (activeIster !== i) {
                description.classList.remove('show');
            }
        });
    }

    // Handle İSTER button clicks
    isterContainer.addEventListener('click', (e) => {
        const button = e.target.closest('.ister-button');
        if (!button) return;

        const isterNumber = parseInt(button.dataset.ister);
        const container = document.getElementById(`ister-container-${isterNumber}`);
        const description = document.getElementById(`description-${isterNumber}`);

        // If clicking the same button, close the form
        if (activeIster === isterNumber) {
            if (activeForm) {
                closeForm(activeForm);
                activeForm = null;
            }
            activeIster = null;
            description.classList.remove('show');
            return;
        }

        // Close previous form if exists
        if (activeForm) {
            closeForm(activeForm);
        }

        // Show description and create new form
        description.classList.add('show');
        activeIster = isterNumber;
        activeForm = showInputForm(container, isterNumber);
    });
});