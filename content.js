// content.js
// This script will change the background color of the Google homepage to lightblue

// Check if the current page is Google's homepage
if (window.location.hostname === 'www.google.com' && window.location.pathname === '/') {
    // Change the background color to lightblue
    document.body.style.backgroundColor = 'lightblue';
  
    // Add a custom message to the page
    const messageDiv = document.createElement('div');
    messageDiv.textContent = 'This is a message from your Chrome Extension!';
    messageDiv.style.position = 'fixed';
    messageDiv.style.bottom = '10px';
    messageDiv.style.right = '10px';
    messageDiv.style.padding = '10px';
    messageDiv.style.backgroundColor = '#fff';
    messageDiv.style.border = '1px solid #ddd';
    messageDiv.style.borderRadius = '4px';
    messageDiv.style.boxShadow = '0 2px 4px rgba(0,0,0,0.2)';
    document.body.appendChild(messageDiv);
  }
  
  // Listen for messages from the background script or popup
  chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
      if (request.greeting === "hello") {
        console.log("Hello from the background script!");
        // Perform actions based on the message
        sendResponse({farewell: "goodbye"});
      }
    }
  );
  
  // This is just an example and won't necessarily do anything meaningful
  // unless it's part of a larger extension that you've configured to work with Google's homepage.
  