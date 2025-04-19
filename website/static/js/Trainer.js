document.addEventListener("DOMContentLoaded", function () {
    const cards = document.querySelectorAll('.formateur-card');
    cards.forEach(card => {
        card.addEventListener('click', function () {
            const formateurId = this.getAttribute('data-formateur-id');
            location.href = `/formateur/${formateurId}`;
        });
    });

    const modifierButton = document.getElementById('modifier-button');
    if (modifierButton) {
        modifierButton.addEventListener('click', function () {
            const formateurId = this.getAttribute('data-formateur-id');
            window.location.href = `/modifier_formateur/${formateurId}`;
        });
    }

    const formateurId = document.querySelector('.right-column').dataset.formateurId;

    document.getElementById('modifier-button').addEventListener('click', function () {
        window.location.href = `/modifier_formateur/${formateurId}`;
    });

    document.getElementById('supprimer-button').addEventListener('click', function () {
        document.getElementById('delete-modal1').classList.add('show');
    });

    document.getElementById('confirm-delete').addEventListener('click', function () {
        fetch(`/supprimer_formateur/${formateurId}`, { method: 'DELETE' })
          .then(response => {
            if (response.ok) {
              window.location.href = '/'; 
            } else {
              console.error('Error deleting formateur:', response.statusText);
            }
          })
          .catch(error => {
            console.error('Error deleting formateur:', error);
          });
    });

    document.getElementById('cancel-delete').addEventListener('click', function () {
        document.getElementById('delete-modal1').classList.remove('show');
    });
});
