document.getElementById('moveFiles').addEventListener('click', function() {
    chrome.runtime.sendMessage({action: "moveFiles"});
});