function updateCount() {
    const text = document.getElementById("text").value;
    document.getElementById("characters").innerText =
        "Characters : " + text.length;
    const words = text.trim() === ""
        ? 0
        : text.trim().split(/\s+/).length;
    document.getElementById("words").innerText =
        "Words : " + words;
}

function copySummary() {
    const summary = document.getElementById("summary").innerText;
    navigator.clipboard.writeText(summary);
    alert("Summary copied!");
}

document.querySelector("form").addEventListener("submit", function () {
    document.getElementById("loading").style.display = "block";
    document.getElementById("submitBtn").disabled = true;
    document.getElementById("submitBtn").innerText = "Generating...";
});

window.onload = updateCount;