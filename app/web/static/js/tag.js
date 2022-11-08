async function pollLastScannedTag(callback) {
    let response = await fetch("/last_scanned_tag");

    if (response.status != 200) {
        console.log('Error fetching last scanned tag: ' + response.statusText);
    } else {
        let tag = await response.text();
        callback(tag);
    }

    // Reconnect in one second
    await new Promise(resolve => setTimeout(resolve, 500));
    await pollLastScannedTag(callback);
}
