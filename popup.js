// popup.js
document.addEventListener('DOMContentLoaded', function() {
    var changeColorButton = document.getElementById('changeColor');
    // onClick's logic below:
    changeColorButton.addEventListener('click', function() {
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            // Send a message to the active tab
            chrome.tabs.sendMessage(tabs[0].id, {color: "blue"}, function(response) {
                console.log('Color changed to blue');
            });
        });
    }, false);
}, false);
