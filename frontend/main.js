function uploadFile() {
    let fileInput = document.getElementById("fileUpload");
    let formData = new FormData();
    formData.append("file", fileInput.files[0]);

    fetch("/upload", { method: "POST", body: formData })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error("Error:", error));
}

function sendEmail() {
    let recipient = document.getElementById("recipient").value;
    let body = document.getElementById("emailBody").value;

    fetch("/send_email", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ recipient, subject: "Automated Email", body })
    })
    .then(response => response.json())
    .then(data => alert(data.success || data.error));
}
