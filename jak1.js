// app.js
const btn = document.getElementById('menuBtn');
const menu = document.getElementById('menu');
btn?.addEventListener('click', () => menu.classList.toggle('open'));

// smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(a=>{
  a.addEventListener('click', e=>{
    const id = a.getAttribute('href');
    const el = document.querySelector(id);
    if(el){ e.preventDefault(); el.scrollIntoView({behavior:'smooth'}); }
  });
});
