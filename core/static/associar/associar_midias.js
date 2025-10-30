document.addEventListener("DOMContentLoaded", function() {
    const modal = document.getElementById('modal');
    const confirmBtn = document.getElementById('confirm-selection');
    const tbody = document.getElementById('midias-selecionadas-tbody');

    // Fecha modal clicando fora
    window.onclick = function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    }

    // Confirma seleção
    confirmBtn.addEventListener('click', function() {
        const checkboxes = document.querySelectorAll('#modal input[type="checkbox"]:checked');

        checkboxes.forEach(cb => {
            const id = cb.value;
            const titulo = cb.dataset.titulo;

            if (!document.querySelector(`#midias-selecionadas-tbody input[value="${id}"]`)) {
                const tr = document.createElement('tr');

                // Título
                const tdTitulo = document.createElement('td');
                tdTitulo.textContent = titulo;
                tr.appendChild(tdTitulo);

                // Ordem
                const tdOrdem = document.createElement('td');
                const inputOrdem = document.createElement('input');
                inputOrdem.type = 'number';
                inputOrdem.name = `ordem_midia_${id}`;
                inputOrdem.value = '0';
                inputOrdem.style.width = '60px';
                inputOrdem.style.textAlign = 'center';
                tdOrdem.appendChild(inputOrdem);
                tr.appendChild(tdOrdem);

                // Hidden input
                const hiddenInput = document.createElement('input');
                hiddenInput.type = 'hidden';
                hiddenInput.name = 'midias';
                hiddenInput.value = id;
                tr.appendChild(hiddenInput);

                tbody.appendChild(tr);
            }
        });

        modal.style.display = 'none';
        checkboxes.forEach(cb => cb.checked = false);
    });

    // Limpa a lista de mídias selecionadas após envio do formulário via HTMX
    document.body.addEventListener('htmx:afterRequest', function(evt) {
        // Limpa somente se o formulário enviado for o principal
        const form = document.getElementById('form-principal');
        if (evt.target === form || form.contains(evt.target)) {
            tbody.innerHTML = '';
        }
    });
});
