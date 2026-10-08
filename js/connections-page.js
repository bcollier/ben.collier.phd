/* /connections/: mounts the Connections game (js/connections/, synced from the
   connections_demo repo) and wires the sticky-note theme picker to it. */
(function () {
  var mountEl = document.getElementById('cx-game');
  if (!mountEl || !window.ConnectionsPlayer || !window.CONNECTIONS_PACKS) return;
  var buttons = Array.prototype.slice.call(document.querySelectorAll('.cx-theme'));
  var card = document.querySelector('.cx-card');
  var game = window.ConnectionsPlayer.mount(mountEl, {
    packs: window.CONNECTIONS_PACKS,
    pack: 'ben',
    picker: false,
    useUrl: true,
    shareUrl: location.origin + location.pathname,
    onChange: function (id) {
      buttons.forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-pack') === id)); });
      if (card) card.setAttribute('data-theme', id);
    },
  });
  buttons.forEach(function (b) {
    b.addEventListener('click', function () { game.setPack(b.getAttribute('data-pack'), 0, true); });
  });
})();
