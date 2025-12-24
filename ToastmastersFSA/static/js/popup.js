function openPopup(htmlContent) {
  document.getElementById("popup-body").innerHTML = htmlContent;
  document.getElementById("popup").style.display = "flex";
}
function closePopup() {
  document.getElementById("popup").style.display = "none";
}