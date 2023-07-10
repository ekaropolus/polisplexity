// Add event listener to each toggle button
var toggleButtons = document.querySelectorAll(".toggle-btn");
toggleButtons.forEach(function(button) {
  button.addEventListener("click", function() {
    // Toggle visibility of service description and service iframe
    var card = button.closest(".service-card");
    var details = card.querySelector(".service-details");

    var iframeContainer = card.querySelector(".service-iframe-container");
    if (iframeContainer.style.display === "none") {
      iframeContainer.style.display = "block";
      button.textContent = "Try Service";
    } else {
      iframeContainer.style.display = "none";
      button.textContent = "Close Service";
    }
  });
});



