chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    if (request.action === "get-text") {
      const text = document.body.innerText;
      sendResponse({ text: text });
    }
  });