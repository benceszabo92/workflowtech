// Workflow Tech — közös JS (többoldalas)
(function () {
  // mobil menü
  var burger = document.getElementById('burger');
  if (burger) burger.addEventListener('click', function () {
    document.getElementById('navlinks').classList.toggle('open');
  });

  // karusszelek (Wenzel + pályázati galériák)
  document.querySelectorAll('.carousel').forEach(function (c) {
    var track = c.querySelector('.track'),
        n = c.querySelectorAll('.slide').length,
        dots = c.querySelectorAll('.dot'),
        cur = c.querySelector('.cur');
    function go(i) {
      i = (i + n) % n; c.dataset.idx = i;
      track.style.transform = 'translateX(-' + (i * 100) + '%)';
      dots.forEach(function (d, di) { d.classList.toggle('on', di === i); });
      if (cur) cur.textContent = (i + 1);
    }
    var p = c.querySelector('.prev'), nx = c.querySelector('.next');
    if (p) p.onclick = function () { go(+c.dataset.idx - 1); };
    if (nx) nx.onclick = function () { go(+c.dataset.idx + 1); };
    dots.forEach(function (d) { d.onclick = function () { go(+d.dataset.i); }; });
  });

  // géppark fülek (CNC / Egyetemes)
  document.querySelectorAll('.tab').forEach(function (t) {
    t.addEventListener('click', function () {
      var box = t.closest('.tabhost') || document;
      box.querySelectorAll('.tab').forEach(function (x) { x.classList.remove('on'); });
      t.classList.add('on');
      box.querySelectorAll('.tabpane').forEach(function (p) { p.classList.remove('on'); });
      var pane = box.querySelector('#t-' + t.dataset.pane);
      if (pane) pane.classList.add('on');
    });
  });

  // lightbox (géppark fotók nagyítása)
  var lb = document.getElementById('lb');
  if (lb) {
    var lbi = document.getElementById('lbimg'), lbc = document.getElementById('lbcap');
    document.querySelectorAll('.imgwrap[data-img]').forEach(function (w) {
      w.addEventListener('click', function () {
        lbi.src = w.dataset.img; lbi.alt = w.dataset.name || '';
        lbc.textContent = w.dataset.name || ''; lb.classList.add('on');
      });
    });
    function close() { lb.classList.remove('on'); }
    document.getElementById('lbx').addEventListener('click', close);
    lb.querySelector('.bd').addEventListener('click', close);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  }

  // reveal animáció
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (en) { if (en.isIntersecting) en.target.classList.add('in'); });
  }, { threshold: 0.1 });
  document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
})();
