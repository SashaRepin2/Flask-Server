const accordion_items = document.querySelectorAll('.accordion__item');

if (accordion_items) {
	for (item of accordion_items) {
		item.addEventListener('click', function () {
			this.classList.toggle('active');
			console.log(this);
		});
	}
}
