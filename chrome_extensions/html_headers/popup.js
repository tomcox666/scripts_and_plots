chrome.runtime.sendMessage({ action: "get_clipboard" }, (response) => {
    if (response && response.length > 0) {
      const clipboardList = document.getElementById("clipboard-list");
      response.forEach((text) => {
        const listItem = document.createElement("LI");
        listItem.textContent = text;
        listItem.addEventListener("click", () => {
          chrome.runtime.sendMessage({ action: "copy_text", text });
        });
        clipboardList.appendChild(listItem);
      });
    } else {
      console.log("Clipboard is empty or response is null");
    }
  });