document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");

    form.addEventListener("submit", function(event) {
        const name = document.getElementById("name").value.trim();
        const phone = document.getElementById("phone").value.trim();
        const date = document.getElementById("date").value;
        const time = document.getElementById("time").value;

        if (!name || !phone || !date || !time) {
            alert("Please fill out all fields.");
            event.preventDefault(); // Stop form submission
        }
    });
});
