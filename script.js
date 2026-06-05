const themeToggle = document.getElementById("themeToggle");
const savedTheme = localStorage.getItem("careerCompassTheme");

if (savedTheme === "light") {
  document.body.classList.add("light-mode");
}

if (themeToggle) {
  themeToggle.addEventListener("click", () => {
    document.body.classList.toggle("light-mode");
    localStorage.setItem("careerCompassTheme", document.body.classList.contains("light-mode") ? "light" : "dark");
  });
}

const stepRange = document.getElementById("stepRange");
const stepValue = document.getElementById("stepValue");
if (stepRange && stepValue) {
  stepValue.textContent = stepRange.value;
  stepRange.addEventListener("input", () => {
    stepValue.textContent = stepRange.value;
  });
}

const timer = document.getElementById("quizTimer");
if (timer) {
  let seconds = 300;
  setInterval(() => {
    if (seconds <= 0) return;
    seconds -= 1;
    const mins = String(Math.floor(seconds / 60)).padStart(2, "0");
    const secs = String(seconds % 60).padStart(2, "0");
    timer.textContent = `${mins}:${secs}`;
  }, 1000);
}
