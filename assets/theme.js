(function () {
  var KEY = "malt-theme";
  var root = document.documentElement;

  function current() {
    return root.getAttribute("data-theme") === "light" ? "light" : "dark";
  }

  function apply(theme, persist) {
    var light = theme === "light";
    if (light) root.setAttribute("data-theme", "light");
    else root.removeAttribute("data-theme");
    if (persist) {
      try {
        localStorage.setItem(KEY, light ? "light" : "dark");
      } catch (e) {}
    }
    document.querySelectorAll("[data-theme-toggle]").forEach(function (btn) {
      btn.setAttribute("aria-pressed", light ? "true" : "false");
      btn.setAttribute(
        "aria-label",
        light ? "Koyu arayüze geç" : "Açık arayüze geç"
      );
      btn.title = light ? "Koyu" : "Açık";
    });
  }

  function boot() {
    var saved = null;
    try {
      saved = localStorage.getItem(KEY);
    } catch (e) {}
    apply(saved === "light" ? "light" : "dark", false);
  }

  function onClick(e) {
    var btn = e.target.closest("[data-theme-toggle]");
    if (!btn) return;
    apply(current() === "light" ? "dark" : "light", true);
  }

  boot();
  document.addEventListener("click", onClick);
})();
