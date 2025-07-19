document.addEventListener("DOMContentLoaded", function () {
    const pgurl = window.location.href;

    console.log(document.querySelectorAll('a.nav-link'))
    document.querySelectorAll('a.nav-link').forEach((element) => {
        if (element.classList.contains('active')) {
            element.classList.remove('active');
        }
        if (element.href === pgurl) {
            element.classList.add('active')
        }
    })
})