# FreePhish
## Repository for ACM IMC 2023 paper - "Phishing in the Free Waters: A Study of Phishing Attacks Created using Free Website Building Services" <paper-link>

## This README has the following instructions:

### 1) Running the FreePhish web extension on your Chromium browser.
### 2) Running the FreePhish framework on your local machine.

## How to Load the FreePhish Web extension into your Chromium-based Browser.

Note: You need to use a Chromium based browser (eg. Google Chrome, Microsoft Edge, Brave Browser etc.). This extension is not supported on Mozilla Firefox or Safari.

### Step 1: Download or Clone this repository to your local machine.

### Step 2: Open the Browser and Navigate to `chrome://extensions/`

1. Launch your Chromium-based browser.
2. Open a new tab.
3. Type `chrome://extensions/` into the address bar and press `Enter`.

### Step 3: Enable Developer Mode

1. Look for the "Developer mode" toggle switch usually located at the top-right corner of the Extensions page.
2. Turn on "Developer mode" by clicking the toggle switch. This will reveal additional options for loading extensions.

### Step 4: Load the Unpacked Extension

1. Click on the "Load unpacked" button. This will open a file dialog.
2. Navigate to the 'browser_extension' folder of this repo.
3. Select the directory and click "Open" or "OK" depending on your operating system.

FreePhish should now be loaded into the browser, and its icon will typically appear next to the address bar or under the Extensions menu, depending on your browser.

### Step 5: Test the Extension

1. Your browser is now protected by FreePhish! It should protect you from accessing Free Web Builder (FWB) phishing attacks!

For more information about these attacks please check our ACM IMC 2023 paper - <add link>

Here is a preview of FreePhish running on Brave Browser:

![Extension Preview](./extension_preview.gif)

## Framework overview

![Framework](./framework.png)

## Experimental dataset

We share the URL and screenshot of 1,293 websites in the 'Dataset' folder. For these websites have been condifrmed to have been removed by their respective hosting domains.
