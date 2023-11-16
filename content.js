// content.js
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.action === "fetchData") {
      var courseInfoDiv = document.getElementById('app-course-info');
      if (courseInfoDiv) {
          var courseTitle = courseInfoDiv.querySelector('.app-text-engage').textContent;
          var courseDescription = courseInfoDiv.querySelectorAll('.col-sm-12')[1].textContent.trim();

          // Remove sentences that start with "Credit" or "Prerequisite"
          courseDescription = courseDescription.replace(/Credit.*?(\.|\?|!)(?=\s|$)/g, '');
          courseDescription = courseDescription.replace(/Prerequisite.*?(\.|\?|!)(?=\s|$)/g, '');

          sendResponse({
              courseTitle: courseTitle,
              courseDescription: courseDescription.trim()
          });
      }
  }
});
