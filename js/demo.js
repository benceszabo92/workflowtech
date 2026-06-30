// Workflow Pro — élő demó (read-only minta). Nézetváltás + letiltott műveletek toast.
(function () {
  var root = document.getElementById('dmapp');
  if (!root) return;
  var navs = root.querySelectorAll('.dm-nav');
  var views = root.querySelectorAll('.dm-view');
  var body = root.querySelector('.dm-body');

  function show(id) {
    navs.forEach(function (n) { n.classList.toggle('on', n.dataset.view === id); });
    views.forEach(function (v) { v.classList.toggle('on', v.id === 'v-' + id); });
    if (body) body.scrollTop = 0;
  }
  navs.forEach(function (n) {
    n.addEventListener('click', function () { show(n.dataset.view); });
  });
  document.querySelectorAll('[data-go]').forEach(function (el) {
    el.addEventListener('click', function (e) { e.preventDefault(); show(el.dataset.go); });
  });

  // letiltott műveletek (minta) → toast
  var toast = document.getElementById('dm-toast'), timer;
  document.querySelectorAll('[data-lock]').forEach(function (b) {
    b.addEventListener('click', function (e) {
      e.preventDefault();
      if (!toast) return;
      toast.textContent = b.dataset.lock || 'Ez egy minta — a művelet le van tiltva.';
      toast.classList.add('show');
      clearTimeout(timer);
      timer = setTimeout(function () { toast.classList.remove('show'); }, 2400);
    });
  });
})();
