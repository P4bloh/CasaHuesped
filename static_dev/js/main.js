// GSAP para el efecto de zoom en el carrusel
gsap.fromTo("#carouselBanner .carousel-item img",
    { scale: 1.1 }, // Comienza con la imagen aumentada
    { scale: 1, duration: 10, ease: "power1.inOut", repeat: -1, yoyo: true } // Se aleja lentamente
);

