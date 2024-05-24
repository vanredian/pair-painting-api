document.getElementById('createRoomButton').addEventListener('click', async () => {
    const name = document.getElementById('createName').value;

    if (!name) {
        alert('Please enter your name');
        return;
    }

    const data = { name };

    try {
        const response = await fetch('http://127.0.0.1:8000/create-room', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            console.error("Failed to create/join room:", await response.text());
            return;
        }

        const result = await response.json();
        console.log(result);

        // Display the room info and UID
        document.getElementById('roomUID').textContent = result.uid;
        document.getElementById('roomInfo').style.display = 'block';
    } catch (error) {
        console.error('Error:', error);
    }
});

document.getElementById('showJoinRoomFormButton').addEventListener('click', () => {
    document.getElementById('joinRoomForm').style.display = 'block';
});

document.getElementById('joinRoomButton').addEventListener('click', async () => {
    const uid = document.getElementById('uid').value;
    const name = document.getElementById('joinName').value;

    if (!uid || !name) {
        alert('Please enter your name and UID');
        return;
    }

    const data = { uid, name };

    try {
        const response = await fetch('http://127.0.0.1:8000/join-room', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            if (response.status === 404) {
                document.getElementById('errorMessage').style.display = 'block';
            } else {
                console.error("Failed to join room:", await response.text());
            }
            return;
        }

        const result = await response.json();
        console.log(result);

        // Hide the error message if successful
        document.getElementById('errorMessage').style.display = 'none';
    } catch (error) {
        console.error('Error:', error);
    }
});
