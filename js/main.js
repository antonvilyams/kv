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
    const progressBar = carousel.querySelector('.carousel-progress-bar');
    const prevBtn = carousel.querySelector('.carousel-arrow--prev');
    const nextBtn = carousel.querySelector('.carousel-arrow--next');
    const gap = 20;

    if (!track) return;

    const originals = Array.from(track.querySelectorAll('.carousel-slide'));
    const total = originals.length;
    if (total === 0) return;

    originals.forEach((slide) => {
      const clone = slide.cloneNode(true);
      clone.classList.add('carousel-slide--clone');
      clone.setAttribute('aria-hidden', 'true');
      track.appendChild(clone);
    });

    originals.slice().reverse().forEach((slide) => {
      const clone = slide.cloneNode(true);
      clone.classList.add('carousel-slide--clone');
      clone.setAttribute('aria-hidden', 'true');
      track.insertBefore(clone, track.firstChild);
    });

    const slides = Array.from(track.querySelectorAll('.carousel-slide'));
    let index = total;
    let isAnimating = false;

    function getSlideStep() {
      const slide = slides[total];
      if (!slide) return 0;
      return slide.getBoundingClientRect().width + gap;
    }

    function getLogicalIndex() {
      return ((index - total) % total + total) % total;
    }

    function setTrackPosition(animate) {
      const step = getSlideStep();
      track.style.transition = animate ? 'transform 0.4s ease' : 'none';
      track.style.transform = `translateX(-${index * step}px)`;

      if (progressBar) {
        const logical = getLogicalIndex();
        progressBar.style.width = `${100 / total}%`;
        progressBar.style.transform = `translateX(${logical * 100}%)`;
      }
    }

    function normalizeIndex() {
      if (index >= total * 2) {
        index -= total;
        setTrackPosition(false);
      } else if (index < total) {
        index += total;
        setTrackPosition(false);
      }
    }

    function goTo(newIndex) {
      if (isAnimating) return;
      index = newIndex;
      isAnimating = true;
      setTrackPosition(true);
    }

    track.addEventListener('transitionend', (event) => {
      if (event.target !== track || event.propertyName !== 'transform') return;
      normalizeIndex();
      isAnimating = false;
    });

    prevBtn?.addEventListener('click', () => goTo(index - 1));
    nextBtn?.addEventListener('click', () => goTo(index + 1));

    window.addEventListener('resize', () => {
      setTrackPosition(false);
    }, { passive: true });

    setTrackPosition(false);
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
