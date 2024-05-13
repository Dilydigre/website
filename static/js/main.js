function download() {
    const imageData = document.getElementById("generated-img").src;
    const downloadLink = document.createElement("a");
    downloadLink.href = imageData;
    downloadLink.download = "generatedImage" + Date.now() + ".png";
    downloadLink.class = "hidden";
    downloadLink.click();
};

function updateModelText() {
    const modelSelector = document.getElementById("model-label");   
    if (modelSelector.innerHTML === "Modèle v.2") {
        modelSelector.innerHTML = "Modèle v.1";
    } else {
        modelSelector.innerHTML = "Modèle v.2";
    }
};