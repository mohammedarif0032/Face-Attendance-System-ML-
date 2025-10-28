// For index.html (Attendance)
if (document.getElementById('video')) {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    const captureBtn = document.getElementById('captureBtn');
    const status = document.getElementById('status');

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => video.srcObject = stream)
        .catch(err => status.textContent = 'Error accessing webcam: ' + err);

    captureBtn.addEventListener('click', () => {
        ctx.drawImage(video, 0, 0, 320, 240);
        const imageData = canvas.toDataURL('image/jpeg');
        
        fetch('/api/mark_attendance', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image: imageData })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                status.textContent = `Attendance marked for ${data.name}!`;
                status.style.color = 'green';
            } else {
                status.textContent = data.error || 'Failed to mark attendance';
                status.style.color = 'red';
            }
        })
        .catch(err => {
            status.textContent = 'Error: ' + err;
            status.style.color = 'red';
        });
    });
}

// For register.html
if (document.getElementById('registerBtn')) {
    const registerBtn = document.getElementById('registerBtn');
    const imageInput = document.getElementById('imageInput');
    const nameInput = document.getElementById('nameInput');
    const regStatus = document.getElementById('regStatus');

    registerBtn.addEventListener('click', () => {
        const file = imageInput.files[0];
        if (!file || !nameInput.value) {
            regStatus.textContent = 'Please select image and enter name';
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            const imageData = e.target.result;
            fetch('/api/register_user', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: nameInput.value, image: imageData })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    regStatus.textContent = `User ${data.user_id} registered!`;
                    regStatus.style.color = 'green';
                } else {
                    regStatus.textContent = data.error || 'Registration failed';
                    regStatus.style.color = 'red';
                }
            });
        };
        reader.readAsDataURL(file);
    });
}