document.addEventListener("DOMContentLoaded", function () {
    const moveFilesBtn = document.getElementById("move-files-btn");
    moveFilesBtn.addEventListener("click", function () {
      chrome.runtime.sendMessage({ action: "moveFiles" });
    });
  });