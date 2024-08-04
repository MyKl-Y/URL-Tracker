const dotenv = require('dotenv');
/*
function categorizeUrl(url) {
    for (let category in categories) {
        if (categories[category].some(keyword => url.lower().includes(keyword))) {
            return category;
        }
    }
    return "other";
}
*/

let activeTabs = {}; // Store active tab info for each window

function sendToServer(data) {
    fetch(process.env.URL || '', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => console.log('Success:', data))
    .catch((error) => console.error('Error:', error));
}

function updateActiveTab(windowId, tabId, url) {
    if (activeTabs[windowId] && activeTabs[windowId].tabId !== null && activeTabs[windowId].startTime !== null) {
        const duration = new Date().getTime() - activeTabs[windowId].startTime;
        //const category = categorizeUrl(activeTabs[windowId].url);
        sendToServer({ 
            event: 'tab-inactive', 
            windowId: windowId,
            tabId: activeTabs[windowId].tabId, 
            url: activeTabs[windowId].url,
            //category: category,
            duration: duration, 
            timestamp: new Date().toISOString() 
        });
    }

    activeTabs[windowId] = {
        tabId: tabId,
        startTime: new Date().getTime(),
        url: url
    };

    //const category = categorizeUrl(url);
    sendToServer({ 
        event: 'tab-active', 
        windowId: windowId,
        tabId: tabId, 
        url: url,
        //category: category,
        timestamp: new Date().toISOString() 
    });
}

browser.tabs.onActivated.addListener(activeInfo => {
    browser.tabs.get(activeInfo.tabId, (tab) => {
        updateActiveTab(tab.windowId, activeInfo.tabId, tab.url);
    });
});

browser.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.url) {
        updateActiveTab(tab.windowId, tabId, changeInfo.url);
    }
});

browser.tabs.onRemoved.addListener((tabId, removeInfo) => {
    const windowId = removeInfo.windowId;
    if (activeTabs[windowId] && activeTabs[windowId].tabId === tabId) {
        const duration = new Date().getTime() - activeTabs[windowId].startTime;
        //const category = categorizeUrl(activeTabs[windowId].url);
        sendToServer({ 
            event: 'tab-closed', 
            windowId: windowId,
            tabId: tabId, 
            url: activeTabs[windowId].url,
            //category: category,
            duration: duration, 
            timestamp: new Date().toISOString() 
        });
        delete activeTabs[windowId];
    }
});

browser.windows.onFocusChanged.addListener(windowId => {
    if (windowId !== browser.windows.WINDOW_ID_NONE) {
        browser.windows.get(windowId, { populate: true }, (window) => {
            const activeTab = window.tabs.find(tab => tab.active);
            if (activeTab) {
                updateActiveTab(windowId, activeTab.id, activeTab.url);
            }
        });
    }
});
