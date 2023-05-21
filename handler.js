console.log("handler.js is up and running")
if (window.opener) {
    window.opener.postMessage("opened", "*")
}
