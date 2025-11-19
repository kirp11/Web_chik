
function clickBtn() {
	let inputElement_1 = document.getElementsByTagName('input')[0];
	let inputElement_2 = document.getElementsByTagName('input')[1];
	let inputText_1 = inputElement_1.value;
	let inputText_2 = inputElement_2.value;
	buff = inputText_1
	inputElement_1.value = inputText_2
	inputElement_2.value = buff;
}