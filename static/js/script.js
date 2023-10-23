function loadContent(url) {
	fetch(url)
		.then(response => response.json())
		.then(data => {
			document.querySelector(".App__main-view").innerHTML = 
			`<div class="App__main-view">
			<div class="App__top-gradient"></div>
			<div class="App__header-placeholder"></div>
			<section class="App__section App__quick-links">
			  <h1>Good afternoon</h1>
			  <div class="App__quick-links-container">
				<div class="App__quick-link">
				  <div class="App__quick-link-featured-img">♥</div>
				  <span>Liked Songs</span>
				</div>
				<div class="App__quick-link">
				  <div class="App__quick-link-featured-img"></div>
				  <span>Daily Mix 1</span>
				</div>
				<div class="App__quick-link">
				  <div class="App__quick-link-featured-img"></div>
				  <span>Discover Weekly</span>
				</div>
				<div class="App__quick-link">
				  <div class="App__quick-link-featured-img"></div>
				  <span>Daily Mix 2</span>
				</div>
				<div class="App__quick-link">
				  <div class="App__quick-link-featured-img"></div>
				  <span>Daily Mix 3</span>
				</div>
				<div class="App__quick-link">
				  <div class="App__quick-link-featured-img"></div>
				  <span>Daily Mix 4</span>
				</div>
			  </div>
			</section>
			<section class="App__section App__your-shows">
			  <div class="App__section-header">
				<h3>Your shows</h3>
				<span>SEE ALL</span>
			  </div>
			  <div class="App__section-grid-container">
				<div class="App__section-grid-item">
				  <div class="featured-image"></div>
				  <h3>TED Radio Hour</h3>
				  <span>NPR</span>
				</div>
				<div class="App__section-grid-item">
				  <div class="featured-image"></div>
				  <h3>Short Wave</h3>
				  <span>NPR</span>
				</div>
				<div class="App__section-grid-item">
				  <div class="featured-image"></div>
				  <h3>Post Reports</h3>
				  <span>The Washington Post</span>
				</div>
				<div class="App__section-grid-item">
				  <div class="featured-image"></div>
				  <h3>Planet Money</h3>
				  <span>NPR</span>
				</div>
				<div class="App__section-grid-item">
				  <div class="featured-image"></div>
				  <h3>How I Built this...</h3>
				  <span>NPR</span>
				</div>
				<div class="App__section-grid-item">
				  <div class="featured-image"></div>
				  <h3>TED Radio Hour</h3>
				  <span>NPR</span>
				</div>
				<div class="App__section-grid-item">
				  <div class="featured-image"></div>
				  <h3>Short Wave</h3>
				  <span>NPR</span>
				</div>
				<div class="App__section-grid-item">
				  <div class="featured-image"></div>
				  <h3>Post Reports</h3>
				  <span>The Washington Post</span>
				</div>
				<div class="App__section-grid-item">
				  <div class="featured-image"></div>
				  <h3>Planet Money</h3>
				  <span>NPR</span>
				</div>
				<div class="App__section-grid-item">
				  <div class="featured-image"></div>
				  <h3>How I Built this...</h3>
				  <span>NPR</span>
				</div>
			  </div>
			</section>
			<section class="App__section App__your-shows">
			  <div class="App__section-header">
				<h3>Your top mixes</h3>
				<span>SEE ALL</span>
			  </div>
			  <div class="App__section-grid-container">
				<div class="App__section-grid-item">
				  <div class="featured-image"></div>
				  <h3>TED Radio Hour</h3>
				  <span>NPR</span>
				</div>
				<div class="App__section-grid-item">
				  <div class="featured-image"></div>
				  <h3>Short Wave</h3>
				  <span>NPR</span>
				</div>
				<div class="App__section-grid-item">
				  <div class="featured-image"></div>
				  <h3>Post Reports</h3>
				  <span>The Washington Post</span>
				</div>
				<div class="App__section-grid-item">
				  <div class="featured-image"></div>
				  <h3>Planet Money</h3>
				  <span>NPR</span>
				</div>
				<div class="App__section-grid-item">
				  <div class="featured-image"></div>
				  <h3>How I Built this...</h3>
				  <span>NPR</span>
				</div>
				<div class="App__section-grid-item">
				  <div class="featured-image"></div>
				  <h3>TED Radio Hour</h3>
				  <span>NPR</span>
				</div>
				<div class="App__section-grid-item">
				  <div class="featured-image"></div>
				  <h3>Short Wave</h3>
				  <span>NPR</span>
				</div>
				<div class="App__section-grid-item">
				  <div class="featured-image"></div>
				  <h3>Post Reports</h3>
				  <span>The Washington Post</span>
				</div>
				<div class="App__section-grid-item">
				  <div class="featured-image"></div>
				  <h3>Planet Money</h3>
				  <span>NPR</span>
				</div>
				<div class="App__section-grid-item">
				  <div class="featured-image"></div>
				  <h3>How I Built this...</h3>
				  <span>NPR</span>
				</div>
			  </div>
			  
			</section>
		  </div>
	`
		})
		.catch(error => console.error('Error:', error));
}

document.addEventListener('DOMContentLoaded', function() {
    const allElts = document.querySelectorAll('.App__category-item');

    allElts.forEach(item => {
        item.addEventListener('click', function() {
            console.log("Clicked");
            allElts.forEach(item => {
                item.classList.remove('App__category-item--selected');
            });
            item.classList.add('App__category-item--selected');
			const url = item.getAttribute("data-url");
			loadContent(url);
        });
    });
});
