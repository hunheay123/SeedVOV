function press(value) {
  document.getElementById("display").value += value;
}

function calculate() {
  try {
    const result = eval(document.getElementById("display").value);
    document.getElementById("display").value = result;
  } catch {
    alert("잘못된 식입니다!");
  }
}

function clearDisplay() {
  document.getElementById("display").value = "";
}
