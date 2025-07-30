// // welcome.js
window.addEventListener('DOMContentLoaded', () => {
  console.log('Cyber Shield Dashboard loaded');
  
  const testLink = document.querySelector('a[href="cybersheild.html"]');
  const fetchLink = document.querySelector('a[href="fetchdata.html"]');

  if (testLink && fetchLink) {
    console.log('Navigation buttons are ready.');
  } else {
    console.warn('One or both navigation links not found.');
  }
});
