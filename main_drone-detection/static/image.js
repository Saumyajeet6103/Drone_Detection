/*
function loadImage(event) {
    var imageOutput = document.querySelector("#imageOutput");
    imageOutput.src = URL.createObjectURL(event.target.files[0]);
}

document.querySelector("#imageUploadForm").addEventListener("submit", e => {

    e.preventDefault();
    
    var formData = new FormData();
    var image = document.querySelector('#imageInput').files[0];
    formData.append('image', image);
    
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log("Response:", data);
        document.querySelector('#response').innerText = data['resText'];
    });
    
});

*/
function loadImage(event) {
    var imageOutput = document.querySelector("#imageOutput");
    imageOutput.src = URL.createObjectURL(event.target.files[0]);
}

document.querySelector("#imageUploadForm").addEventListener("submit", e => {
    e.preventDefault();
    
    var formData = new FormData();
    var image = document.querySelector('#imageInput').files[0];
    formData.append('image', image);
    
    fetch('/upload', {
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
        document.querySelector('#response').innerText = 'Error uploading image';
    });
});
