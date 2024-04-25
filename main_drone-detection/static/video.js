function loadVideo(event) {
    var videoOutput = document.querySelector("#videoOutput");
    videoOutput.src = URL.createObjectURL(event.target.files[0]);
}

document.querySelector("#videoUploadForm").addEventListener("submit", e => {
    e.preventDefault();
    
    var formData = new FormData();
    var video = document.querySelector('#videoInput').files[0];
    formData.append('video', video);
    
    fetch('/uploadvideo', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log("Response:", data);
        document.querySelector('#response').innerText = data['resText'];
    })
    .catch(error => {
        console.error('Error:', error);
        document.querySelector('#response').innerText = 'Error uploading video';
    });
});
