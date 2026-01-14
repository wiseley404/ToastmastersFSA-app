document.addEventListener("DOMContentLoaded", () => {

    const sendNowCheckbox = document.getElementById("id_send_now");
    const schedulingSection = document.getElementById("scheduling-section");
    const btnText = document.getElementById("btn-text");

    function updateSchedulingVisibility() {
        if (sendNowCheckbox.checked) {
            schedulingSection.classList.add("hidden");
            btnText.textContent = "Envoyer";
        } else {
            schedulingSection.classList.remove("hidden");
            btnText.textContent = "Planifier";
        }
    }

    sendNowCheckbox.addEventListener("change", updateSchedulingVisibility);
    updateSchedulingVisibility(); 


    const editor = document.getElementById("message-editor");
    const textarea = document.getElementById("id_message");

    document.querySelectorAll(".editor-toolbar button").forEach(button => {
        button.addEventListener("click", () => {
            const command = button.dataset.command;
            document.execCommand(command, false, null);
            editor.focus();
        });
    });

    // Sync avant submit
    document.getElementById("email-form").addEventListener("submit", () => {
        textarea.value = editor.innerHTML;
    });


    const fileInput = document.getElementById("attachments");
    const fileNames = document.querySelector(".attachment-names");

    fileInput.addEventListener("change", () => {
        if (fileInput.files.length === 0) {
            fileNames.textContent = "";
            return;
        }

        const names = Array.from(fileInput.files)
            .map(file => file.name)
            .join(", ");

        fileNames.textContent = names;
    });

});
