function confirmDelete(event, url) {
    event.preventDefault();
    const popupContainer = document.getElementById('delete-popup');
    const confirmButton = document.getElementById('deleteFeatureButton');
    const closeButton = document.getElementById('closeDeletingPopup');
    popupContainer.style.display = 'block';
    function closeDeleting () {
        popupContainer.style.display = 'none';
    }
    closeButton.addEventListener('click', closeDeleting);

    confirmButton.addEventListener('click', function() {
        window.location.href = url;
    });

}

window.confirmDelete = confirmDelete;