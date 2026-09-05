/* ---------------------------------------------------------------------------
   Booking + consulting configuration, shared by all five design variants.

   Edit THIS FILE ONLY. Every design reads window.BOOKING from here, so a new
   Stripe link or Calendly URL goes in once rather than five times.

   To take real payments:
     1. Create a Stripe Payment Link (dashboard.stripe.com -> Payment links).
        One per offer. Stripe hosts the checkout page; nothing sensitive ever
        touches this site, which is why this is a plain URL and not a form.
     2. Paste the URL into `checkout` on the matching offer below.
     3. Optionally set `scheduler` to a Calendly/Cal.com link for the call.

   While `checkout` is empty the button falls back to a prefilled email. The
   site stays honest either way: it never pretends to take a payment it cannot.
   --------------------------------------------------------------------------- */

window.BOOKING = {
  brand: "Hot Metal AI",
  brandUrl: "",              // hotmetal.ai is not serving yet; left blank on purpose
  email: "ben@collier.phd",
  scheduler: "",             // e.g. "https://calendly.com/bcollier/consult"

  offers: [
    {
      id: "office-hour",
      name: "Consulting hour",
      price: "$450",
      unit: "60 minutes",
      blurb:
        "One call. Bring a decision you are stuck on: a model that will not hold up, " +
        "a metric nobody trusts, a hiring bar for a data team. You leave with a written " +
        "recommendation, not a proposal.",
      points: [
        "Live working session, recorded if you want it",
        "One-page written follow-up within two business days",
        "No deck, no discovery phase",
      ],
      checkout: "",
    },
    {
      id: "review",
      name: "Model or analysis review",
      price: "$2,400",
      unit: "one week",
      blurb:
        "You have a model, pipeline, or analysis about to carry a real decision. " +
        "I read the code and the assumptions, then tell you where it breaks and what " +
        "it would take to trust it.",
      points: [
        "Code, data, and evaluation reviewed end to end",
        "Written findings ranked by what would actually change the decision",
        "Ninety-minute readout with your team",
      ],
      checkout: "",
    },
    {
      id: "workshop",
      name: "Team workshop",
      price: "From $8,000",
      unit: "one to three days",
      blurb:
        "The classroom version, run inside your company. Python workflows, evaluation " +
        "that survives a business constraint, and the judgment to tell a finding from " +
        "an artifact. Built around your data, not a public dataset.",
      points: [
        "Custom curriculum built on your own problems",
        "Hands-on labs, not a lecture",
        "Delivered through Hot Metal AI",
      ],
      checkout: "",
    },
  ],
};

/* Turn an offer into the right link: hosted checkout if configured, otherwise a
   prefilled mailto. Kept here so all five designs behave identically. */
window.bookingHref = function (offer) {
  if (offer.checkout) return offer.checkout;
  const subject = encodeURIComponent("Consulting enquiry: " + offer.name);
  const body = encodeURIComponent(
    "Hi Ben,\n\nI would like to book: " +
      offer.name +
      " (" + offer.price + ", " + offer.unit + ").\n\n" +
      "What I am trying to decide:\n\n\n" +
      "Company / team:\n\n" +
      "Timing:\n\n"
  );
  return "mailto:" + window.BOOKING.email + "?subject=" + subject + "&body=" + body;
};

window.bookingCta = function (offer) {
  return offer.checkout ? "Book and pay" : "Request this";
};
