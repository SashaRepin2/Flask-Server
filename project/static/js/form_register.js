const resetFormBtn = document.getElementById('reset_form_register');
const formRegister = document.getElementById('form_register');

resetFormBtn.addEventListener('click', e => {
	formRegister.reset();
});
