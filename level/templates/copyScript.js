function copyLevelID(levelid) {
    
    var tempInput = document.createElement('input');
    document.body.appendChild(tempInput);
    tempInput.value = levelid;
    tempInput.select();
    document.execCommand('copy');
    document.body.removeChild(tempInput);

    alert('Level ID copied: ' + levelid);
}