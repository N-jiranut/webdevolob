// Mobile Menu
const menuBtn = document.getElementById('menuBtn');
const nav = document.getElementById('primaryNav');
menuBtn?.addEventListener('click', () => {
  const open = nav.classList.toggle('open');
  menuBtn.setAttribute('aria-expanded', String(open));
});
nav?.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{
  nav.classList.remove('open');
  menuBtn?.setAttribute('aria-expanded','false');
}));

// Theme Toggle
const root = document.documentElement;
const themeToggle = document.getElementById('themeToggle');
const saved = localStorage.getItem('theme');
if(saved){ root.classList.toggle('light', saved === 'light'); }
themeToggle?.addEventListener('click', () => {
  const isLight = root.classList.toggle('light');
  localStorage.setItem('theme', isLight ? 'light' : 'dark');
});

// IntersectionObserver animations
const io = new IntersectionObserver((entries)=>{
  entries.forEach(entry=>{
    const el = entry.target;
    if(entry.isIntersecting){
      const type = el.dataset.animate;
      el.classList.add('inview', type);
      if(el.dataset.delay) el.setAttribute('data-delay', el.dataset.delay);
      io.unobserve(el);
    }
  });
}, {threshold: .14});
document.querySelectorAll('[data-animate]').forEach(el=>io.observe(el));

// Simple Slider
(function(){
  const track = document.getElementById('sliderTrack');
  if(!track) return;
  const slides = Array.from(track.children);
  let idx = 0;
  function go(n){
    idx = (n + slides.length) % slides.length;
    track.style.transform = `translateX(-${idx*100}%)`;
  }
  document.querySelector('.slider__btn--next')?.addEventListener('click', ()=>go(idx+1));
  document.querySelector('.slider__btn--prev')?.addEventListener('click', ()=>go(idx-1));
  let timer = setInterval(()=>go(idx+1), 4500);
  track.addEventListener('pointerenter', ()=>clearInterval(timer));
  track.addEventListener('pointerleave', ()=>timer = setInterval(()=>go(idx+1), 4500));
})();

// Contact Form (demo)
const form = document.getElementById('contactForm');
const statusEl = document.getElementById('formStatus');
form?.addEventListener('submit', async (e)=>{
  e.preventDefault();
  statusEl.textContent = 'กำลังส่ง...';
  const data = Object.fromEntries(new FormData(form).entries());
  if(!data.name || !data.email || !data.message){
    statusEl.textContent = 'กรุณากรอกข้อมูลให้ครบ';
    return;
  }
  try{
    const res = await fetch('/api/contact', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify(data)
    });
    if(res.ok){
      statusEl.textContent = 'ส่งเรียบร้อย ขอบคุณครับ!';
      form.reset();
    }else{
      statusEl.innerHTML = 'API ไม่พร้อม ใช้ <a href="mailto:hello@example.com">อีเมล</a> แทนได้';
    }
  }catch(err){
    statusEl.textContent = 'เครือข่ายมีปัญหา ลองใหม่อีกครั้ง';
  }
});
document.getElementById('year').textContent = new Date().getFullYear();
