(function () {
  const header = document.getElementById('header');
  const burger = document.querySelector('.header-burger');
  const mobileMenu = document.getElementById('mobile-menu');
  const mobileClose = document.querySelector('.mobile-menu-close');
  const carousel = document.querySelector('[data-carousel]');
  const heroSection = document.querySelector('.section--hero');

  function updateHeader() {
    if (!header) return;

    const atHeroTop = heroSection && window.scrollY < 80;
    header.classList.toggle('header--dynamic', atHeroTop);
    header.classList.toggle('header--scrolled', !atHeroTop);
  }

  function openMobileMenu() {
    if (!mobileMenu || !burger) return;
    mobileMenu.classList.add('is-open');
    mobileMenu.setAttribute('aria-hidden', 'false');
    burger.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
  }

  function closeMobileMenu() {
    if (!mobileMenu || !burger) return;
    mobileMenu.classList.remove('is-open');
    mobileMenu.setAttribute('aria-hidden', 'true');
    burger.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  }

  window.addEventListener('scroll', updateHeader, { passive: true });
  window.addEventListener('resize', updateHeader, { passive: true });
  updateHeader();

  burger?.addEventListener('click', openMobileMenu);
  mobileClose?.addEventListener('click', closeMobileMenu);

  document.querySelectorAll('.mobile-menu-list a').forEach((link) => {
    link.addEventListener('click', closeMobileMenu);
  });

  if (carousel) {
    const track = carousel.querySelector('.carousel-track');
    const slides = Array.from(carousel.querySelectorAll('.carousel-slide'));
    const viewport = carousel.querySelector('.carousel-viewport');
    const prevBtn = carousel.querySelector('.carousel-arrow--prev');
    const nextBtn = carousel.querySelector('.carousel-arrow--next');
    const progressBar = carousel.querySelector('.carousel-progress-bar');
    const gap = 20;
    let index = 0;

    function getSlideStep() {
      const slide = slides[0];
      if (!slide) return 0;
      return slide.getBoundingClientRect().width + gap;
    }

    function updateCarousel() {
      if (!track || !slides.length) return;

      const step = getSlideStep();
      track.style.transform = `translateX(-${index * step}px)`;

      if (progressBar) {
        const segmentWidth = 100 / slides.length;
        progressBar.style.width = `${segmentWidth}%`;
        progressBar.style.transform = `translateX(${index * 100}%)`;
      }
    }

    function goTo(newIndex) {
      const total = slides.length;
      if (total === 0) return;

      if (newIndex < 0) {
        index = total - 1;
      } else if (newIndex >= total) {
        index = 0;
      } else {
        index = newIndex;
      }

      updateCarousel();
    }

    prevBtn?.addEventListener('click', () => goTo(index - 1));
    nextBtn?.addEventListener('click', () => goTo(index + 1));

    window.addEventListener('resize', () => updateCarousel(), { passive: true });
    updateCarousel();
  }

  function handleFormSubmit(form) {
    form.addEventListener('submit', (event) => {
      event.preventDefault();

      if (form.dataset.form === 'contact') {
        const wrapper = form.closest('.contact-form') || form.parentElement;
        if (wrapper) wrapper.classList.add('is-submitted');
        const success = form.querySelector('.contact-form-success');
        if (success) success.hidden = false;
        return;
      }

      if (form.dataset.form === 'newsletter') {
        const input = form.querySelector('input[type="email"]');
        if (input?.value) {
          alert('Thank you!');
          input.value = '';
        }
      }
    });
  }

  document.querySelectorAll('form[data-form]').forEach(handleFormSubmit);

  document.querySelectorAll('a[href="#contact-form"]').forEach((link) => {
    link.addEventListener('click', (event) => {
      event.preventDefault();
      document.getElementById('contact-form')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });
})();
