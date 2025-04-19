document.addEventListener("DOMContentLoaded", function () {
  console.log("DOM fully loaded and parsed");
  setTimeout(function () {
    console.log("Hiding loading screen");
    document.getElementById("loading-screen").style.display = "none";
    document.getElementById("main-content").style.display = "block";
  }, 3000); // 3 seconds delay, adjust as needed
});
