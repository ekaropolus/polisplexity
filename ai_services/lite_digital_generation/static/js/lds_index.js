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
    fetchCityStatistics(cityId);
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
  const housesCount = document.getElementById('houses-count');
  const storesCount = document.getElementById('stores-count');
  const lampsCount = document.getElementById('lamps-count');
  const treesCount = document.getElementById('trees-count');
  const statusSummaryList = document.getElementById('status-summary-list');

  housesCount.textContent = `Houses: ${statistics.houses || 0}`;
  storesCount.textContent = `Stores: ${statistics.stores || 0}`;
  lampsCount.textContent = `Lamps: ${statistics.lamps || 0}`;
  treesCount.textContent = `Trees: ${statistics.trees || 0}`;

  statusSummaryList.innerHTML = '';
  for (const status in statistics.status_summary) {
    const listItem = document.createElement('li');
    listItem.textContent = `${status}: ${statistics.status_summary[status]}`;
    statusSummaryList.appendChild(listItem);
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

// Search button click event
document.getElementById("search-button").addEventListener("click", function() {
  const searchInput = document.getElementById("search-input");
  const query = searchInput.value.trim();
  if (query !== "") {
    searchCity(query);
  }
});

// Function to create an object (house, store, lamp, tree)
function createObject(route) {
  // Create a new XMLHttpRequest object
  var xhr = new XMLHttpRequest();
  console.log(cityId);

  // Define the request parameters
  xhr.open("POST", `/ai_services/digital_services/city/${cityId}/${route}/`, true);
  xhr.setRequestHeader("Content-Type", "application/json");

  // Handle the request response
  xhr.onload = function() {
    if (xhr.status === 200) {
      // Object created successfully, reload the iframe
      document.getElementById('city-iframe').contentWindow.location.reload();
      console.log(xhr.responseText);
    } else {
      // Display an error message
      alert("Error creating object: " + xhr.responseText);
    }
  };

  // Send the request
  xhr.send();
}

// Function to search the city and display the response in the card
function searchCity(query) {
  const url = `/ai_services/digital_services/city/${cityId}/ask/?query=${encodeURIComponent(query)}`;
  fetch(url, { method: 'GET' })
    .then(response => response.json())
    .then(response => {
      const searchResponseText = document.getElementById('search-response-text');
      const searchResponseCard = document.getElementById('search-response-card');

      if (response.error) {
        searchResponseText.textContent = `Error: ${response}`;
      } else {
        searchResponseText.textContent = `Response: ${response}`;
      }

      
    })
    .catch(error => console.log('Error searching city:', error));
}



// Clear Button click event
document.getElementById("clear-button").addEventListener("click", function() {
  clearSearchResponse();
});

// Function to clear the search response card
function clearSearchResponse() {
  document.getElementById("search-response-text").textContent = "";
}

// Function to search the city and display the response in the card
function createCity() {
  const url = `/ai_services/digital_services/lite/digital/GEN/`;
  fetch(url, { method: 'GET' })
    .then(response => response.json())
    .catch(error => console.log('Error searching city:', error));
}