(function () {
  const root = document.documentElement.getAttribute("data-root") || "";

  // The personal address is never written into the HTML (see hide_email in
  // scripts/build.py). Assemble it here so visitors see a normal link.
  const user = "ben", domain = "collier" + "." + "phd";
  const address = user + "@" + domain;
  document.querySelectorAll(".eml").forEach(function (el) {
    el.textContent = address;
    if (el.tagName === "A") el.href = "mailto:" + address;
  });

  // Booking buttons: a configured Cal.com or Calendly URL wins; otherwise an
  // email with the subject prefilled.
  const booking = (window.SITE && window.SITE.booking) || {};
  document.querySelectorAll("a[data-book]").forEach(function (a) {
    const url = booking[a.getAttribute("data-book")];
    if (url) {
      a.href = url;
      a.target = "_blank";
      a.rel = "noopener";
      if (a.dataset.liveLabel) {
        a.textContent = a.dataset.liveLabel;
        if (a.getAttribute("data-book") === "studentHours" && a.nextSibling) a.nextSibling.textContent = " with me for office hours.";
      }
    } else if (a.dataset.subject) {
      const body = "Hi Ben,\n\nI'd like to book a " + a.dataset.subject.toLowerCase() + ". A little about what I'm working on:\n\n";
      a.href = "mailto:" + address + "?subject=" + encodeURIComponent(a.dataset.subject) + "&body=" + encodeURIComponent(body);
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
      // Newest first. The home page shows only the last year, so an old post
      // never sits there looking like recent news.
      const posts = (data.posts || []).slice().sort(function (a, b) {
        return a.date < b.date ? 1 : -1;
      });
      const yearAgo = new Date(Date.now() - 365 * 24 * 3600 * 1000).toISOString().slice(0, 10);
      const recent = posts.filter(function (p) { return p.date >= yearAgo; });
      renderPosts(recent, document.getElementById("linkedin-recent"), { limit: 5 });
      renderPosts(posts, document.getElementById("linkedin-all"));
    })
    .catch(function () {
      /* Keep the HTML fallback if GitHub Pages pathing or file:// fails. */
    });
})();
