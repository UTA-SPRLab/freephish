document.addEventListener("DOMContentLoaded", function() {
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        const currentTab = tabs[0];
        const url = new URL(currentTab.url);
        const domain = url.hostname;

        chrome.runtime.sendMessage({ action: 'getCheckResult', domain: domain }, function(response) {
            const statusElement = document.getElementById("status");
            const warningElement = document.getElementById("warning");

            if (response === "phishing") {
                statusElement.textContent = "Phishing";
                statusElement.className = "red-text";
                warningElement.textContent = "This website has been detected as dangerous by FreePhish, please do not access this website or share any personal information.";
            }

            else if (response === "suspicious") {
                statusElement.textContent = "Suspicious";
                statusElement.className = "orange-text";
                warningElement.textContent = "This website looks suspicious. Please take caution when entering any information on this website.";
            }
             else if (response === "safe") {
                statusElement.textContent = "Safe";
                statusElement.className = "green-text";
                warningElement.textContent = "";
            } else {
                statusElement.textContent = "Not checked";
                warningElement.textContent = "";
            }
        });
    });
});
