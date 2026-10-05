(function () {
  "use strict";

  function onReady(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn);
    } else {
      fn();
    }
  }

  function applyTheme(isDark) {
    document.documentElement.classList.toggle("dark", isDark);
    document.documentElement.style.colorScheme = isDark ? "dark" : "light";
    try {
      localStorage.setItem("theme", isDark ? "dark" : "light");
    } catch (err) {
      /* storage may be blocked */
    }
    var btn = document.getElementById("theme-toggle");
    if (btn) {
      btn.setAttribute("aria-pressed", isDark ? "true" : "false");
      btn.setAttribute("aria-label", isDark ? "Switch to light mode" : "Switch to dark mode");
    }
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute("content", isDark ? "#344E41" : "#DAD7CD");
  }

  function initTheme() {
    var isDark = document.documentElement.classList.contains("dark");
    var btn = document.getElementById("theme-toggle");
    if (!btn) return;
    btn.setAttribute("aria-pressed", isDark ? "true" : "false");
    btn.setAttribute("aria-label", isDark ? "Switch to light mode" : "Switch to dark mode");
    btn.addEventListener("click", function () {
      applyTheme(!document.documentElement.classList.contains("dark"));
    });
  }

  function initHeader() {
    var header = document.getElementById("site-header");
    if (!header) return;
    function update() {
      header.classList.toggle("is-scrolled", window.scrollY > 8);
    }
    update();
    window.addEventListener("scroll", update, { passive: true });
  }

  function initMenu() {
    var btn = document.getElementById("menu-toggle");
    var menu = document.getElementById("mobile-menu");
    if (!btn || !menu) return;

    function setOpen(open) {
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      btn.setAttribute("aria-label", open ? "Close menu" : "Open menu");
      btn.classList.toggle("is-open", open);
      menu.classList.toggle("is-open", open);
      menu.setAttribute("aria-hidden", open ? "false" : "true");
      document.body.classList.toggle("menu-open", open);
      if (open) {
        var first = menu.querySelector("a, button");
        if (first) first.focus();
      }
    }

    btn.addEventListener("click", function () {
      setOpen(btn.getAttribute("aria-expanded") !== "true");
    });

    menu.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        setOpen(false);
      });
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && btn.getAttribute("aria-expanded") === "true") {
        setOpen(false);
        btn.focus();
      }
    });

    document.addEventListener("click", function (event) {
      if (btn.getAttribute("aria-expanded") !== "true") return;
      if (menu.contains(event.target) || btn.contains(event.target)) return;
      setOpen(false);
    });

    window.addEventListener("resize", function () {
      if (window.innerWidth >= 1024 && btn.getAttribute("aria-expanded") === "true") {
        setOpen(false);
      }
    });
  }

  function initReveal() {
    var nodes = document.querySelectorAll(".reveal");
    if (!nodes.length) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches || !("IntersectionObserver" in window)) {
      nodes.forEach(function (el) {
        el.classList.add("is-visible");
      });
      return;
    }
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -32px 0px" }
    );
    nodes.forEach(function (el) {
      observer.observe(el);
    });
  }

  function initScrollSpy() {
    var links = Array.prototype.slice.call(document.querySelectorAll("[data-nav]"));
    if (!links.length) return;
    var sections = links
      .map(function (link) {
        return document.getElementById(link.getAttribute("data-nav"));
      })
      .filter(Boolean);
    if (!sections.length || !("IntersectionObserver" in window)) return;

    var ratios = {};
    function paint() {
      var bestId = null;
      var best = 0;
      Object.keys(ratios).forEach(function (id) {
        if (ratios[id] > best) {
          best = ratios[id];
          bestId = id;
        }
      });
      links.forEach(function (link) {
        if (link.getAttribute("data-nav") === bestId) {
          link.setAttribute("aria-current", "true");
        } else {
          link.removeAttribute("aria-current");
        }
      });
    }

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          ratios[entry.target.id] = entry.isIntersecting ? entry.intersectionRatio : 0;
        });
        paint();
      },
      { rootMargin: "-30% 0px -45% 0px", threshold: [0, 0.2, 0.45, 0.7, 1] }
    );
    sections.forEach(function (section) {
      observer.observe(section);
    });
  }

  function csrfToken(form) {
    var input = form.querySelector('input[name="csrfmiddlewaretoken"]');
    if (input && input.value) return input.value;
    var meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.getAttribute("content") : "";
  }

  function bindAjaxForm(form) {
    var status = form.querySelector(".form-status");
    var button = form.querySelector('button[type="submit"]');
    var label = button ? button.querySelector(".btn-label") : null;

    function setStatus(message, kind) {
      if (!status) return;
      status.textContent = message || "";
      status.classList.remove("is-error", "is-success");
      if (kind) status.classList.add(kind === "error" ? "is-error" : "is-success");
    }

    function clearErrors() {
      form.querySelectorAll("[data-field]").forEach(function (wrap) {
        var error = wrap.querySelector(".field-error");
        var field = wrap.querySelector("input, textarea, select");
        if (error) error.textContent = "";
        if (field) field.removeAttribute("aria-invalid");
      });
      setStatus("", null);
    }

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      clearErrors();
      var original = label ? label.textContent : button ? button.textContent : "";
      if (button) {
        button.disabled = true;
        button.setAttribute("aria-busy", "true");
      }
      if (label) label.textContent = "Sending…";

      fetch(form.action, {
        method: "POST",
        body: new FormData(form),
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": csrfToken(form),
        },
      })
        .then(function (response) {
          return response.json().then(function (data) {
            return { ok: response.ok, data: data };
          });
        })
        .then(function (result) {
          if (button) {
            button.disabled = false;
            button.removeAttribute("aria-busy");
          }
          if (label) label.textContent = original;
          if (result.ok && result.data && result.data.success) {
            setStatus(result.data.message, "success");
            form.reset();
            return;
          }
          var message = (result.data && result.data.message) || "Please try again.";
          if (result.data && result.data.errors) {
            Object.keys(result.data.errors).forEach(function (key) {
              var wrap = form.querySelector('[data-field="' + key + '"]');
              if (!wrap) return;
              var error = wrap.querySelector(".field-error");
              var field = wrap.querySelector("input, textarea, select");
              if (error) error.textContent = result.data.errors[key];
              if (field) field.setAttribute("aria-invalid", "true");
            });
            message = Object.keys(result.data.errors)
              .map(function (key) {
                return result.data.errors[key];
              })
              .join(" ");
          }
          setStatus(message, "error");
        })
        .catch(function () {
          if (button) {
            button.disabled = false;
            button.removeAttribute("aria-busy");
          }
          if (label) label.textContent = original;
          setStatus("Network error. Please try again.", "error");
        });
    });
  }

  function initForms() {
    ["contact-form", "newsletter-form"].forEach(function (id) {
      var form = document.getElementById(id);
      if (form) bindAjaxForm(form);
    });
  }

  function initProgress() {
    var bar = document.getElementById("scroll-progress");
    if (!bar) return;
    function update() {
      var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      var progress = height > 0 ? (window.scrollY / height) * 100 : 0;
      bar.style.width = progress + "%";
    }
    update();
    window.addEventListener("scroll", update, { passive: true });
  }

  function initCopy() {
    document.querySelectorAll("[data-copy]").forEach(function (button) {
      button.addEventListener("click", function () {
        var value = button.getAttribute("data-copy");
        if (!value || !navigator.clipboard) return;
        var previous = button.textContent;
        navigator.clipboard.writeText(value).then(function () {
          button.textContent = "Copied";
          window.setTimeout(function () {
            button.textContent = previous;
          }, 1600);
        });
      });
    });
  }

  onReady(function () {
    initTheme();
    initHeader();
    initMenu();
    initReveal();
    initScrollSpy();
    initForms();
    initProgress();
    initCopy();
  });
})();
