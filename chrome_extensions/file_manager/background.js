chrome.downloads.onDeterminingFilename.addListener(function(item, suggest) {
    suggest({filename: `temp/${item.filename}`});
});

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action === "moveFiles") {
        chrome.downloads.search({}, function(results) {
            results.forEach(function(item) {
                if (item.filename.includes('temp/')) {
                    const newFilename = item.filename.replace('temp/', 'Files/');
                    chrome.downloads.move(item.id, {filename: newFilename});
                }
            });
        });
    }
});