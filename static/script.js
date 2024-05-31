// // static/script.js


// 1.Mouse Background colour
document.addEventListener('mousemove', function(e) {
    const follower = document.getElementById('cursor-follower');
    follower.style.display = 'block';
    follower.style.left = (e.pageX - 10) + 'px'; 
    follower.style.top = (e.pageY - 10) + 'px'; 
    follower.style.transform = 'scale(1.5)'; 
});

// 2.Mouse fade out effect as it moves
document.addEventListener('mousemove', function(e) {
    const follower = document.getElementById('cursor-follower');
    follower.style.display = 'block';
    follower.style.left = (e.pageX - 10) + 'px';
    follower.style.top = (e.pageY - 10) + 'px';

    // Reset any ongoing animations
    follower.style.opacity = '1';
    follower.style.transform = 'scale(1)';
    // Animate opacity and scale for a fading trail effect
    follower.animate([
        { opacity: 1, transform: 'scale(1.5)' },
        { opacity: 0, transform: 'scale(1)' }
    ], {
        duration: 1000,
        fill: 'forwards'
    });
});


// 3. Mouse CLICK Effect
function clickEffect(e) {
    const circle = document.createElement('div');
    circle.setAttribute('class', 'click-circle');
    circle.style.width = '20px';
    circle.style.height = '20px';
    circle.style.position = 'absolute';
    circle.style.borderRadius = '50%';
    circle.style.backgroundColor = 'rgba(255, 0, 0, 0.5)';
    circle.style.left = e.pageX + 'px';
    circle.style.top = e.pageY + 'px';
    document.body.appendChild(circle);

    // Animation for circle (expansion and fade out)
    circle.animate([
        { transform: 'scale(1)', opacity: 1 },
        { transform: 'scale(3)', opacity: 0 }
    ], {
        duration: 500,
        easing: 'ease-out',
        fill: 'forwards' // Keep the animation state after finishing
    });

    setTimeout(() => circle.remove(), 500); // Clean up the circle after animation
}







// Clear Button on search bar
function toggleClearButton() {
    var searchInput = document.getElementById('search');
    var clearBtn = document.querySelector('.btn-clear');
    clearBtn.style.display = searchInput.value.length > 0 ? 'block' : 'none';
  }
  
  function clearSearch() {
    var searchInput = document.getElementById('search');
    searchInput.value = '';
    searchInput.focus(); // keep focus on input after clearing
    toggleClearButton(); // Hide the clear button again
  }




document.addEventListener('DOMContentLoaded', function() {
    const triggers = document.querySelectorAll('.suggestion-wrap span');
    const panels = document.querySelectorAll('.panel');

    // Event listeners for each trigger to show/hide panels
    triggers.forEach(trigger => {
        trigger.addEventListener('click', function() {
            const panelId = trigger.id.replace('trigger', 'panel');
            panels.forEach(panel => {
                if (panel.id === panelId) {
                    panel.classList.toggle('hidden');
                } else {
                    panel.classList.add('hidden');
                }
            });
        });
    });


    populateList('ingredient-list', 
    ["Egg", "Sugar", "Flour", "Milk", "Bread", "Chicken", 
    "Rice", "Apple", "Avocado", "Banana", "Baking soda", "Baking powder", "Basil", 
    "Black pepper", "Butter", "Cheese", "Cinnamon", "Cheddar", "Clove", "Coconut", "Coriander", 
    "Cornstarch", "Cumin", "Garlic", "Honey", "Lemon", "Nutmeg", "Oats", "Olive oil", "Onion", "Orange", 
    "Oregano", "Paprika", "Parsley", "Pineapple", "Peanut butter", "Pepper", "Pumpkin", "Raisins", "Salt", 
    "Shrimp", "Soy sauce", "Tomato", "Tuna", "Vanilla extract", "Vegetable oil", "Vinegar", "Yogurt"]

);
    // populateList('nutrient-list', ["Calories", "Protein", "Fat", "Carbohydrates", "Fiber", "Sugar"]);
    populateList('category-list', ["appetizers-and-snacks", "bread","side-dish", "breakfast-and-brunch","desserts","drinks"
    ,"main-dish","meat-and-poultry","salad"]);
    // populateList('restriction-list', ["Gluten-free", "Nut-free", "Dairy-free"]);

    // Generic function to populate lists with checkboxes
    function populateList(elementId, items) {
        const list = document.getElementById(elementId);
        list.innerHTML = ''; // Clear existing items
        items.forEach(item => {
            const label = document.createElement('label');
            label.className = 'ingredient-item';
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.value = item;
            checkbox.addEventListener('change', function() {
                if (this.checked) {
                    list.insertBefore(label, list.firstChild); // Move to top
                } else {
                    list.appendChild(label); // Move to bottom
                }
            });
            label.appendChild(checkbox);
            label.appendChild(document.createTextNode(item));
            list.appendChild(label);
        });
    }
    // Search functionality for each panel
    addSearchFunctionality('ingredient-search', 'ingredient-list');
    addSearchFunctionality('nutrient-search', 'nutrient-list');
    addSearchFunctionality('category-search', 'category-list');

    // Function to add search functionality to the lists
    function addSearchFunctionality(searchInputId, listId) {
        const searchInput = document.getElementById(searchInputId);
        searchInput.addEventListener('input', function(event) {
            const searchValue = event.target.value.toLowerCase();
            const items = document.getElementById(listId).getElementsByTagName('label');
            Array.from(items).forEach(item => {
                const itemText = item.textContent.toLowerCase();
                if (itemText.includes(searchValue)) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }
});
