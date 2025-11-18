
function blockBtn() {
	let inputElement = document.getElementsByTagName('input')[0];
	inputElement.setAttribute("disabled", "disabled");
}

function unblockBtn() {
	let inputElement = document.getElementsByTagName('input')[0];
	inputElement.removeAttribute("disabled");
}