function clickButton() {
  alert("버튼이 클릭되었습니다!");
}

function goBack() {
  history.back();
}

function goToBoard() {
  document.getElementById("board").style.display = "block";
}

function hideBoard() {
  document.getElementById("board").style.display = "none";
}