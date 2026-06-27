(function () {
  const header = document.getElementById('header');
  const burger = document.querySelector('.header-burger');
  const mobileMenu = document.getElementById('mobile-menu');
  const mobileClose = document.querySelector('.mobile-menu-close');
  const carousel = document.querySelector('[data-carousel]');
  const heroSection = document.querySelector('.section--hero');

  function updateHeader() {
    if (!header) return;

    const heroBottom = heroSection
      ? heroSection.offsetTop + heroSection.offsetHeight
      : window.innerHeight;
    const isOverHero = window.scrollY < heroBottom - header.offsetHeight;

    header.classList.toggle('header--dynamic', isOverHero);
    header.classList.toggle('header--scrolled', !isOverHero);
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
    const prevBtn = carousel.querySelector('.carousel-arrow--prev');
    const nextBtn = carousel.querySelector('.carousel-arrow--next');
    const progressBar = carousel.querySelector('.carousel-progress-bar');
    let index = 0;

    function getVisibleCount() {
      const width = window.innerWidth;
      if (width <= 480) return 1;
      if (width <= 767) return 2;
      if (width <= 1024) return 3;
      return 5;
    }

    function getMaxIndex() {
      return Math.max(0, slides.length - getVisibleCount());
    }

    function updateCarousel() {
      const slide = slides[0];
      if (!slide || !track) return;

      const gap = 20;
      const slideWidth = slide.getBoundingClientRect().width + gap;
      track.style.transform = `translateX(-${index * slideWidth}px)`;

      if (progressBar) {
        const maxIndex = getMaxIndex() || 1;
        const progress = maxIndex === 0 ? 1 : index / maxIndex;
        progressBar.style.transform = `scaleX(${0.2 + progress * 0.8})`;
      }
    }

    function goTo(newIndex) {
      index = Math.max(0, Math.min(newIndex, getMaxIndex()));
      updateCarousel();
    }

    prevBtn?.addEventListener('click', () => goTo(index - 1));
    nextBtn?.addEventListener('click', () => goTo(index + 1));
    window.addEventListener('resize', () => goTo(index));

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
