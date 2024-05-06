const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth * 0.8;
canvas.height = window.innerHeight;

// Variables for simulation
let gravity = 0.08;
let density = 1;
let explosionType = 1;

// Item class representing a damageable object
class Item {
    constructor(x, y, hp = 100, width = 50, height = 50) {
        this.x = x;
        this.y = y;
        this.hp = hp;
        this.width = width;
        this.height = height;
    }
    
    draw() {
        ctx.fillStyle = this.hp > 0 ? "green" : "red"; // Change color based on HP
        ctx.fillRect(this.x - this.width / 2, this.y - this.height / 2, this.width, this.height);
    }
}

// Global variable for item
let item;

// Add item to the canvas
function addItem(x) {
    item = new Item(x * canvas.width / 100, canvas.height / 2); // Place it along the x-axis
}

// Event listeners for GUI changes
document.getElementById('gravity-slider').addEventListener('input', (e) => {
    gravity = parseFloat(e.target.value);
    document.getElementById('gravity-value').innerText = gravity.toFixed(2);
});

document.getElementById('density-slider').addEventListener('input', (e) => {
    density = parseFloat(e.target.value);
    document.getElementById('density-value').innerText = density.toFixed(1);
});

document.getElementById('explosion-type').addEventListener('change', (e) => {
    explosionType = parseInt(e.target.value, 10);
});

document.getElementById('item-position').addEventListener('input', (e) => {
    const position = parseInt(e.target.value, 10);
    document.getElementById('item-position-value').innerText = position;
});

document.getElementById('add-item').addEventListener('click', () => {
    const position = parseInt(document.getElementById('item-position').value, 10);
    addItem(position);
    document.getElementById('item-hp').innerText = item.hp; // Reset HP
});

// Function to calculate damage based on explosion type and distance
function calculateDamage(explosionPos, itemPos, type) {
    const distance = Math.abs(explosionPos.x - itemPos.x);
    let damage;
    
    if (type === 1) { // Explosion type 1
        damage = Math.max(0, 100 - (distance / 10)); // Simple linear reduction with distance
    } else { // Explosion type 2
        damage = Math.max(0, 200 - (distance / 5)); // Higher initial damage, but falls off faster
    }
    
    return damage;
}

// Particle class for explosions
class Particle {
    constructor(x, y, radius, color, energy) {
        this.x = x;
        this.y = y;
        this.radius = radius;
        this.color = color;
        this.energy = energy;
        this.volume = (4 / 3) * Math.PI * radius ** 3;
        this.mass = this.volume * density;
        this.velocity = Math.sqrt(energy / this.mass); 
        const angle = Math.random() * 2 * Math.PI;
        this.dx = this.velocity * Math.cos(angle);
        this.dy = this.velocity * Math.sin(angle);
    }

    update() {
        this.x += this.dx;
        this.y += this.dy;
        this.dy += gravity;
    }

    draw() {
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, 2 * Math.PI);
        ctx.fill();
    }
}

let particles = [];

// Create explosion with sound and particles
function createExplosion(pos, soundFile, colors) {
    const explosionEnergy = 275000;
    const numParticles = 100;
    const particleEnergy = explosionEnergy / numParticles;
  
    const sound = new Audio(soundFile);
    sound.play();
  
    for (let i = 0; i < numParticles; i++) {
        const color = colors[Math.floor(Math.random() * colors.length)];
        const radius = Math.random() * 3 + 2;
        particles.push(new Particle(pos.x, pos.y, radius, color, particleEnergy));
    }
  
    // Calculate damage to the item
    if (item) {
        const damage = calculateDamage(pos, item, explosionType);
        item.hp = Math.max(0, item.hp - damage);
        document.getElementById('item-hp').innerText = item.hp;
    }
}

// Animation loop to draw particles and item
function animate() {
    requestAnimationFrame(animate);
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles = particles.filter(p => p.y > 0);
    
    for (const particle of particles) {
        particle.update();
        particle.draw();
    }
    
    if (item) {
        item.draw(); // Draw the item if it exists
    }
}

// Event listeners for explosions
canvas.addEventListener('mousedown', (event) => {
    let colors, soundFile;
    if (explosionType === 1) {
        colors = [document.getElementById('color-picker1').value,
                  document.getElementById('color-picker2').value,
                  document.getElementById('color-picker3').value,
                  document.getElementById('color-picker4').value];
        soundFile = 'explosion.wav';
    } else {
        colors = [document.getElementById('color-picker5').value,
                  document.getElementById('color-picker6').value,
                  document.getElementById('color-picker7').value,
                  document.getElementById('color-picker8').value];
        soundFile = 'explosion_2.mp3';
    }
    
    if (event.button === 0) {
        createExplosion({ x: event.clientX, y: event.clientY }, soundFile, colors);
    }
});

animate(); // Start the animation loop