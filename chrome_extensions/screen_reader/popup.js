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