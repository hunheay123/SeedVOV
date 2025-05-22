function addPost() {
  const title = document.getElementById("title").value;
  const content = document.getElementById("content").value;

  if (!title || !content) {
    alert("제목과 내용을 모두 입력하세요!");
    return;
  }

  const postList = document.getElementById("postList");

  const li = document.createElement("li");
  li.className = "post-item";
  li.innerHTML = `<strong>${title}</strong><p>${content}</p>
                  <button onclick="deletePost(this)">삭제</button>`;

  postList.appendChild(li);

  document.getElementById("title").value = "";
  document.getElementById("content").value = "";
}

function deletePost(button) {
  const li = button.parentElement;
  li.remove();
}
