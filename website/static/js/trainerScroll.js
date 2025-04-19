document.addEventListener("DOMContentLoaded", function() {
    var scrollButton = document.querySelector('.scroll-to-top');
    
    window.addEventListener('scroll', function() {
      if (window.scrollY > 200) { 
        scrollButton.style.display = 'block';
      } else {
        scrollButton.style.display = 'none';
      }
    });
  });
  