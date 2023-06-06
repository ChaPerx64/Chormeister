// funtion for confimation pop-up
function dangerButtonClicked(e, link) {
  if (confirm("Are you sure?")) {
    e.preventDefault();
    window.location.href = link;
  }
}
const copyContent = async () => {
  let text = document.getElementById("field_to_copy").value;
  try {
    await navigator.clipboard.writeText(text);
    console.log("Content copied to clipboard");
  } catch (err) {
    console.error("Failed to copy: ", err);
  }
};
