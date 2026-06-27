(function () {
  const header = document.getElementById('header');
  const burger = document.querySelector('.header-burger');
  const mobileMenu = document.getElementById('mobile-menu');
  const mobileClose = document.querySelector('.mobile-menu-close');
  const mobileOverlay = document.querySelector('.mobile-menu-overlay');
  const carousel = document.querySelector('[data-carousel]');

  function updateHeader() {
    if (!header) return;
    header.classList.toggle('header--scrolled', window.scrollY > 50);
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
  updateHeader();

  burger?.addEventListener('click', openMobileMenu);
  mobileClose?.addEventListener('click', closeMobileMenu);
  mobileOverlay?.addEventListener('click', closeMobileMenu);

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
    window.addEventListener('resize', () => {
      goTo(index);
    });

    updateCarousel();
  }

  const newsletterForm = document.querySelector('.newsletter-form');
  newsletterForm?.addEventListener('submit', (event) => {
    event.preventDefault();
    const input = newsletterForm.querySelector('.newsletter-input');
    if (input?.value) {
      alert('Thank you!');
      input.value = '';
    }
  });
})();
