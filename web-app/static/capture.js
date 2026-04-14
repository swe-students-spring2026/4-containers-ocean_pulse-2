// capture image from webcam per 10 seconds
const video = document.getElementById("webcamVideo");

const canvas = document.getElementById("captureCanvas");

const context = canvas.getContext("2d");


// 10 seconds
const INTERVAL = 10000;

function captureImage(){

    if(!video.videoWidth){

        console.log("video not ready");

        return;
    }
    canvas.width = video.videoWidth;

    canvas.height = video.videoHeight;

    context.drawImage(video,0,0);

    const imageData = canvas.toDataURL("image/jpeg");

    console.log("captured image");
    // next PR will send the image to flask
}

setInterval(captureImage, INTERVAL);

