var width = 0;
var height = 0;

var streaming = false;

var video = null;
var canvas = null;
var photo = null;
var startbutton = null;

function CameraStart() {
    video = document.getElementById('video');
    canvas = document.getElementById('canvas');
    photo = document.getElementById('photo');
    document.getElementById('camera-struct').style.display = "flex";
    document.getElementById('choice').style.display = "none";
    startbutton = document.getElementById('startbutton');
    navigator.mediaDevices.getUserMedia({ video: true, audio: false })
        .then(function (stream) {
            video.srcObject = stream;
            video.play();
        })
        .catch(function (err) {
            console.log("An error occurred: " + err);
        });

    video.addEventListener('canplay', function (ev) {
        if (!streaming) {
            height = video.videoHeight;
            width = video.videoWidth;
            canvas.setAttribute('width', width);
            canvas.setAttribute('height', height);
            streaming = true;
            setInterval(function () {
                TakePicture();
            }, 10);
        }
    }, false);
}
function TakePicture() {
    var context = canvas.getContext('2d');
    if (width && height) {
        canvas.width = width;
        canvas.height = height;
        context.drawImage(video, 0, 0, width, height);

        var data = canvas.toDataURL('image/png');
        photo.setAttribute('src', data);
    }
}

function StopCamera() {
    document.getElementById("camera-struct").style.display = "none";
    document.getElementById("choice").style.display = "flex";
    stopStreamedVideo(video);
}

function stopStreamedVideo(videoElem) {
    const stream = videoElem.srcObject;
    const tracks = stream.getTracks();
  
    tracks.forEach(function(track) {
      track.stop();
    });
  
    videoElem.srcObject = null;
  }
  