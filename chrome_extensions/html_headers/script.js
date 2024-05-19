const clipboard = [];

document.addEventListener("copy", (event) => {
  const text = window.getSelection().toString();
  clipboard.push(text);
  if (clipboard.length > MAX_ITEMS) {
    clipboard.shift();
  }
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "get_clipboard") {
    sendResponse(clipboard);
  } else if (request.action === "copy_text") {
    const text = request.text;
    navigator.clipboard.writeText(text);
  }
});