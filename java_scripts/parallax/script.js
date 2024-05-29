const parallaxBackground = document.querySelector('.parallax-background');
const parallaxBackgroundLayer1 = document.querySelector('.parallax-background-layer-1');
const parallaxBackgroundLayer2 = document.querySelector('.parallax-background-layer-2');
const parallaxMidground = document.querySelector('.parallax-midground');

window.addEventListener('scroll', () => {
  const scrollPosition = window.scrollY;
  parallaxBackground.style.transform = `translateY(${scrollPosition * 0.25}px) translateZ(-1px) scale(2)`;
  parallaxBackgroundLayer1.style.transform = `translateY(${scrollPosition * 0.15}px) translateZ(-0.5px) scale(1.5)`;
  parallaxBackgroundLayer2.style.transform = `translateY(${scrollPosition * 0.05}px) translateZ(0px) scale(1)`;
  parallaxMidground.style.transform = `translateY(${scrollPosition * 0.1}px) translateZ(0.5px) scale(1.5)`;
});