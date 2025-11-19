
function divBtn() {
	lists = ["1.jpg", "2.jpg","3.jpg","4.jpg"]
	var randomIndex = Math.floor(Math.random() * lists.length)
	var randomElement = lists[randomIndex]

	document.getElementsByTagName('img')[0].src = randomElement
}