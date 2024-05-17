const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth * 0.8;
canvas.height = window.innerHeight;

// Variables for simulation
let explosionEnergy = 275000;
let density = 1;
let explosionType = 1;
let gravity = 0.08;

// Define global array for particles
let particles = [];

// Particle class for creating explosion effects
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

// Item class with a health bar for visual representation
class Item {
    constructor(x, y, hp = 100, width = 50, height = 50) {
        this.x = x;
        this.y = y;
        this.hp = hp;
        this.width = width;
        this.height = height;
    }

    draw() {
        ctx.fillStyle = this.color; // Use the item's color
        ctx.fillRect(this.x - this.width / 2, this.y - this.height / 2, this.width, this.height);

        // Draw a health bar
        const healthBarWidth = 50;
        const healthBarHeight = 10;
        ctx.fillStyle = "white";
        ctx.fillRect(
            this.x - healthBarWidth / 2,
            this.y - this.height / 2 - healthBarHeight,
            healthBarWidth,
            healthBarHeight
        );
        ctx.fillStyle = "red";
        ctx.fillRect(
            this.x - healthBarWidth / 2,
            this.y - this.height / 2 - healthBarHeight,
            healthBarWidth * (this.hp / 100),
            healthBarHeight
        );
    }
}

// Function to calculate damage based on explosion type
function calculateDamage(explosionPos, itemPos, type) {
    const distance = Math.abs(explosionPos.x - itemPos.x);
    let damage;

    if (type === 1) {
        damage = Math.max(0, (explosionEnergy / 10000) * (100 - (distance / 10)));
    } else {
        damage = Math.max(0, (explosionEnergy / 10000) * (200 - (distance / 5)));
    }

    return damage;
}

// Global variable for item
let item;

// Function to create an item at a specified position
function addItem(x) {
    item = new Item(x * canvas.width / 100, canvas.height / 2);
}

// Call addItem to create an initial item
addItem(50);

// Event listener for item size adjustment
document.getElementById('item-size-slider').addEventListener('input', (e) => {
    const size = parseInt(e.target.value, 10);
    item.width = size;
    item.height = size;
});

// Event listener for item type selection
document.getElementById('item-type-select').addEventListener('change', (e) => {
    const itemType = e.target.value;
    if (itemType === 'type-1') {
        item.hp = 100;
        item.width = 50;
        item.height = 50;
    } else if (itemType === 'type-2') {
        item.hp = 200;
        item.width = 75;
        item.height = 75;
    }
});

// Allow item to be moved based on mouse clicks
canvas.addEventListener('mousedown', (event) => {
    if (event.button === 0) {
        const rect = canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        if (item) {
            item.x = x;
            item.y = y;
        }
    }
});

// Explosion creation with sound and particles
function createExplosion(pos, soundFile, colors, volume) {
    const numParticles = 100;
    const particleEnergy = explosionEnergy / numParticles;

    const sound = new Audio(soundFile);
    sound.volume = volume;
    sound.play();

    if (item && item.hp > 0) {
        const damageSound = new Audio('damage.wav');
        damageSound.volume = volume;
        damageSound.play();
    }

    for (let i = 0; i < numParticles; i++) {
        const color = colors[Math.floor(Math.random() * colors.length)];
        const radius = Math.random() * 3 + 2;
        particles.push(new Particle(pos.x, pos.y, radius, color, particleEnergy));
    }

    if (item) {
        const damage = calculateDamage(pos, item, explosionType);
        item.hp = Math.max(0, item.hp - damage);
        document.getElementById('item-hp').innerText = item.hp;
    }
}

// Animation loop to draw particles and item, and display position
function animate() {
    requestAnimationFrame(animate);
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    particles = particles.filter(p => p.y > 0);
    for (const particle of particles) {
        particle.update();
        particle.draw();
    }

    if (item) {
        item.draw();
        ctx.fillStyle = "white";
        ctx.font = "16px Arial";
        ctx.textAlign = "left";
        ctx.textBaseline = "top";
        ctx.fillText(`Item Position: (${item.x}, ${item.y})`, 10, 10);
    }
}

// Reset button for resetting the item's position and HP
document.getElementById('reset-button').addEventListener('click', () => {
    item.x = canvas.width / 2;
    item.y = canvas.height / 2;
    item.hp = 100;
});

// Get the color picker input
const itemColorPicker = document.getElementById('item-color-picker');

// Add an event listener to the color picker input
itemColorPicker.addEventListener('input', (e) => {
    // Update the item's color
    item.color = e.target.value;
});

canvas.addEventListener('mousedown', (event) => {
    if (event.button === 2) { // Right mouse button
        const volume = parseFloat(document.getElementById('volume-slider').value);
        let colors, soundFile;
        if (explosionType === 1) {
            colors = [
                document.getElementById('color-picker1').value,
                document.getElementById('color-picker2').value,
                document.getElementById('color-picker3').value,
                document.getElementById('color-picker4').value,
            ];
            soundFile = 'explosion.wav';
        } else {
            colors = [
                document.getElementById('color-picker5').value,
                document.getElementById('color-picker6').value,
                document.getElementById('color-picker7').value,
                document.getElementById('color-picker8').value,
            ];
            soundFile = 'explosion_2.mp3';
        }
        
        createExplosion({ x: event.clientX, y: event.clientY }, soundFile, colors, volume);
    }
});

// Volume control for sound effects
document.getElementById('volume-slider').addEventListener('input', (e) => {
    const volume = parseFloat(e.target.value);
    document.getElementById('volume-value').innerText = volume.toFixed(2);

    const audioElements = document.querySelectorAll('audio');
    for (const audio of audioElements) {
        audio.volume = volume;
    }
});

// Start the animation loop
animate();
