// Get the current hour
var date = new Date();
var hour = date.getHours();
// Set the color of the sky based on the hour
var sky = document.getElementById("sky");
 if (hour >= 6 && hour < 18) {
    sky.setAttribute("color", "#87CEEB"); // Light blue
  } else {
    sky.setAttribute("color", "#000000"); // Dark blue
  }
  
// // Adjust the brightness of the lamps based on the time of day
// var lamps = document.querySelectorAll("a-entity[id^='lamp']"); // Get all the lamp elements
// if (hour >= 18 || hour < 6) {
//   lamps.forEach(function(lamp) {
//     lamp.setAttribute("color", "#BF40BF"); // Brighter light at night
