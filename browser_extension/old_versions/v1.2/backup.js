// Store URL check results
const urlCheckResults = {};

// Listener for checking URLs
chrome.webRequest.onCompleted.addListener(
    async function(details) {
        // Check if the request is for the main_frame (i.e., a new URL the user navigated to)
        if (details.type !== "main_frame") {
            return;
        }

        const url = new URL(details.url);  // Create URL object
        const domain = url.hostname;  // Extract the domain name
        const tabId = details.tabId;

        const patterns = [
            ".weebly", ".000webhost", ".blogspot", ".wix", "sites.google",
            ".github.io", "firebase", ".squareup", "forms.zoho", ".wordpress",
            "forms.google", ".sharepoint", ".yolasite", ".godaddysite",
            ".mailchimp", ".glitch.me", ".hpage", "webflow.io", "docs.google", "vercel.app"
        ];

        const urlMatches = patterns.some(pattern => url.href.includes(pattern));

        if (urlMatches) {
            try {
                const response = await fetch("http://45.79.207.137:5000/check_url", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ url: url.href })
                });

                const data = await response.json();

                if (data.result === "phishing") {
                    // Store the result
                    urlCheckResults[domain] = "phishing";

                    // Execute script to replace webpage
                    chrome.tabs.executeScript(tabId, {
                        code: `
                            document.body.innerHTML = \`
                                <h1 style="text-align: center; background-color: #000; color: #fff;">FreePhish Phishing Blocker</h1>
                                <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; background-color: #cc0000; color: white;">
                                    <img src='chrome-extension://${chrome.runtime.id}/warning.svg' alt='Warning Icon'>
                                    <div style="font-weight: bold; font-size: 36px;">WARNING</div>
                                    <div style="font-size: 24px;">
                                        <span style="font-weight: bold; font-style: italic;">FreePhish</span>
                                        <span style="font-weight: bold;"> blocked</span>
                                        a potential phishing website at: ${domain}
                                    </div>
                                    <button id="goBack" style="margin-top: 20px; font-size: 18px;">Close tab and go back to safety</button>
                                </div>
                            \`;

                            document.getElementById("goBack").addEventListener("click", function() {
                                chrome.runtime.sendMessage({ action: "closeTab", tabId: ${tabId} });
                            });
                        `
                    });
                } else {
                    // Store the result as safe if not phishing
                    urlCheckResults[domain] = "safe";
                }

                
            } catch (error) {
                console.log("Error:", error);
            }
        }
    },
    { urls: ["<all_urls>"] }
);

// Listener for handling messages from content scripts or popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'closeTab') {
        chrome.tabs.remove(message.tabId);
    } else if (message.action === 'getCheckResult') {
        sendResponse(urlCheckResults[message.domain]);
    }
});
