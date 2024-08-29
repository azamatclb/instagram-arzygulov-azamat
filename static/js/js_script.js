async function sendRequest(url, method = 'GET', data = null) {
    const response = await fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: data ? JSON.stringify(data) : null
    });

    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText);
    }

    return await response.json();
}

async function handleLikeClick(event) {
    event.preventDefault();

    const form = event.target.closest('form');
    const url = form.getAttribute('action');
    const method = form.getAttribute('data-method') || 'POST';

    try {
        const result = await sendRequest(url, method, { post_id: form.querySelector('input[name="post_id"]').value });

        const likeIcon = form.querySelector('i');
        const likesCount = form.querySelector('.likes-count');

        if (likeIcon) {
            likeIcon.classList.toggle('bi-heart');
            likeIcon.classList.toggle('bi-heart-fill');
        }

        if (likesCount) {
            likesCount.textContent = `${result.likes_count} Likes`;
        }
    } catch (error) {
        console.error('Ошибка при обработке запроса:', error);
    }
}

function init() {
    document.querySelectorAll('form[data-method]').forEach(form => {
        form.addEventListener('submit', handleLikeClick);
    });
}

document.addEventListener('DOMContentLoaded', init);
