
function addspace() {
	let inputElements = document.getElementsByTagName('input');
	let inputElement = inputElements[inputElements.length-1];
	let newinput = document.createElement('input');
	inputElement.after(document.createElement('br'),document.createElement('br'), newinput);
}