/* Google Analytics 4 for ben.collier.phd.

   Loaded from every page's <head> only when data/site.json has a "ga4_id".
   GA4 itself measures page views, time on site (engagement time), scroll
   depth, outbound links, file downloads (the PDFs), and where visitors come
   from. This file adds one event, ui_click, for every link or button pressed,
   with what it said (click_label) and where on the page it was (click_area),
   so the nav tabs, Book a call, reel play buttons and the robot's note can be
   compared. Ad features and Google signals are off.

   Not counted: localhost and file:// copies, headless browsers (our own
   screenshot and video renders), and anyone who has opened any page with
   ?notrack once in that browser (Ben's own visits). ?track turns it back on. */
(function () {
  "use strict";
  var me = document.currentScript;
  var id = me && me.getAttribute("data-ga");
  if (!id) return;
  try {
    if (/[?&]notrack\b/.test(location.search)) localStorage.setItem("nb-notrack", "1");
    if (/[?&]track\b/.test(location.search)) localStorage.removeItem("nb-notrack");
    if (localStorage.getItem("nb-notrack") === "1") return;
  } catch (e) { /* storage blocked: count the visit */ }
  if (location.protocol === "file:" || /^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname)) return;
  if (navigator.webdriver || /HeadlessChrome/.test(navigator.userAgent) || /[?&]capture\b/.test(location.search)) return;

  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;
  gtag("js", new Date());
  gtag("config", id, { allow_google_signals: false, allow_ad_personalization_signals: false });
  var s = document.createElement("script");
  s.async = true;
  s.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(id);
  document.head.appendChild(s);

  // Where on the page a click happened, in words a report can group by.
  function area(el) {
    if (el.closest(".tabs")) return "nav tab";
    if (el.closest(".sticky-cta")) return "book a call (header)";
    if (el.closest(".brand")) return "logo";
    if (el.closest(".foot")) return "footer";
    if (el.closest(".bot, .bot-sign")) return "robot";
    if (el.closest(".reel, .v2")) return "reels player";
    var sec = el.closest("section[id], section[aria-labelledby], [id]:not(main)");
    if (sec) return sec.id || sec.getAttribute("aria-labelledby");
    return "page";
  }

  document.addEventListener("click", function (e) {
    var el = e.target && e.target.closest && e.target.closest("a, button, summary, [role='button']");
    if (!el) return;
    // The visible words, without small print or icons ("Book a call", not "Book a call free, 15 minutes").
    var copy = el.cloneNode(true);
    Array.prototype.forEach.call(copy.querySelectorAll("small, svg"), function (n) { n.remove(); });
    var label = (el.getAttribute("aria-label") || copy.textContent || el.getAttribute("title") || "")
      .replace(/[\s\u2192]+/g, " ").trim().slice(0, 100);
    gtag("event", "ui_click", {
      click_label: label || "(no text)",
      click_area: area(el),
      link_url: el.href ? String(el.href).slice(0, 300) : ""
    });
  }, true);
})();
