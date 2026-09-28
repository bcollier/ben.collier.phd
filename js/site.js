(function () {
  const root = document.documentElement.getAttribute("data-root") || "";

  // Booking buttons carry a prefilled mailto as their href. When a booking
  // URL is configured in js/config.js, point them at it instead.
  const booking = (window.SITE && window.SITE.booking) || {};
  document.querySelectorAll("a[data-book]").forEach(function (a) {
    const url = booking[a.getAttribute("data-book")];
    if (url) {
      a.href = url;
      a.target = "_blank";
      a.rel = "noopener";
      if (a.dataset.liveLabel) a.textContent = a.dataset.liveLabel;
    }
  });
  if (booking.paidHour) {
    document.querySelectorAll("[data-live-text]").forEach(function (el) {
      el.textContent = el.getAttribute("data-live-text");
    });
  }

  function renderPosts(posts, mount, opts) {
    if (!mount) return;
    const filter = (opts && opts.filter) || null;
    const limit = (opts && opts.limit) || posts.length;
    const filtered = posts.filter(function (p) {
      if (!filter) return true;
      return (p.tags || []).indexOf(filter) !== -1;
    }).slice(0, limit);

    if (!filtered.length) return;

    mount.innerHTML = filtered.map(function (p) {
      const people = (p.people || [])
        .map(function (name) {
          return "<span>" + escapeHtml(name) + "</span>";
        })
        .join("");
      const peopleBlock = people ? '<div class="people">' + people + "</div>" : "";
      const source = p.url
        ? '<div class="source"><a href="' + escapeAttr(p.url) + '">View on LinkedIn</a></div>'
        : "";
      return (
        "<li>" +
        "<time datetime=\"" + escapeAttr(p.date) + "\">" + formatDate(p.date) + "</time>" +
        '<div class="post"><p>' + escapeHtml(p.text) + "</p>" +
        peopleBlock + source + "</div></li>"
      );
    }).join("");
  }

  function formatDate(iso) {
    if (!iso) return "";
    const d = new Date(iso + "T00:00:00");
    return d.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  function escapeAttr(s) {
    return escapeHtml(s).replace(/"/g, "&quot;");
  }

  fetch(root + "data/linkedin.json")
    .then(function (r) { return r.json(); })
    .then(function (data) {
      const posts = data.posts || [];
      renderPosts(posts, document.getElementById("linkedin-recent"), { limit: 5 });
      renderPosts(posts, document.getElementById("linkedin-all"));
    })
    .catch(function () {
      /* Keep the HTML fallback if GitHub Pages pathing or file:// fails. */
    });
})();
