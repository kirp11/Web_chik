
function Apptext() {
	let node = document.getElementsByTagName('ol')[0];
	let liLast = document.createElement('li');
	liLast.innerHTML = 'Текст';
	node.append(liLast);
}