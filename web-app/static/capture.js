// capture image from webcam per 10 seconds
const videoElement = document.getElementById("webcamVideo");

const canvas = document.getElementById("captureCanvas");

const context = canvas.getContext("2d");


// 10 seconds
const INTERVAL = 10000;

async function captureImage(){

    if(!videoElement.videoWidth){

        console.log("video not ready");

        return;
    }
    canvas.width = videoElement.videoWidth;

    canvas.height = videoElement.videoHeight;

    context.drawImage(videoElement,0,0);

    const imageData = canvas.toDataURL("image/jpeg", 0.9);

    console.log("captured image");

    try{
        const response = await fetch("/upload-image", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                image: imageData
            })
        });

        const result = await response.json();

        if(!response.ok){
            throw new Error(result.error || "upload failed");
        
        }
        console.log("uploaded image:", result.filename);
    } 
    catch(error){
        console.error("upload failed:", error)
    }
}

setInterval(captureImage, INTERVAL);

