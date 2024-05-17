const gameBoard = document.getElementById('game-board');
const restartBtn = document.getElementById('restart-btn');
const leaderboardBtn = document.getElementById('leaderboard-btn');
const leaderboardContainer = document.getElementById('leaderboard-container');

let cards = [];
let flippedCards = [];
let matchedCards = [];
let clickCount = 0;
let startTime = null;

function createCard(id) {
    const card = document.createElement('div');
    card.classList.add('card');
    card.dataset.id = id;

    // Add a unique image to each pair of cards
    const image = document.createElement('img');
    image.src = `images/${id}.png`; // assumes images are named 0.png, 1.png, etc.
    image.alt = `Image ${id}`;
    image.style.display = 'none'; // hide the image initially
    card.appendChild(image);

    card.addEventListener('click', flipCard);
    return card;
}

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

function startGame() {
    cards = [];
    flippedCards = [];
    matchedCards = [];
    clickCount = 0;
    startTime = new Date().getTime();

    for (let i = 0; i < 10; i++) {
        cards.push(createCard(i));
        cards.push(createCard(i));
    }

    cards = shuffleArray(cards);

    cards.forEach(card => {
        gameBoard.appendChild(card);
    });
}

function flipCard(event) {
    const card = event.target;

    if (card.classList.contains('flipped') || card.classList.contains('matched')) {
        return;
    }

    clickCount++;
    card.classList.add('flipped');
    card.querySelector('img').style.display = 'block'; // show the image when card is flipped
    flippedCards.push(card);

    if (flippedCards.length === 2) {
        checkMatch();
    }
}

function checkMatch() {
    const card1 = flippedCards[0];
    const card2 = flippedCards[1];

    if (card1.dataset.id === card2.dataset.id) {
        card1.classList.add('matched');
        card2.classList.add('matched');
        matchedCards.push(card1, card2);
    } else {
        setTimeout(() => {
            card1.classList.remove('flipped');
            card2.classList.remove('flipped');
            card1.querySelector('img').style.display = 'none'; // hide the image again
            card2.querySelector('img').style.display = 'none';
        }, 1000);
    }

    flippedCards = [];

    if (matchedCards.length === cards.length) {
        const endTime = new Date().getTime();
        const timeTaken = (endTime - startTime) / 1000;
        const score = calculateScore(clickCount, timeTaken);
        updateLeaderboard(score);
        alert(`Congratulations! You have won the game in ${timeTaken} seconds with ${clickCount} clicks. Your score is ${score}.`);
    }
}

function calculateScore(clickCount, timeTaken) {
    return Math.round(100000 / (clickCount * timeTaken));
}

function updateLeaderboard(score) {
    const leaderboard = JSON.parse(localStorage.getItem('leaderboard')) || [];
    leaderboard.push({ score, date: new Date().toLocaleString() });
    leaderboard.sort((a, b) => b.score - a.score);
    localStorage.setItem('leaderboard', JSON.stringify(leaderboard));
}

startGame();

restartBtn.addEventListener('click', () => {
    gameBoard.innerHTML = '';
    startGame();
});

leaderboardBtn.addEventListener('click', () => {
    const leaderboard = JSON.parse(localStorage.getItem('leaderboard'));
    if (leaderboard) {
        leaderboardContainer.innerHTML = '';
        leaderboard.forEach(entry => {
            const entryElement = document.createElement('p');
            entryElement.textContent = `${entry.date} - Score: ${entry.score}`;
            leaderboardContainer.appendChild(entryElement);
        });
    } else {
        leaderboardContainer.textContent = 'No scores yet!';
    }
});