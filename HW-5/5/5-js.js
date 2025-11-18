
let inputrect = document.getElementsByClassName('rect-big')[0];

inputrect.addEventListener('mouseover', function(event) {
inputrect.textContent = 'Наведено';
});

inputrect.addEventListener('mouseout', function(event) {
inputrect.textContent = '';
});