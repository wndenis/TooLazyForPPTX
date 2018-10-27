<script src="//www.WebRTC-Experiment.com/RecordRTC.js"></script>

var session = {
  audio: true,
  video: false
};
var recordRTC = null;
navigator.mediaDevices.getUserMedia(session, function (mediaStream) {
  recordRTC = RecordRTC(MediaStream);
  recordRTC.startRecording();
}, onError);

recordRTC.stopRecording(function(audioURL) {
  var formData = new FormData();
  formData.append('edition[audio]', recordRTC.getBlob())
  $.ajax({
    type: 'POST',
    url: 'some/path',
    data: formData,
    contentType: false,
    cache: false,
    processData: false,
  })
});
