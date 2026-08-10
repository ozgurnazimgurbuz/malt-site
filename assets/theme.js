(function () {
  var KEY = "malt-theme";
  var ORDER = ["dark", "light", "liquid"];
  var root = document.documentElement;

  var META = {
    dark: {
      nextLabel: "Açık arayüze geç",
      title: "Koyu",
      pressed: "false",
    },
    light: {
      nextLabel: "Liquid Glass arayüze geç",
      title: "Açık",
      pressed: "true",
    },
    liquid: {
      nextLabel: "Koyu arayüze geç",
      title: "Liquid Glass",
      pressed: "mixed",
    },
  };

  function normalize(raw) {
    if (raw === "light" || raw === "liquid") return raw;
    return "dark";
  }

  function current() {
    if (root.classList.contains("liquid-glass")) return "liquid";
    if (root.getAttribute("data-theme") === "light") return "light";
    return "dark";
  }

  function nextOf(theme) {
    var i = ORDER.indexOf(theme);
    return ORDER[(i + 1) % ORDER.length];
  }

  function apply(theme, persist) {
    theme = normalize(theme);
    root.classList.toggle("liquid-glass", theme === "liquid");
    if (theme === "light") root.setAttribute("data-theme", "light");
    else root.removeAttribute("data-theme");

    if (persist) {
      try {
        localStorage.setItem(KEY, theme);
      } catch (e) {}
    }

    var meta = META[theme];
    document.querySelectorAll("[data-theme-toggle]").forEach(function (btn) {
      btn.setAttribute("aria-pressed", meta.pressed);
      btn.setAttribute("aria-label", meta.nextLabel);
      btn.title = meta.title;
      btn.setAttribute("data-theme-current", theme);
    });
  }

  function boot() {
    var saved = null;
    try {
      saved = localStorage.getItem(KEY);
    } catch (e) {}
    apply(normalize(saved), false);
  }

  function onClick(e) {
    var btn = e.target.closest("[data-theme-toggle]");
    if (!btn) return;
    apply(nextOf(current()), true);
  }

  boot();
  document.addEventListener("click", onClick);
})();
