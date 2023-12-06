document.addEventListener('DOMContentLoaded', function() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, {action: "fetchData"}, function(response) {
            if(response) {
                displayCourseInfo(response.data);
            }
        });
    });
});

function displayCourseInfo(data) {
    if(data && data.keywords) {
        const keywordsDiv = document.getElementById('courseKeywords');
        keywordsDiv.innerHTML = '<h2>Keywords:</h2><ul>' + 
            data.keywords.map(keyword => `<li class="keyword">${keyword}</li>`).join('') + '</ul>';
    }

    if(data && data.wikipedia_links) {
        const linksDiv = document.getElementById('wikipediaLinks');
        linksDiv.innerHTML = '<h2>Wikipedia Links:</h2><ul>' +
            data.wikipedia_links.map(link => `<li><a href="${link}" target="_blank">${link}</a></li>`).join('') + '</ul>';
    }
}
