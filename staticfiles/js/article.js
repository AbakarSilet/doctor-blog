// Récupérer le token CSRF depuis la balise meta
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

document.addEventListener('DOMContentLoaded', function () {
    // Gestion du like d'article
    const likeButton = document.getElementById('likeButton');
    if (likeButton) {
        likeButton.addEventListener('click', function () {
            if (this.hasAttribute('disabled')) return;

            const slug = this.dataset.articleSlug;
            const heartIcon = this.querySelector('i');

            fetch(`/article/${slug}/like/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
            })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('likeCount').textContent = data.total_likes;

                    if (data.liked) {
                        this.classList.add('liked');
                        heartIcon.classList.replace('far', 'fas');
                    } else {
                        this.classList.remove('liked');
                        heartIcon.classList.replace('fas', 'far');
                    }
                })
                .catch(error => console.error('Erreur:', error));
        });
    }

    // Gestion du like de commentaire
    document.querySelectorAll('.like-icon').forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            const commentId = this.dataset.commentId;

            fetch(`/like_commentaire/${commentId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
                credentials: 'same-origin',
            })
                .then(response => response.json())
                .then(data => {
                    const icon = this.querySelector('i');
                    const likeCount = this.querySelector('.like-count');

                    if (data.liked) {
                        this.classList.add('liked');
                        icon.classList.replace('far', 'fas');
                    } else {
                        this.classList.remove('liked');
                        icon.classList.replace('fas', 'far');
                    }

                    likeCount.textContent = data.total_likes;
                })
                .catch(error => console.error('Erreur:', error));
        });
    });
});