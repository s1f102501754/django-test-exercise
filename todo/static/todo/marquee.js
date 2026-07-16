document.addEventListener('DOMContentLoaded', () => {
  const marquee = document.querySelector('.marquee');
  const image = marquee?.querySelector('.moving-image');

  if (!marquee || !image) {
    return;
  }

  let position = marquee.clientWidth;
  const speed = 120;
  let lastTime = null;

  const animate = (time) => {
    if (lastTime === null) {
      lastTime = time;
    }

    const delta = (time - lastTime) / 600;
    lastTime = time;
    position -= speed * delta;

    const imageWidth = image.getBoundingClientRect().width;
    if (position < -imageWidth) {
      position = marquee.clientWidth;
    }

    image.style.transform = `translateX(${position}px)`;
    requestAnimationFrame(animate);
  };

  requestAnimationFrame(animate);
});
