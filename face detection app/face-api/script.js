const video = document.getElementById("video");

Promise.all([
  faceapi.nets.tinyFaceDetector.loadFromUri("./models"),
  faceapi.nets.faceLandmark68Net.loadFromUri("./models"),
]).then(startWebcam);

function startWebcam() {
  navigator.mediaDevices
    .getUserMedia({
      video: true,
      audio: false,
    })
    .then((stream) => {
      video.srcObject = stream;
    })
    .catch((error) => {
      console.error(error);
    });
}


let count = 0
let Break = false

const startBreak = () => {
  Break = true

  setTimeout(() => {
    Break = false
  }, 300000)
}

video.addEventListener("play", () => {
  const canvas = faceapi.createCanvasFromMedia(video);
  document.body.append(canvas);
  faceapi.matchDimensions(canvas, { height: video.height, width: video.width });

  let x = undefined,
    y = undefined


  setInterval(async () => {
    const detections = await faceapi
      .detectAllFaces(video, new faceapi.TinyFaceDetectorOptions())
      .withFaceLandmarks();

    const resizedDetections = faceapi.resizeResults(detections, {
      height: video.height,
      width: video.width,
    });
    canvas.getContext("2d").clearRect(0, 0, canvas.width, canvas.height);
    faceapi.draw.drawDetections(canvas, resizedDetections);
    faceapi.draw.drawFaceLandmarks(canvas, resizedDetections);

/*if (count > 5){

      emailjs
      .send(
        'service_hcx2m2f',
        'template_rmp4vge',
        {
          from_name: "Mayank",
          to_name: "Mayank",
          from_email: "mayanksh518@gmail.com",
          to_email: "mayanksh518@gmail.com",
          message: "students have been distracted a lot of times , Please try to engage...",
        },
        '0xpyMpUb5FebvT9z3'
      )
      
      };*/

    if (x == undefined) {
      x = detections[0].landmarks._shift._x
      y = detections[0].landmarks._shift._y
    } else {
      if (Break == false) {
        try {
          if (Math.abs(x - detections[0].landmarks._shift._x) > 20) {
            alert("You have been distracted")
            count++;
            console.log(count)
          }
        } catch {
          alert("You have been distracted.")
        }
      }
    }

  }, 1000);
});

document.addEventListener("visibilitychange", () => {
  if (document.hidden) {
    if (Break == false) {
      count++
      disableScreen()
    }
  } else {
    document.getElementById("count").innerHTML = count
  }
})

document.getElementById("count").innerHTML = count

function disableScreen() {

  document.getElementById('disable-screen').style.visibility = 'visible';

  window.addEventListener('keydown', disableKeyboard);

  window.addEventListener('mousedown', disableMouse);

  setTimeout(function () {
    document.getElementById('disable-screen').style.visibility = 'hidden';

    window.removeEventListener('keydown', disableKeyboard);

    window.removeEventListener('mousedown', disableMouse);
  }, 10000);
}


function disableKeyboard(event) {
  event.preventDefault();
}


function disableMouse(event) {
  event.preventDefault();
}

