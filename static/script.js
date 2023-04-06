import JSConfetti from 'js-confetti'


async function generateResponse() {
    const jsConfetti = new JSConfetti()

    const username = document.getElementById("username").value;
    const message = document.getElementById("user-input").value;
    const responseElement = document.getElementById("response");

    const loadingContainer = document.getElementById("loading-container");


    if (!username || !message) {
        alert("Please enter a username and message.");
        return;
    }
    
    // Make button disabled while making the API call
    document.getElementById("submit").disabled = true;
    // Show the spinning emoji while making the API call
    loadingContainer.style.display = "flex";

    const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, message }),
    };

    const response = await fetch("/ask", requestOptions);
    const data = await response.json();

    // Hide the spinning emoji after the API call is completed
    loadingContainer.style.display = "none";
    // Make button enabled after the API call is completed
    document.getElementById("submit").disabled = false;


    responseElement.textContent = data.response;

    // Trigger confetti
    jsConfetti.addConfetti({emojis:['📎', '🔥']})

}
