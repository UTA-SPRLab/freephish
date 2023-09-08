document.addEventListener("DOMContentLoaded", function() {
    // Get the current tab to know which site we're on
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        const currentTab = tabs[0];
        const url = new URL(currentTab.url);
        const domain = url.hostname;

        // Send message to background.js to get the phishing check result for the current domain
        chrome.runtime.sendMessage({ action: 'getCheckResult', domain: domain }, function(response) {
            const statusElement = document.getElementById("status");

            if (response === "phishing") {
                statusElement.textContent = "Suspicious";
                statusElement.className = "red-text";
            } else if (response === "safe") {
                statusElement.textContent = "benign";
                statusElement.className = "";
            } else {
                statusElement.textContent = "Unknown/Safe";
                statusElement.className = "green-text";
            }
        });
    });
});
