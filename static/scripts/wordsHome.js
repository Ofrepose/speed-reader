const getButton = document.querySelector("#getStartBtn");

getButton.addEventListener("mouseenter", e => {
	getButton.innerHTML = "find your book.";
});

getButton.addEventListener("mouseleave", e => {
	getButton.innerHTML = "find your book";
});
