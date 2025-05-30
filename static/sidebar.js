/* sidebar.js — one drawer behaviour on every screen
   ------------------------------------------------- */

/* ----------  BUILD MARKUP  ---------- */
const body = document.body;
const sidebar = document.createElement("aside");
const overlay = document.createElement("div");
const btnOpen = document.createElement("button");
/* --- replace ONLY this block inside sidebar.js --- */
const menuHTML = `
  <header class="flex items-center justify-between gap-2 px-6 pt-6">
    <div class="flex items-center gap-2">
      <span class="bg-amber-600 text-white font-bold px-1.5 py-0.5 rounded-sm">N</span>
      <h2 class="text-2xl font-semibold">Memo</h2>
    </div>
    <button id="btn-close" class="text-2xl hover:text-gray-700">
      <i class="fa-solid fa-xmark"></i>
    </button>
  </header>

  <nav id="nav-links" class="mt-10 flex flex-col gap-2 text-[17px] font-medium">
    <h3 class="pl-6 mb-4 text-gray-500">Menu</h3>

    <!-- DASHBOARD -->
    <a href="/dashboard/"
       data-route="dashboard"
       class="px-6 py-2 rounded-r-full hover:bg-amber-100 transition-colors">
       Dashboard
    </a>

    <!-- MY MEMOS -->
    <a href="/my_memo/"
       data-route="mymemo"
       class="px-6 py-2 rounded-r-full hover:bg-amber-100 transition-colors">
       My memo
    </a>

    <!-- ALL MEMOS -->
    <a href="/all_memo/"
       data-route="allmemo"
       class="px-6 py-2 rounded-r-full hover:bg-amber-100 transition-colors">
       All memo
    </a>

    <!-- EDIT PROFILE -->
    <a href="/edit_profile/"
       data-route="profile"
       class="px-6 py-2 rounded-r-full hover:bg-amber-100 transition-colors">
       Edit Profile
    </a>
  </nav>
`;

sidebar.innerHTML = menuHTML;
sidebar.className =
  "fixed inset-y-0 left-0 w-64 bg-rose-50 shadow-lg transform -translate-x-full " +
  "transition-transform duration-300 z-40";

overlay.className =
  "fixed inset-0 bg-black/40 opacity-0 pointer-events-none " +
  "transition-opacity duration-300 z-30";

btnOpen.innerHTML = `<i class="fa-solid fa-bars"></i>`;
btnOpen.className =
  "fixed top-6 left-6 z-50 text-2xl text-gray-700 hover:text-gray-900 focus:outline-none";

/* ----------  ATTACH  ---------- */
body.prepend(sidebar); // keep before main content
body.appendChild(overlay);
body.appendChild(btnOpen);

/* ----------  HELPERS  ---------- */
function openSidebar() {
  sidebar.style.transform = "translateX(0)";
  overlay.style.opacity = "1";
  overlay.style.pointerEvents = "auto";
  body.style.overflow = "hidden";
}
function closeSidebar() {
  sidebar.style.transform = "";
  overlay.style.opacity = "0";
  overlay.style.pointerEvents = "none";
  body.style.overflow = "";
}

/* ----------  EVENTS  ---------- */
btnOpen.addEventListener("click", openSidebar);
overlay.addEventListener("click", closeSidebar);
sidebar.querySelector("#btn-close").addEventListener("click", closeSidebar);
window.addEventListener("keydown", (e) => {
  if (e.key === "Escape") closeSidebar();
});

/* ----------  OPTIONAL: keep drawer open if user widens screen while it’s open  ----------
   Comment out these four lines if you *always* want it to stay overlay‑style. */
window.addEventListener("resize", () => {
  if (window.innerWidth < 640) return; // ignore tiny jitters on mobile
  if (
    sidebar.style.transform === "translateX(0)" &&
    window.innerWidth >= 1024
  ) {
    // keep visible but remove overlay on huge screens
    overlay.style.opacity = "0";
    overlay.style.pointerEvents = "none";
  }
});
/* 🔖 HIGHLIGHT ACTIVE LINK ------------------------------------ */
(function highlightActive() {
  const path = location.pathname.toLowerCase(); // normalize case
  let route = "";

  if (path.includes("/dashboard")) route = "dashboard";
  else if (path.includes("/my_memo")) route = "mymemo";
  else if (path.includes("/all_memo")) route = "allmemo";
  else if (path.includes("/edit_profile")) route = "profile";
  else route = "dashboard"; // fallback

  const current = sidebar.querySelector(`[data-route="${route}"]`);
  if (current) current.classList.add("bg-amber-100");
})();

/* ----------  HELPERS  ---------- */
function openSidebar() {
  sidebar.style.transform = "translateX(0)";
  overlay.style.opacity = "1";
  overlay.style.pointerEvents = "auto";
  body.style.overflow = "hidden";
  /* NEW: remember state */
  localStorage.setItem("sidebarOpen", "1");
}

function closeSidebar() {
  sidebar.style.transform = "";
  overlay.style.opacity = "0";
  overlay.style.pointerEvents = "none";
  body.style.overflow = "";
  /* NEW: forget state */
  localStorage.removeItem("sidebarOpen");
}

/* ----------  INITIAL STATE  ---------- */
if (localStorage.getItem("sidebarOpen") === "1") {
  openSidebar(); // keep it open across page loads
  overlay.style.opacity = "0"; // OPTIONAL: hide overlay if you prefer
  overlay.style.pointerEvents = "none";
  body.style.overflow = ""; // allow scroll when re‑loaded open
}
/* ----------  HELPERS  ---------- */
function openSidebar() {
  sidebar.style.transform = "translateX(0)";
  overlay.style.opacity = "1";
  overlay.style.pointerEvents = "auto";
  body.style.overflow = "hidden";
  localStorage.setItem("sidebarOpen", "1");

  /* HIDE the hamburger while drawer is open */
  btnOpen.style.display = "none";
}

function closeSidebar() {
  sidebar.style.transform = "";
  overlay.style.opacity = "0";
  overlay.style.pointerEvents = "none";
  body.style.overflow = "";
  localStorage.removeItem("sidebarOpen");

  /* SHOW the hamburger again */
  btnOpen.style.display = "";
}
