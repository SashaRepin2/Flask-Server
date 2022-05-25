function readURL(input) {
	if (input.files && input.files[0]) {
		var reader = new FileReader();

		reader.onload = function (e) {
			console.log(e.target.result);
			document.getElementById('image_load').src = e.target.result;
		};

		reader.readAsDataURL(input.files[0]);
	}
}

document.getElementById('file').onchange = function () {
	readURL(this);
};
