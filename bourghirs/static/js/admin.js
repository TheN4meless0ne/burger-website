document.getElementById('add-item-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    // Collect form data
    const itemName = document.getElementById('item-name').value;
    const itemPrice = document.getElementById('item-price').value;
    const itemDescription = document.getElementById('item-description').value;
    const itemImage = document.getElementById('item-image').files[0];

    const allergens = Array.from(document.querySelectorAll('input[name="allergens"]:checked')).map(el => el.value);
    const tags = Array.from(document.querySelectorAll('input[name="tags"]:checked')).map(el => el.value);

    const formData = new FormData();
    formData.append('name', itemName);
    formData.append('price', parseFloat(itemPrice));
    formData.append('description', itemDescription);
    formData.append('allergens', JSON.stringify(allergens));
    formData.append('tags', JSON.stringify(tags));
    formData.append('image', itemImage);

    // Send the form data to the server using an AJAX request
    fetch('/add-item', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Handle success
            console.log('Item added successfully:', data);
        } else {
            // Handle error
            console.error('Error adding item:', data);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

function showForm() {
    document.getElementById('new-item-modal').style.display = 'block';
}

function closeForm() {
    document.getElementById('new-item-modal').style.display = 'none';
}