const btn = document.getElementById("dbtn");

btn.addEventListener("click", () => {
  const box = document.getElementById("dbox");
  if (box.style.display === 'none') {
    box.style.display = 'block';
    btn.style.display = 'none';
  } else {
    box.style.display = 'none';
  }
});
