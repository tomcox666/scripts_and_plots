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
    utterance.text = "";
    utterance.lang = "en-US";
    utterance.rate = 1;
    utterance.pitch = 1;
    utterance.volume = 1;
  }
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    chrome.tabs.sendMessage(tabs[0].id, { action: "get-text" }, function (response) {
      if (response && response.text) {
        utterance.text = response.text;
        speechSynthesis.speak(utterance);
      } else {
        console.error("Error: No text received from content script.");
      }
    });
  });
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