let speechSynthesis = window.speechSynthesis;
let utterance = null;

chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  switch (request.action) {
    case "play":
      play();
      break;
    case "pause":
      pause();
      break;
    case "stop":
      stop();
      break;
  }
});

function play() {
  if (utterance === null) {
    utterance = new SpeechSynthesisUtterance();
    utterance.text = document.body.innerText;
    utterance.lang = "en-US";
    utterance.rate = 1;
    utterance.pitch = 1;
    utterance.volume = 1;
  }
  speechSynthesis.speak(utterance);
}

function pause() {
  if (speechSynthesis.speaking) {
    speechSynthesis.pause();
  }
}

function stop() {
  if (speechSynthesis.speaking) {
    speechSynthesis.cancel();
  }
}

document.addEventListener("DOMContentLoaded", function () {
  const playButton = document.getElementById("play-button");
  const pauseButton = document.getElementById("pause-button");
  const stopButton = document.getElementById("stop-button");

  playButton.addEventListener("click", function () {
    chrome.runtime.sendMessage({ action: "play" });
  });

  pauseButton.addEventListener("click", function () {
    chrome.runtime.sendMessage({ action: "pause" });
  });

  stopButton.addEventListener("click", function () {
    chrome.runtime.sendMessage({ action: "stop" });
  });
});

