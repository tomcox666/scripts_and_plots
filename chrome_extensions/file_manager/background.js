chrome.downloads.onChanged.addListener(function(downloadDelta) {
    if (downloadDelta.state === "complete" && downloadDelta.filename.includes("temp")) {
      var tempFolder = "temp";
      var filesFolder = "Files";
      var downloadId = downloadDelta.id;
      var filename = downloadDelta.filename;
  
      chrome.downloads.search({ id: downloadId }, function(download) {
        var fileUrl = download[0].url;
        var filePath = fileUrl.replace("file:///", "");
  
        // Create the temp folder if it doesn't exist
        chrome.fileSystem.getWritableEntry(filePath, function(entry) {
          entry.getDirectory(tempFolder, { create: true }, function(tempDir) {
            // Move the file to the temp folder
            entry.getFile(filename, { create: false }, function(file) {
              tempDir.moveTo(file, filename, function() {
                // Move the file to the Files folder
                entry.getDirectory(filesFolder, { create: true }, function(filesDir) {
                  filesDir.moveTo(file, filename, function() {
                    console.log("File moved to Files folder");
                  });
                });
              });
            });
          });
        });
      });
    }
  });
  
  chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    if (request.action === "moveFiles") {
      var tempFolder = "temp";
      var filesFolder = "Files";
  
      chrome.fileSystem.getWritableEntry("/", function(entry) {
        entry.getDirectory(tempFolder, { create: true }, function(tempDir) {
          entry.getDirectory(filesFolder, { create: true }, function(filesDir) {
            tempDir.getEntries(function(entries) {
              entries.forEach(function(entry) {
                tempDir.moveTo(entry, entry.name, function() {
                  console.log("File moved to Files folder");
                });
              });
            });
          });
        });
      });
    }
  });