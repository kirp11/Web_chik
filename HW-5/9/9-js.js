
function removetext() {
	let node = document.getElementsByTagName('ol')[0];
	let liLast = node.lastChild;
	node.removeChild(liLast);
}