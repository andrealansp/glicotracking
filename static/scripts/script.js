document.addEventListener("DOMContentLoaded", function () {
    const pgurl = window.location.href;

    document.querySelectorAll('a.nav-link').forEach((element) => {
        if (element.classList.contains('active')) {
            element.classList.remove('active');
        }
        if (element.href === pgurl) {
            element.classList.add('active')
        }
    })

    const toggleBtn = document.getElementById('toggleNav');
    const nav = document.querySelector('.div1');
    const parent = document.querySelector('.parent');

    if (toggleBtn && nav) {
        toggleBtn.addEventListener('click', function() {
            nav.classList.toggle('recolhida');
            parent.classList.toggle('nav-collapsed');

            // Salva estado no localStorage
            localStorage.setItem('navRecolhida', nav.classList.contains('recolhida'));
        });

        // Restaura estado anterior
        if (localStorage.getItem('navRecolhida') === 'true') {
            nav.classList.add('recolhida');
            parent.classList.add('nav-collapsed');
        }
    }

})
