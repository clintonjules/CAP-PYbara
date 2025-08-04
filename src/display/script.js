function uploadImage() {
    let fileInput = document.getElementById('fileInput');
    let file = fileInput.files[0];
    let formData = new FormData();

    formData.append('file', file);

    let uploadedImage = document.getElementById('uploadedImage');
    uploadedImage.src = URL.createObjectURL(file);
    uploadedImage.style.display = 'block';

    fetch('http://127.0.0.1:5000/uploads', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            let resultText = '';
            let resultImage = document.getElementById('resultImage');;

            if (data.prediction && data.probability !== undefined) {
                resultText = 'Prediction: ' + data.prediction + '\nProbability: ' + data.probability;

                if (data.prediction == "CAP") {
                    resultImage.src = "cap_images/billed-cap.png";
                }
                
                else {
                    resultImage.src = "cap_images/no_cap.jpeg";
                }
                
                resultImage.style.display = 'block';
            }
            else {
                resultText = "File type not valid"
            }

            document.getElementById('result').innerText = resultText;
        })
        .catch(error => console.error('Error:', error));
}