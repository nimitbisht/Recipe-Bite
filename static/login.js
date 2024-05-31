particlesJS("particles-js", {
    particles: {
        number: {
            value: 500,
            density: {
                enable: true,
                value_area: 800
            }
        },
        color: {
            value: "#ffffff" // Change color to match salt color
        },
        shape: {
            type: "edge", // Change shape to "edge" or "triangle"
            stroke: {
                width: 0,
                color: "#000000"
            },
            polygon: {
                nb_sides: 5
            }
        },
        opacity: {
            value: 1, // Adjust opacity to your preference
            random: true,
            anim: {
                enable: true,
                speed: 1,
                opacity_min: 0.1,
                sync: false
            }
        },
        size: {
            value: 3, // Adjust size to your preference
            random: true,
            anim: {
                enable: true,
                speed: 1.5,
                size_min: 0.1,
                sync: false
            }
        },
        line_linked: {
            enable: false // Disable line linking
        },
        move: {
            enable: true,
            speed: 1.5,
            direction: "bottom",
            random: false,
            straight: false,
            out_mode: "out",
            bounce: false,
            attract: {
                enable: false,
                rotateX: 600,
                rotateY: 1200
            }
        }
    },
    retina_detect: true
});
