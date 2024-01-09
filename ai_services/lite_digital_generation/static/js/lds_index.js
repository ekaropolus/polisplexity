// Global variable for cityId
let cityId;

// Update iframe on city ID click
const cityIdLinks = document.querySelectorAll('.city-id-link');
const cityIframe = document.getElementById('city-iframe');

cityIdLinks.forEach(link => {
  link.addEventListener('click', (event) => {
    event.preventDefault();
    cityId = event.target.dataset.cityId;
    const url = `/ai_services/digital_services/city/GEN/${cityId}/`;
    cityIframe.src = url;

    // Fetch to set the city in the global cities dictionary on the server
    fetch(`/ai_services/digital_services/city/set/mongo/city/${cityId}`)
      .then(response => response.json())
      .then(data => {
        console.log(data.message);
        fetchCityStatistics(cityId);  // Fetch city statistics after setting the city
      })
      .catch(error => console.error('Error setting city:', error));

    console.log('City ID:', cityId);
  });
});


// Function to fetch city statistics and update the navbar
function fetchCityStatistics(cityId) {
  fetch(`/ai_services/digital_services/city/${cityId}/statistics/`, { method: 'GET' })
    .then(response => response.json())
    .then(data => updateNavbar(data))
    .catch(error => console.log('Error fetching city statistics:', error));
}

// Function to update the navbar with city statistics
function updateNavbar(statistics) {
  const statusSummaryContainer = document.getElementById('status-summary-container');

  // Clear existing content
  statusSummaryContainer.innerHTML = '';

  // Function to create a card for each statistic
  function createCard(title, value) {
    const card = document.createElement('div');
    card.className = 'card mb-3';

    const cardBody = document.createElement('div');
    cardBody.className = 'card-body';

    const cardTitle = document.createElement('h5');
    cardTitle.className = 'card-title';
    cardTitle.textContent = title;

    const cardText = document.createElement('p');
    cardText.className = 'card-text';
    cardText.textContent = value;

    cardBody.appendChild(cardTitle);
    cardBody.appendChild(cardText);
    card.appendChild(cardBody);

    return card;
  }

  // Loop through each statistic and create a card
  for (const key in statistics) {
    if (typeof statistics[key] === 'object' && statistics[key] !== null) {
      // If the statistic is an object, loop through its properties
      for (const subKey in statistics[key]) {
        const card = createCard(`${key} - ${subKey}`, statistics[key][subKey]);
        statusSummaryContainer.appendChild(card);
      }
    } else {
      // For non-object statistics, create a card directly
      const card = createCard(key, statistics[key]);
      statusSummaryContainer.appendChild(card);
    }
  }
}




// Create City button click event
document.getElementById("create-city-button").addEventListener("click", function() {
  createCity();
});

// Create House button click event
document.getElementById("create-house-button").addEventListener("click", function() {
  createObject("create_house");
});

// Create Store button click event
document.getElementById("create-store-button").addEventListener("click", function() {
  createObject("create_store");
});

// Create Lamp button click event
document.getElementById("create-lamp-button").addEventListener("click", function() {
  createObject("create_lamp");
});

// Create Tree button click event
document.getElementById("create-tree-button").addEventListener("click", function() {
  createObject("create_tree");
});

// Create Human button click event
document.getElementById("create-human-button").addEventListener("click", function() {
  createObject("create_human");
});

// Search button click event
document.getElementById("search-button").addEventListener("click", function() {
  const searchInput = document.getElementById("search-input");
  const query = searchInput.value.trim();
  if (query !== "") {
    searchCity(query);
  }
});

// Search button click event
document.getElementById("simulation-button").addEventListener("click", function() {
  const searchInput = document.getElementById("search-input");
  const query = searchInput.value.trim();
  if (query !== "") {
    generativeCity(query);
  }
});

// Search button click event
document.getElementById("generative-button").addEventListener("click", function() {
  const searchInput = document.getElementById("search-input");
  const query = searchInput.value.trim();
  if (query !== "") {
    generativeCity(query);
  }
});




function simulateCity(query) {
  const spinner = document.getElementById("spinner"); // Get the spinner element
  spinner.style.display = "block"; // Show the spinner before the request

  const url = `/ai_services/digital_services/city/${cityId}/simulate/?query=${encodeURIComponent(query)}`;
  fetch(url, { method: 'GET' })
    .then(response => response.json())
    .then(response => {
      spinner.style.display = "none"; // Hide the spinner after the request is complete

      const searchResponseText = document.getElementById('search-response-text');
      if (response.error) {
        searchResponseText.innerHTML += `<p>Error: ${response}</p>`;
      } else {
        searchResponseText.innerHTML += `<code>${response}</code>`;
      }
    })
    .catch(error => {
      spinner.style.display = "none"; // Hide the spinner also if there is an error
      console.log('Error searching city:', error);
    });
}

