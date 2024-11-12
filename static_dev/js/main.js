// GSAP para el efecto de zoom en el carrusel
gsap.fromTo("#carouselBanner .carousel-item img",
    { scale: 1.1 }, // Comienza con la imagen aumentada
    { scale: 1, duration: 10, ease: "power1.inOut", repeat: -1, yoyo: true } // Se aleja lentamente
);

// Definir la función de animación para el logo-container
function animateLogoContainer() {
    gsap.from(".carousel-logo-container", {
        x: -250, // Desplazamiento inicial desde la izquierda
        opacity: 0, // Comienza con opacidad 0
        duration: 1.7, // Duración de la animación
        ease: "power2.out", // Tipo de easing
        scrollTrigger: {
            trigger: ".carousel-logo-container",
            start: "top 80%", // Inicia la animación cuando el elemento está al 80% de la vista
            toggleActions: "play none none none" // Reproduce la animación al cargar la página
        }
    });
}

// Llamar a la función de animación al cargar la página
document.addEventListener("DOMContentLoaded", function () {
    animateLogoContainer();
});

// Fancybox para las imágenes //
$(document).ready(function () {
    $('[data-fancybox]').fancybox({
        // Opciones personalizadas
        buttons: [
            "zoom",
            "slideShow",
            "thumbs",
            "close"
        ],
        loop: true,
        protect: true
    });
});