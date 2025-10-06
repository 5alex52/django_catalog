const content = document.querySelector('.content');
const header = document.querySelector('.header');
const header_after = document.querySelector('.header_after');

window.addEventListener('scroll', function () {
    var value = window.scrollY;
    (header.offsetHeight <= value + 50) ? header.classList.add('fixed') : header.classList.remove('fixed');
    (header.offsetHeight <= value + 50) ? header_after.style.height = 100 + 'px' : header_after.style.height = 0 + 'px';
});