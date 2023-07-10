// Get the Sidebar
var mySidebar = document.getElementById("mySidebar");

// Get the DIV with overlay effect
var overlayBg = document.getElementById("myOverlay");

// Toggle between showing and hiding the sidebar, and add overlay effect
function w3_open() {
//   if (mySidebar.style.display === 'block') {
//     mySidebar.style.display = 'none';
//     overlayBg.style.display = "none";
//   } else {
//     mySidebar.style.display = 'block';
//     overlayBg.style.display = "block";
//   }
// }
  var sidebar = document.getElementById("mySidebar");
  if (sidebar.classList.contains("w3-hide")) {
    sidebar.classList.remove("w3-hide");
  } else {
    sidebar.classList.add("w3-hide");
  }
}

function AccFunc(id) {
  var x = document.getElementById(id);
  if (x.className.indexOf("w3-show") == -1) {
    x.className += " w3-show";
    x.previousElementSibling.className += " w3-green";
  } else {
    x.className = x.className.replace(" w3-show", "");
    x.previousElementSibling.className =
    x.previousElementSibling.className.replace(" w3-green", "");
  }


}

