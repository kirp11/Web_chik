
function clickBtn() {
	let inputElement = document.getElementsByTagName('input')[0];
	let inputText = inputElement.value;
	if (isNaN(inputText)=== true){
		alert('Впишите число, а не текст');
	}
	else {
		alert(inputText * inputText);
	}
	inputElement.value = '';
}