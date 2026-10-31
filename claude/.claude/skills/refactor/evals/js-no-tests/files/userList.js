// ユーザー一覧を表示するためのモジュールです。
// このファイルではユーザーのデータを取得して、フィルターして、表示します。

const API = "https://example.com/api/users";

// fetchを呼び出す関数
async function doFetch(url) {
  return await fetch(url);
}

// JSONを取得する関数
async function get_json(url) {
  const res = await doFetch(url);
  return await res.json();
}

function getUserName(u) {
  return u.name;
}

// ユーザー一覧を読み込んで画面に表示する
async function loadAndRenderUsers(showInactive, sortByName) {
  const data = await get_json(API);
  let list = [];
  // データをループする
  for (let i = 0; i < data.length; i++) {
    const u = data[i];
    if (!showInactive) {
      if (u.status !== "active") {
        continue;
      }
    }
    if (u.role === "admin" || u.role === "owner") {
      u.isAdmin = true;
    } else {
      u.isAdmin = false;
    }
    if (u.lastLogin && Date.now() - new Date(u.lastLogin).getTime() > 2592000000) {
      u.stale = true;
    }
    list.push(u);
  }
  if (sortByName) {
    list.sort((a, b) => (getUserName(a) < getUserName(b) ? -1 : 1));
  }
  // HTMLを作る
  const el = document.getElementById("user-list");
  el.innerHTML = "";
  for (const user of list) {
    const li = document.createElement("li");
    li.textContent = getUserName(user) + (user.isAdmin ? " (admin)" : "") + (user.stale ? " *" : "");
    el.appendChild(li);
  }
  // 件数を表示する
  document.getElementById("user-count").textContent = list.length + " users";
}

function fetchUserCount() {
  return document.querySelectorAll("#user-list li").length;
}

module.exports = { loadAndRenderUsers, fetchUserCount };
