function confirmDelete(event, url, type) {
    event.preventDefault();
    const popupContainer = document.getElementById('delete-popup');
    const confirmButton = document.getElementById('deleteFeatureButton');
    const closeButton = document.getElementById('closeDeletingPopup');
    const header = document.getElementById('delete-popup-title');
    
    header.textContent = `${type} törlése`
    popupContainer.style.display = 'flex';
    function closeDeleting () {
        popupContainer.style.display = 'none';
    }
    closeButton.addEventListener('click', closeDeleting);

    confirmButton.addEventListener('click', function() {
        window.location.href = url;
    });

}

window.confirmDelete = confirmDelete;