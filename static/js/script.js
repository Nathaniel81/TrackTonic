document.addEventListener('DOMContentLoaded', function() {
    const allElts = document.querySelectorAll('.App__category-item');
    allElts.forEach(item => {
        item.addEventListener('click', function() {
            console.log("Clicked");
            allElts.forEach(item => {
                item.classList.remove('App__category-item--selected');
            });
            item.classList.add('App__category-item--selected');
        });
    });
});
