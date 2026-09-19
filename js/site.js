/* Progressive enhancement: all page content and People links work without JS. */
(() => {
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.site-nav');
  const people = document.querySelector('.people-menu');
  if (!toggle || !nav || !people) return;
  toggle.hidden = false;
  nav.classList.add('is-enhanced');
  function closeMenu() {
    toggle.setAttribute('aria-expanded', 'false');
    nav.classList.remove('is-open');
    people.open = false;
  }
  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    toggle.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('is-open', open);
    if (!open) people.open = false;
  });
  document.addEventListener('keydown', event => {
    if (event.key !== 'Escape') return;
    if (people.open) {
      people.open = false;
      people.querySelector('summary').focus();
    } else if (nav.classList.contains('is-open')) {
      closeMenu();
      toggle.focus();
    }
  });
  document.addEventListener('click', event => {
    if (!people.contains(event.target)) people.open = false;
    if (!nav.contains(event.target) && !toggle.contains(event.target)) closeMenu();
  });
  nav.addEventListener('focusout', event => {
    if (!people.contains(event.relatedTarget)) people.open = false;
  });
  const desktop = window.matchMedia('(min-width: 56rem)');
  desktop.addEventListener('change', () => {
    const focusWasInNav = nav.contains(document.activeElement);
    closeMenu();
    if (!desktop.matches && focusWasInNav) toggle.focus();
  });
})();
