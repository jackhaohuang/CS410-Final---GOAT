chrome.runtime.onInstalled.addListener(function() {
    console.log("Extension installed");
    // Perform on install actions, e.g., setting up default values in storage
    chrome.tabs.create({ url: 'http://google.com' });
  });