function typeWriter(text, elementId, speed, prefix = "") {
    let i = 0;
    const dest = document.getElementById(elementId);
    dest.innerHTML = prefix; // Set the prefix text

    function type() {
        if (i < text.length) {
            dest.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }

    type();
}


function searchCity(query) {
  const spinner = document.getElementById("spinner");
  spinner.style.display = "block";

  const url = `/ai_services/digital_services/city/${cityId}/ask/?query=${encodeURIComponent(query)}`;
  fetch(url, { method: 'GET' })
    .then(response => response.json())
    .then(response => {
      spinner.style.display = "none";

      const searchResponseText = 'search-response-text';
      if (response.error) {
        typeWriter(response.error, searchResponseText, 50, "<p><strong>Error:</strong> ");
      } else {
        typeWriter(response, searchResponseText, 50, "<p><strong>Response:</strong></p><p>");
      }
    })
    .catch(error => {
      spinner.style.display = "none";
      console.log('Error searching city:', error);
    });
}

function generativeCity(query) {
  const spinner = document.getElementById("spinner");
  spinner.style.display = "block";

  const url = `/ai_services/digital_services/city/${cityId}/generative/?query=${encodeURIComponent(query)}`;
  fetch(url, { method: 'GET' })
    .then(response => response.json())
    .then(response => {
      spinner.style.display = "none";

      const searchResponseText = 'search-response-text';
      if (response.error) {
        typeWriter(response.error, searchResponseText, 50, "<p><strong>Error:</strong> ");
      } else {
        typeWriter(response, searchResponseText, 50, "<p><strong>Response:</strong></p><p>");
        document.getElementById('city-iframe').contentWindow.location.reload();
      }
    })
    .catch(error => {
      spinner.style.display = "none";
      console.log('Error searching city:', error);
    });
}

// Function to create an object (house, store, lamp, tree)
function createObject(route) {
  // Get the spinner element and show it
  const spinner = document.getElementById("spinner");
  spinner.style.display = "block";

  var xhr = new XMLHttpRequest();
  console.log(cityId);

  xhr.open("POST", `/ai_services/digital_services/city/${cityId}/${route}/`, true);
  xhr.setRequestHeader("Content-Type", "application/json");

  xhr.onload = function() {
    // Hide the spinner when the request is complete
    spinner.style.display = "none";

    if (xhr.status === 200) {
      document.getElementById('city-iframe').contentWindow.location.reload();
      console.log(xhr.responseText);
    } else {
      alert("Error creating object: " + xhr.responseText);
    }
  };

  xhr.onerror = function() {
    // Hide the spinner also in case of an error
    spinner.style.display = "none";
    console.error("Request failed");
  };

  xhr.send();
}

// Clear Button click event
document.getElementById("clear-button").addEventListener("click", function() {
  clearSearchResponse();
});

// Function to clear the search response card
function clearSearchResponse() {
  document.getElementById("search-response-text").textContent = "";
}

// Function to create a city using a POST request
function createCity() {
  // Send a POST request to your server to create a new city
  fetch("/ai_services/digital_services/city/create/", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
  })
  .then(response => response.json())
  .then(data => {
    // Handle the response from the server, e.g., update UI
    console.log("City created successfully:", data);
    // You can optionally update the UI or perform any other actions here
  })
  .catch(error => {
    console.error("Error creating city:", error);
    // Handle errors, e.g., display an error message
  });
}

// Image upload button click event
document.getElementById("image-upload-button").addEventListener("click", function() {
  document.getElementById("image-input").click(); // Trigger the file input
});

// Event listener for the file input change
document.getElementById("image-input").addEventListener("change", function() {
  if (this.files.length > 0) {
    uploadImage();
  }
});

function uploadImage() {
  const spinner = document.getElementById("spinner"); // Get the spinner element
  spinner.style.display = "block"; // Show the spinner before the request

  const formData = new FormData();
  const file = document.getElementById("image-input").files[0];
  formData.append("image", file); // Add the file to the form data

  // Replace with your Flask endpoint
  const url = `/ai_services/digital_services/city/${cityId}/image/ai_ask/`;

  fetch(url, {
    method: 'POST',
    body: formData, // Send the form data
  })
  .then(response => response.json())
  .then(response => {
    spinner.style.display = "none"; // Hide the spinner after the request is complete

    const searchResponseText = document.getElementById('search-response-text');
    if (response.error) {
      searchResponseText.innerHTML += `<p>Error: ${response.error}</p>`;
    } else {
      // Display the AI response and other details
      searchResponseText.innerHTML += `
        <p><strong>Message:</strong> ${response.message}</p>
        <p><strong>AI Response:</strong> ${response.ai_response}</p>
        <img src="${response.filename}" alt="Uploaded Image" style="max-width: 100%; height: auto;">`;

      // Check if there is a video URL in the response
      if (response.video_url) {
        // Embed the video using the <video> tag
        searchResponseText.innerHTML += `
          <video controls width="400">
            <source src="${response.video_url}" type="video/mp4">
            Your browser does not support the video tag.
          </video>`;
      }
    }
  })
  .catch(error => {
    spinner.style.display = "none"; // Hide the spinner also if there is an error
    console.error('Error uploading image:', error);
  });
}


function copyToClipboard() {
  const textToCopy = document.getElementById('search-response-text').innerText;
  navigator.clipboard.writeText(textToCopy).then(() => {
    alert('Text copied to clipboard');
  }).catch(err => {
    console.error('Error in copying text: ', err);
  });
}

function shareToFacebook() {
  const textToShare = document.getElementById('search-response-text').innerText;
  const facebookUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(textToShare)}`;
  window.open(facebookUrl, '_blank');
}




