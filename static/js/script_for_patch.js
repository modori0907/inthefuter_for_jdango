
var button = document.getElementById('toggle-columns');
var elements = document.getElementsByClassName('toggleable');

button.addEventListener('click', function() {
for (var i = 0; i < elements.length; i++) {

  elements[i].classList.toggle('hidden');
}
});
