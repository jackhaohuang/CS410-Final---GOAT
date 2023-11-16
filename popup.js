// popup.js
document.addEventListener('DOMContentLoaded', function() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, {action: "fetchData"}, function(response) {
            if(response) {
                document.getElementById('courseTitle').textContent = response.courseTitle;
                document.getElementById('courseDescription').textContent = response.courseDescription;
            }
        });
    });
});
