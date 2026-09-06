/* ===========================================================================
   ben-collier — agent session
   Two small behaviours and nothing else:

     1. The session block types itself out once, on load, in under two seconds.
     2. The two booking commands resolve to a calendar or a prefilled email.

   Everything on this page is present and readable in the HTML. If this file
   fails to load, or JavaScript is off, or the visitor has asked for reduced
   motion, the page renders complete and static. The animation is decoration
   layered on top of a working document, never the thing that produces it.

   AI USAGE NOTE (15-113): drafted with Claude in Claude Code, then reworked.
     - The first draft typed every line character by character, which came to
       just over four seconds. Waiting four seconds to read a name is a bad
       trade. Only the command line types now; the queue streams line by line,
       which is also closer to how an agent actually emits output.
     - It also drove the animation by writing textContent character by
       character, which destroys the markup inside each line and would have
       flattened every <b> and <span> in the queue. The queue now animates
       with a visibility flag instead, so the semantic HTML survives.
   =========================================================================== */

(function () {
  "use strict";

  /* -----------------------------------------------------------------------
     BOOKING

     TODO (Ben): paste the Calendly URL below once the event types exist.
     Both commands currently point at the same calendar. The paid tier will
     likely need its own Calendly event type with a payment collection step
     attached, at which point give `consultation` its own URL.

     While CALENDAR is empty, both commands fall back to a prefilled email and
     the page says so in plain words. A page that implies it can book and
     charge when it cannot is exactly the failure this site argues against.
     ----------------------------------------------------------------------- */
  var CALENDAR = {
    intro: "",          // e.g. "https://calendly.com/bcollier/intro-15min"
    consultation: ""    // e.g. "https://calendly.com/bcollier/consultation"
  };
  var EMAIL = "ben@collier.phd";

  var COPY = {
    intro: {
      subject: "Intro call, 15 minutes",
      body:
        "Hi Ben,\n\nI would like to book a 15 minute intro call.\n\n" +
        "What I am trying to work out:\n\n\n" +
        "Company or team:\n\n" +
        "Times that suit me:\n\n"
    },
    consultation: {
      subject: "Consulting engagement, Hot Metal AI",
      body:
        "Hi Ben,\n\nI would like to talk about a paid consulting engagement.\n\n" +
        "The decision I am stuck on:\n\n\n" +
        "Company or team:\n\n" +
        "Timing and budget:\n\n"
    }
  };

  function mailto(kind) {
    var c = COPY[kind];
    return "mailto:" + EMAIL +
      "?subject=" + encodeURIComponent(c.subject) +
      "&body=" + encodeURIComponent(c.body);
  }

  var links = document.querySelectorAll("[data-book]");
  var anyCalendar = false;

  Array.prototype.forEach.call(links, function (a) {
    var kind = a.getAttribute("data-book");
    var url = CALENDAR[kind];
    if (url) {
      a.href = url;
      a.target = "_blank";
      a.rel = "noopener";
      anyCalendar = true;
    } else {
      a.href = mailto(kind);
    }
  });

  var note = document.getElementById("book-note");
  if (note) {
    note.textContent = anyCalendar
      ? "Booking runs through Calendly. You will get a confirmation and a calendar hold straight away."
      : "The calendar is not connected yet, so both commands open a prefilled email and I reply with times. Consulting is invoiced through Hot Metal AI.";
  }

  /* -----------------------------------------------------------------------
     THE TYPING SEQUENCE

     Budget: under two seconds, start to finish.

       0     ->  533ms   command line, 41 chars at 13ms
       533   ->  653ms   pause
       653             boot line appears
       653   ->  793ms   pause
       793   -> 1618ms   five task lines at 165ms each

     Driven by requestAnimationFrame against a start timestamp, NOT by a chain
     of setTimeout calls. That matters: a chain of ~45 timers gets clamped to
     roughly 1Hz whenever the tab is not in the foreground, which stretched a
     1.6 second animation to eleven seconds in testing. Deriving the state from
     elapsed time instead means a throttled or backgrounded tab simply lands on
     the finished state when it comes back, rather than crawling through it.
     ----------------------------------------------------------------------- */

  var root = document.documentElement;
  if (root.className.indexOf("will-type") === -1) return;

  var cmd = document.querySelector('.cmd[data-type="cmd"]');
  var boot = document.querySelector('[data-type="boot"]');
  var tasks = document.querySelectorAll('[data-type="task"]');
  var idleCursor = document.querySelector(".prompt-idle .cursor");

  function revealAll() {
    if (cmd) {
      cmd.classList.add("typed");
      if (target) target.style.maxWidth = "";
    }
    if (boot) boot.classList.add("typed");
    Array.prototype.forEach.call(tasks, function (n) { n.classList.add("typed"); });
    if (cursor && cursor.parentNode) cursor.remove();
    if (idleCursor) idleCursor.style.visibility = "";
  }

  if (!cmd || !boot || !tasks.length) {
    // Something is not where it should be. Show everything rather than
    // leaving the page half hidden.
    root.className = root.className.replace(/\bwill-type\b/, "");
    return;
  }

  var target = cmd.querySelector(".t");
  var FULL = target.textContent;
  var cursor = document.createElement("span");
  cursor.className = "cursor";
  cursor.setAttribute("aria-hidden", "true");

  // Nothing is removed from the DOM. The command line reveals by widening a
  // clip in whole character units; the queue reveals by visibility. Both keep
  // their markup and their text intact for screen readers and for the case
  // where this script never finishes.
  //
  // The starting clip deliberately is NOT written here. The stylesheet already
  // holds the line at max-width:0 under .will-type, and an inline style would
  // outlive a stalled animation and keep the command hidden for good. The
  // first frame writes it, which means it is only ever written by a loop that
  // has proved it can run.
  target.after(cursor);

  // One cursor at a time: the footer prompt waits until the run has settled.
  if (idleCursor) idleCursor.style.visibility = "hidden";

  var CHAR_MS = 13;
  var CMD_END = FULL.length * CHAR_MS;   // ~533ms
  var BOOT_AT = CMD_END + 120;           // ~653ms
  var QUEUE_AT = BOOT_AT + 140;          // ~793ms
  var TASK_MS = 165;
  var END = QUEUE_AT + tasks.length * TASK_MS;

  var t0 = null;
  var shownChars = -1;
  var shownTasks = -1;
  var bootShown = false;

  function frame(now) {
    if (t0 === null) t0 = now;
    var e = now - t0;

    // A hidden tab throttles rAF to a stop. If we resume far past the end,
    // snap rather than replay a stale animation at the visitor.
    if (e > END + 4000) { revealAll(); return; }

    var chars = Math.min(FULL.length, Math.floor(e / CHAR_MS));
    if (chars !== shownChars) {
      shownChars = chars;
      target.style.maxWidth = chars + "ch";
    }

    if (!bootShown && e >= BOOT_AT) {
      bootShown = true;
      boot.classList.add("typed");
      boot.after(cursor);
    }

    if (e >= QUEUE_AT) {
      var n = Math.min(tasks.length, Math.floor((e - QUEUE_AT) / TASK_MS) + 1);
      if (n !== shownTasks) {
        for (var i = 0; i < n; i++) tasks[i].classList.add("typed");
        if (n > 0 && n <= tasks.length) tasks[n - 1].append(cursor);
        shownTasks = n;
      }
    }

    if (e >= END) {
      cmd.classList.add("typed");
      target.style.maxWidth = "";
      cursor.remove();
      if (idleCursor) idleCursor.style.visibility = "";
      return;
    }
    requestAnimationFrame(frame);
  }

  function start() {
    // Opened in a background tab: there is no animation worth showing to
    // someone who is not looking at it.
    if (document.visibilityState === "hidden") { revealAll(); return; }
    requestAnimationFrame(frame);
  }

  // Wait for the webfont so glyphs do not reflow mid-type, but cap the wait:
  // a slow font should delay the animation, not hold the page hostage.
  // Hard deadline. If the sequence has not completed by now, for any reason,
  // show everything. The CSS carries the same 2.6s fallback independently, so
  // the content appears even if this file never executes at all.
  setTimeout(function () {
    if (shownTasks < tasks.length) revealAll();
  }, 2600);

  var kicked = false;
  function kick() { if (kicked) return; kicked = true; start(); }
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(kick);
    setTimeout(kick, 350);
  } else {
    kick();
  }
})();
