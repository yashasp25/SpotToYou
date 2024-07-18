document.getElementById('login-btn').addEventListener('click', () => {
    window.location.href = '/';
});

document.getElementById('logout-btn').addEventListener('click', () => {
    window.location.href = '/logout';
});

document.getElementById('create-playlist-btn').addEventListener('click', () => {
    fetch('/get_all_tracks')
        .then(response => response.text())
        .then(data => {
            document.getElementById('status').innerText = data;
        });
});
