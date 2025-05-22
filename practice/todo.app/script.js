// 페이지 로드 시 기존 목록 불러오기
window.onload = function() {
  loadTodos();
};

function addTodo() {
  const todoInput = document.getElementById("todoInput");
  const todoText = todoInput.value.trim();

  if (todoText === "") {
    alert("할 일을 입력하세요!");
    return;
  }

  const todoList = document.getElementById("todoList");
  const li = document.createElement("li");

  const checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.onchange = function() {
    li.classList.toggle("completed");
    saveTodos();
  };

  const span = document.createElement("span");
  span.innerText = todoText;

  const delButton = document.createElement("button");
  delButton.innerText = "삭제";
  delButton.onclick = function() {
    li.remove();
    saveTodos();
  };

  li.appendChild(checkbox);
  li.appendChild(span);
  li.appendChild(delButton);

  todoList.appendChild(li);
  todoInput.value = "";

  saveTodos();
}

// 로컬스토리지에 저장
function saveTodos() {
  const todoList = document.getElementById("todoList").innerHTML;
  localStorage.setItem("todos", todoList);
}

// 로컬스토리지에서 불러오기
function loadTodos() {
  const savedTodos = localStorage.getItem("todos");
  if (savedTodos) {
    document.getElementById("todoList").innerHTML = savedTodos;

    // 이벤트 재할당 (체크박스/삭제)
    const checkboxes = document.querySelectorAll("#todoList input[type='checkbox']");
    checkboxes.forEach(checkbox => {
      checkbox.onchange = function() {
        checkbox.parentElement.classList.toggle("completed");
        saveTodos();
      };
    });

    const buttons = document.querySelectorAll("#todoList button");
    buttons.forEach(button => {
      button.onclick = function() {
        button.parentElement.remove();
        saveTodos();
      };
    });
  }
}
