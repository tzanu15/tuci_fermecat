
    document.addEventListener("DOMContentLoaded", function() {
        var carousel = new bootstrap.Carousel(document.getElementById("welcomeCarousel"), {
            interval: 20000, // Se schimbă automat la 20 secunde
            pause: false
        });

        // La click pe imagine, trece la următorul slide
        document.getElementById("welcomeCarousel").addEventListener("click", function() {
            carousel.next();
        });
    });