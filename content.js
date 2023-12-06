chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action === "fetchData") {
        var courseInfoDiv = document.getElementById('app-course-info');
        if (courseInfoDiv) {
            var courseTitle = courseInfoDiv.querySelector('.app-text-engage').textContent;
            var courseDescription = courseInfoDiv.querySelectorAll('.col-sm-12')[1].textContent.trim();

            // Clean up the course description
            courseDescription = courseDescription.replace(/Credit.*?(\.|\?|!)(?=\s|$)/g, '');
            courseDescription = courseDescription.replace(/Prerequisite.*?(\.|\?|!)(?=\s|$)/g, '');
            courseDescription = courseDescription.replace(/Same.*?(\.|\?|!)(?=\s|$)/g, '');

            // Construct POST request to Flask server
            fetch('http://127.0.0.1:5000/query_course', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    course_title: courseTitle,
                    course_description: courseDescription.trim()
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                // You can further process the data or send it to the popup
                sendResponse({ data: data });
            })
            .catch((error) => {
                console.error('Error:', error);
                sendResponse({ error: error });
            });

            return true; // indicates that the response is sent asynchronously
        }
    }
});
