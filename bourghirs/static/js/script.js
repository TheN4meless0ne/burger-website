function toggleAdmin() {
    const url = isAdmin ? '/remove_admin' : '/make_admin';
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => {
        if (response.ok) {
            isAdmin = !isAdmin;
            document.getElementById('adminButton').innerText = isAdmin ? 'Remove Admin' : 'Make Admin';
            alert(isAdmin ? 'User is now an admin.' : 'User is no longer an admin.');
        } else {
            alert('Failed to change admin status.');
        }
    });
}