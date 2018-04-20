
const video = document.querySelector('#video');
const canvas = document.querySelector('#draw');
const ctx = canvas.getContext('2d');

const file = document.querySelector('#file');
const p = document.querySelector('#p');
const img = document.querySelector('#img');
const table = document.querySelector('#table');

let locations = [];
let names = [];
ctx.font = '10px Comic Sans MS';

// use canvas to show the frame every 200ms in order to draw a video in the front-end
function drawVideo(){
    ctx.drawImage(video, 0, 0, 500, 400);
    // use the received face_locations to draw rectangulars for painting the edges of the detected faces
    if (locations.length > 0){
        for (var i = 0; i < locations.length; i++){
            l0 = locations[i][0];
            l1 = locations[i][1];
            l2 = locations[i][2];
            l3 = locations[i][3];
            ctx.strokeRect(l3, l0, l1-l3, l2-l0);
        } 
    }
}

// send frames to the server, and wait for its responses
async function fetchData() {
    frame = canvas.toDataURL("image/png"); //format: base64
    let resp = await fetch("/stream", {
        method: "PUT",
        body: frame
    });
    let json = await resp.json();
    locations = json.locations;
    names = json.names;
    textChange()
}

// get video data from webcams
if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
 navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
 video.src = window.URL.createObjectURL(stream);
 video.play();
 });
}

// show the received face_names below the canvas
function textChange() {
    p.innerHTML = ""
    for (let i=0; i<names.length; i++){
        p.innerHTML += "   "
        p.innerHTML += names[i];
    }
}

// invoke drawVideo and fecthData every 200ms and 1000ms repectively
const timeInterval1 = setInterval(drawVideo, 200);
const timeInterval2 = setInterval(fetchData, 1000);

// for creating the form to upload image
function readURL(input) {
    if (input.files && input.files[0]) {
  
      var reader = new FileReader();
  
      reader.onload = function(e) {
        $('.image-upload-wrap').hide();
   
        $('.file-upload-image').attr('src', e.target.result);
        $('.file-upload-content').show();
  
        $('.image-title').html(input.files[0].name);
      };
  
      reader.readAsDataURL(input.files[0]);
  
    } else {
      removeUpload();
    }
}
  
function removeUpload() {
    $('.file-upload-input').replaceWith($('.file-upload-input').clone());
    $('.file-upload-content').hide();
    $('.image-upload-wrap').show();
}

