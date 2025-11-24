
function removeelement() {
	let node = document.getElementsByTagName('ol')[0];
	node.addEventListener('click', function(event) {
      this.removeChild(event.target);
   });
}

removeelement()