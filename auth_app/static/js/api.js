async function registerUser(data) {
    const csrftoken = getCookie('csrftoken'); // Get CSRF token from cookies

    const response = await fetch('/auth/api_register/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken  // Pass CSRF token in headers
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    return result;
}

// Helper function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
