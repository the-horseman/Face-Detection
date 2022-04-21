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
    startbutton = document.getElementById('startbutton');
    navigator.mediaDevices.getUserMedia({ video: true, audio: false })
    .then(function (stream) {
        document.getElementById("stp-video").style.display = "none";
        document.getElementById('choice').style.display = "none";
        document.getElementById("stp-camera").style.display = "block";
        document.getElementById('camera-struct').style.display = "flex";
            video.srcObject = stream;
            $('html, body').animate({
                'scrollTop': $("#camera-struct").position().top
            }, 1000);
            video.play();
        })
        .catch(function (err) {
            console.log("An error occurred: " + err);
        });
    ShowOnCanvas(video);
}

function ShowOnCanvas(video) {
    video.addEventListener('canplay', function (ev) {
        if (!streaming) {
            height = video.videoHeight/2;
            width = video.videoWidth/2;
            // height = 130;
            // width = 200;
            canvas.setAttribute('width', width);
            canvas.setAttribute('height', height);
            streaming = true;
            if (streaming == true)
                TakePicture();
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
        let extra = {"image" : data};
        fetch("/process", {
            method:"POST",
            body:JSON.stringify(extra)
        }).then((rsult) => {
            return rsult.json(); 
        }).then((res) => {
            let img = res["img"];
            let nme = res["name"]
            document.getElementById("rec-face").innerHTML = "<p class='face-name'>" + nme + "</p>";
            photo.setAttribute('src', "data:image/png;base64," + img);
            if (streaming == true) {
                TakePicture()
            }
            else {
                document.getElementById("rec-face").innerHTML = "";
            }
        });
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

    tracks.forEach(function (track) {
        track.stop();
    });
    streaming = false;
    videoElem.srcObject = null;
}

function VideoStart() {
    document.getElementById("inp").click();
    document.getElementById("inp").addEventListener("change", function () {
        document.getElementById("choice").style.display = "none";
        document.getElementById("stp-video").style.display = "block";
        document.getElementById("stp-camera").style.display = "none";
        var media = URL.createObjectURL(this.files[0]);
        video = document.getElementById('video');
        canvas = document.getElementById('canvas');
        photo = document.getElementById('photo');
        console.log(media);
        video.src = media;
        document.getElementById("camera-struct").style.display = "flex";
        $('html, body').animate({
            'scrollTop': $("#camera-struct").position().top
        }, 1000);
        video.play();
        ShowOnCanvas(video);
    });
}

function StopVideo() {
    document.getElementById("choice").style.display = "flex";
    document.getElementById("camera-struct").style.display = "none";
    video.src = null;
    streaming = false;
    document.getElementById("vid-res").click();
}

function ImidStrt() {
    $('html, body').animate({
        'scrollTop': $("#detection").position().top
    }, 1000);
}

function cnt_me() {
    let nme = document.getElementById("fnme").value;
    let mal = document.getElementById("yrmail").value;
    let mess = document.getElementById("message").value;

    Email.send({
        Host: "smtp.gmail.com",
        Username: "contactmemail2002@gmail.com",
        Password: "contactme123",
        To: 'aryanrishi20@gmail.com',
        From: "contactmemail2002@gmail.com",
        Subject: "Contact Me Form",
        Body: "Name => " + nme + "   Email => " + mal + "   Message => " + mess,
    }).then(
        message => alert(message)
    );
}