function showForm(formId) {
    document.querySelectorAll('.form-box').forEach(box => box.classList.remove('active'));
    document.getElementById(formId).classList.add('active');
}

function editProduct(id, name, price, category) {
    document.getElementById('modify-product-id').value = id;
    document.getElementById('modify-name').value = name;
    document.getElementById('modify-price').value = price;
    document.getElementById('modify-category').value = category;
    showForm('modify-form');
}
