document.addEventListener('DOMContentLoaded', () => {
    const mediaItems = document.querySelectorAll('.media-item');
    const display = document.getElementById('media-display');
    let currentIndex = 0;

    if (mediaItems.length === 0) {
        display.innerHTML = '<p style="color: white;">Nenhuma mídia para exibir.</p>';
        return;
    }

    function showMedia(index) {
        const item = mediaItems[index];
        const url = item.dataset.url;
        const type = item.dataset.type;

        console.log(`Exibindo: ${url} (${type})`);

        if (type === 'image') {
            display.innerHTML = `<img src="${url}" alt="Imagem" />`;
        } else if (type === 'video') {
            display.innerHTML = `<video src="${url}" autoplay muted loop playsinline></video>`;
        } else {
            display.innerHTML = `<p style="color: white;">Tipo de mídia desconhecido.</p>`;
        }
    }

    showMedia(currentIndex);

    setInterval(() => {
        currentIndex = (currentIndex + 1) % mediaItems.length;
        showMedia(currentIndex);
    }, 5000);
});
