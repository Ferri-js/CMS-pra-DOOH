document.addEventListener("DOMContentLoaded", function() {
    const modal = document.getElementById('modal');
    const confirmBtn = document.getElementById('confirm-selection');
    const tbody = document.getElementById('playlists-selecionadas-tbody');

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

            if (!document.querySelector(`#playlists-selecionadas-tbody input[value="${id}"]`)) {
                const tr = document.createElement('tr');

                // Título
                const tdTitulo = document.createElement('td');
                tdTitulo.textContent = titulo;
                tr.appendChild(tdTitulo);

                // Ordem
                const tdOrdem = document.createElement('td');
                const inputOrdem = document.createElement('input');
                inputOrdem.type = 'number';
                inputOrdem.name = `ordem_playlist_${id}`;
                inputOrdem.value = '0';
                inputOrdem.style.width = '60px';
                inputOrdem.style.textAlign = 'center';
                tdOrdem.appendChild(inputOrdem);
                tr.appendChild(tdOrdem);

                // Hidden input
                const hiddenInput = document.createElement('input');
                hiddenInput.type = 'hidden';
                hiddenInput.name = 'playlists';
                hiddenInput.value = id;
                tr.appendChild(hiddenInput);

                tbody.appendChild(tr);
            }
        });

        modal.style.display = 'none';
        checkboxes.forEach(cb => cb.checked = false);
    });

    // Limpa a lista de mídias selecionadas após envio do formulário via HTMX
    document.body.addEventListener('htmx:afterSwap', function(evt) {
        if (evt.target.id === 'lista-playlists') {
            // Atualização concluída com sucesso, limpa a lista temporária
            document.getElementById('playlists-selecionadas-tbody').innerHTML = '';
        }
    });
});
