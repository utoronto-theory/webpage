/* Homepage photos. The first image remains visible if JavaScript is unavailable. */
(() => {
  const carousel = document.querySelector('.photo-carousel');
  if (!carousel) return;
  const slides = Array.from(carousel.querySelectorAll('.carousel-slide'));
  const controls = carousel.querySelector('.carousel-controls');
  const previous = carousel.querySelector('.carousel-previous');
  const next = carousel.querySelector('.carousel-next');
  const caption = carousel.querySelector('.carousel-caption');
  const count = carousel.querySelector('.carousel-count');
  const status = carousel.querySelector('.carousel-status');
  if (slides.length < 2 || !controls || !previous || !next || !caption || !count || !status) return;

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let current = 0;
  let hovered = false;
  let keyboardFocused = carousel.contains(document.activeElement) && document.activeElement.matches(':focus-visible');
  let timer = null;

  function render(announce = false) {
    slides.forEach((slide, index) => {
      slide.hidden = index !== current;
      slide.classList.toggle('is-active', index === current);
    });
    caption.textContent = slides[current].dataset.caption;
    count.textContent = `${current + 1} / ${slides.length}`;
    // Do not interrupt a screen reader with announcements during automatic rotation.
    if (announce) status.textContent = `Photograph ${current + 1} of ${slides.length}: ${caption.textContent}`;
  }

  function schedule() {
    window.clearTimeout(timer);
    timer = null;
    if (reducedMotion.matches || hovered || document.hidden || keyboardFocused) return;
    timer = window.setTimeout(() => {
      current = (current + 1) % slides.length;
      render();
      schedule();
    }, 7000);
  }

  function navigate(step) {
    current = (current + step + slides.length) % slides.length;
    render(true);
    schedule();
  }

  previous.addEventListener('click', () => navigate(-1));
  next.addEventListener('click', () => navigate(1));
  carousel.addEventListener('pointerenter', event => {
    if (event.pointerType === 'touch') return;
    hovered = true;
    schedule();
  });
  carousel.addEventListener('pointerleave', event => {
    if (event.pointerType === 'touch') return;
    hovered = false;
    schedule();
  });
  // A tap can leave a button focused on phones; only keyboard focus pauses rotation.
  carousel.addEventListener('pointerdown', () => {
    keyboardFocused = false;
    schedule();
  });
  carousel.addEventListener('keydown', () => {
    keyboardFocused = true;
    schedule();
  });
  carousel.addEventListener('focusin', event => {
    keyboardFocused = event.target.matches(':focus-visible');
    schedule();
  });
  carousel.addEventListener('focusout', event => {
    keyboardFocused = carousel.contains(event.relatedTarget) && event.relatedTarget.matches(':focus-visible');
    schedule();
  });
  document.addEventListener('visibilitychange', schedule);
  reducedMotion.addEventListener('change', schedule);

  controls.hidden = false;
  render();
  schedule();
})();
