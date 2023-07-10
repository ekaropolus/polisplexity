const chunks = [];
let mediaRecorder;
let mediaStream;

const startRecord = async () => {
  const mimeType = 'audio/webm; codecs=opus';

  if (!MediaRecorder.isTypeSupported(mimeType)) {
    alert('Opus mime type is not supported');
    return;
  }

  const options = {
    audioBitsPerSecond: 128000,
    mimeType
  };

  try {
    mediaStream = await getLocalMediaStream();
  } catch (error) {
    console.log(`Error accessing microphone: ${error}`);
    return;
  }

  mediaRecorder = new MediaRecorder(mediaStream, options);

  setListeners();

  mediaRecorder.start();
  console.log('Recording started');
};

const stopRecord = async () => {
  if (!mediaRecorder) return;

  mediaRecorder.stop();
  console.log('Recording stopped');

  if (mediaStream) {
    mediaStream.getTracks().forEach(track => track.stop());
  }
};

const getLocalMediaStream = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    return stream;
  } catch (error) {
    console.log(`Error accessing microphone: ${error}`);
    throw error;
  }
};

const setListeners = () => {
  mediaRecorder.ondataavailable = handleOnDataAvailable;
  mediaRecorder.onstop = handleOnStop;
};

const handleOnStop = () => {
  saveFile();

  destroyListeners();
  mediaRecorder = undefined;
};

const destroyListeners = () => {
  mediaRecorder.ondataavailable = undefined;
  mediaRecorder.onstop = undefined;
};

const handleOnDataAvailable = ({ data }) => {
  if (data.size > 0) {
    chunks.push(data);
  }
};

const saveFile = async () => {
  const blob = new Blob(chunks, { type: 'audio/wav' });

  const formData = new FormData();
  formData.append('audio', blob, 'recorded_file.wav');

  try {
    const response = await fetch('/ai_services/gtp_avatar_service/gtp_avatar/process_answer/', {
      method: 'POST',
      body: formData
    });
    console.log('Audio data sent:', response);
  } catch (error) {
    console.log('Error sending audio data:', error);
  }

//   window.URL.revokeObjectURL(blobUrl);
  chunks.length = 0;
};
