document.addEventListener('DOMContentLoaded', function() {
    const allElts = document.querySelectorAll('.App__category-item');
    allElts.forEach(item => {
        item.addEventListener('click', function(event) {
            const selectedCategory = item.parentElement.getAttribute('data-category');
            console.log("Clicked:", selectedCategory);
            localStorage.setItem('selectedCategory', selectedCategory);

            allElts.forEach(item => {
                item.classList.remove('App__category-item--selected');
            });
            item.classList.add('App__category-item--selected');

            const href = item.parentElement.getAttribute('href');
            if (href && href !== "#" && href !== "") {
                window.location.href = href;
            }
        });
    });

    const selectedCategory = localStorage.getItem('selectedCategory');
    if (selectedCategory) {
        const selectedElement = document.querySelector(`[data-category="${selectedCategory}"] .App__category-item`);
        if (selectedElement) {
            allElts.forEach(item => {
                item.classList.remove('App__category-item--selected');
            });
            selectedElement.classList.add('App__category-item--selected');
        }
    }
});
