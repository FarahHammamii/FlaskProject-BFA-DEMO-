const teamEl = document.querySelector('.formateur');
const servicesEl = document.querySelector('.services');
const viewMoreEl = document.querySelector('.view-more');
const btnMoreEl = document.querySelector('.btn-more');

document.addEventListener('DOMContentLoaded', () => {
  const backgroundImageUrls = [
    'url(/static/imgs/transp1.png)',
    'url(/static/imgs/transp2.png)',
    'url(/static/imgs/transp3.png)'
  ];
  const dots = document.querySelectorAll('.dot1');
  let currentImageIndex = 0;

  // Function to change the background image with a fade effect
  function changeBackgroundImage() {
    const sectionHero = document.querySelector('.section-hero');
    
    // Start fade-out animation
    sectionHero.classList.add('fade-out');
    
    // Wait for the fade-out animation to finish
    setTimeout(() => {
      sectionHero.style.backgroundImage = backgroundImageUrls[currentImageIndex];
      sectionHero.classList.remove('fade-out');
      sectionHero.classList.add('fade-in');
      
      // Update active dot
      dots.forEach(dot => dot.classList.remove('active'));
      dots[currentImageIndex].classList.add('active');
      
      // Remove the fade-in class after the animation ends to reset it
      setTimeout(() => sectionHero.classList.remove('fade-in'), 1000); // 1s for fade-in
    }, 500); // 500ms fade-out duration
  }

  // Function to handle click on dots
  function handleDotClick(event) {
    currentImageIndex = parseInt(event.target.getAttribute('data-index'));
    changeBackgroundImage();
  }

  // Add event listeners to the dots
  dots.forEach(dot => {
    dot.addEventListener('click', handleDotClick);
  });

  // Start the image transition
  changeBackgroundImage();

  // Set interval to change the image automatically every 5 seconds
  setInterval(() => {
    currentImageIndex = (currentImageIndex + 1) % backgroundImageUrls.length;
    changeBackgroundImage();
  }, 5000);
});



let hiddenEl;
document.addEventListener('DOMContentLoaded', () => {
  hiddenEl = document.querySelectorAll('.hidden');
});

btnMoreEl.addEventListener('click', () => {
  hiddenEl.forEach((element) => {
    element.classList.remove('hidden');
  });

  viewMoreEl.style.display = 'none';
});

const formateursContainer = document.querySelector('.formateurs-container');
const arrowLeft = document.querySelector('.arrow-left');
const arrowRight = document.querySelector('.arrow-right');

arrowLeft.addEventListener('click', () => {
  formateursContainer.scrollBy(-300, 0); 
});

arrowRight.addEventListener('click', () => {
  formateursContainer.scrollBy(300, 0); 
});