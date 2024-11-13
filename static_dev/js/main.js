document.addEventListener('DOMContentLoaded', function () {
    // Registrar el plugin ScrollTrigger
    gsap.registerPlugin(ScrollTrigger);

    // Función para animar el carrusel
    function animateCarousel() {
        gsap.fromTo("#carouselBanner .carousel-item img",
            { scale: 1.1 }, // Comienza con la imagen aumentada
            { scale: 1, duration: 10, ease: "power1.inOut", repeat: -1, yoyo: true } // Se aleja lentamente
        );
    }

    //// Función para animar el contenedor del logo
    function animateLogoContainer() {
        console.log('Animating logo container');
        gsap.set(".carousel-logo-container", { opacity: 1 }); // Asegúrate de que el contenedor sea visible
        gsap.from(".carousel-logo-container", {
            y: -25, // Desplazamiento inicial desde la izquierda
            opacity: 0, // Comienza con opacidad 0
            duration: 1.7, // Duración de la animación
            ease: "power2.out", // Tipo de easing
            scrollTrigger: {
                trigger: ".carousel-logo-container",
                start: "top 80%", // Inicia la animación cuando el elemento está al 80% de la vista
                toggleActions: "play none none none" // Reproduce la animación al cargar la página
            },
            clearProps: "all" // Elimina las propiedades establecidas por GSAP después de la animación
        });
    }

    // Función para animar el texto de la misión
    function animateMissionText() {
        console.log('Animating mission text');
        gsap.from(".mission-text", {
            opacity: 0, // Comienza con opacidad 0
            duration: 1.7, // Duración de la animación
            ease: "power2.out", // Tipo de easing
            scrollTrigger: {
                trigger: ".mission-text",
                start: "top 80%", // Inicia la animación cuando el elemento está al 80% de la vista
                toggleActions: "play none none none" // Reproduce la animación al cargar la página
            },
            clearProps: "all"
        });
    }

    // Función para animar los títulos h2
    function animateTitles() {
        gsap.from("h2.text-center.mb-4", {
            y: 50, // Desplazamiento inicial desde abajo
            opacity: 0, // Comienza con opacidad 0
            duration: 1.5, // Duración de la animación
            ease: "power2.out", // Tipo de easing
            scrollTrigger: {
                trigger: "h2.text-center.mb-4",
                start: "top 80%", // Inicia la animación cuando el elemento está al 80% de la vista
                toggleActions: "play none none none" // Reproduce la animación al cargar la página
            },
            clearProps: "all"
        });
    }

    // Función para animar los contenedores de características
    function animateFeatureContainers() {
        gsap.from(".feature-container", {
            y: 50, // Desplazamiento inicial desde abajo
            opacity: 0, // Comienza con opacidad 0
            duration: 1.5, // Duración de la animación
            ease: "power2.out", // Tipo de easing
            stagger: 0.3, // Retraso entre las animaciones de cada elemento
            scrollTrigger: {
                trigger: ".feature-container",
                start: "top 80%", // Inicia la animación cuando el elemento está al 80% de la vista
                toggleActions: "play none none none" // Reproduce la animación al cargar la página
            }
        });
    }
    // Llamar a las funciones de animación al cargar la página
    animateCarousel();
    animateLogoContainer();
    animateMissionText();
    animateTitles();
    animateFeatureContainers();

    // Agregar sombra al navbar al hacer scroll
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', function () {
        if (window.scrollY > 0) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
});




// Fancybox para las imágenes
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