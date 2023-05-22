console.log("handler.js is running")
if (window.opener) {
    window.opener.postMessage("opened", "*")
}
