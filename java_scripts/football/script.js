const LEAGUES = [
    { id: 1, name: 'English Premier League' },
    { id: 2, name: 'Spanish La Liga' },
    { id: 3, name: 'German Bundesliga' },
    // Add more leagues as needed
];

const PROXY_URL = 'http://localhost:3000/api'; // Update this to your proxy server URL
const API_KEY = '4yW4jorJiaeP38MGImkZaMrAGhNI6pu8Gidn0zxueDvDHtOg0B78ojT5uOXN'; // Replace with your actual API key

const leagueSelect = document.getElementById('league-select');
const scoresContainer = document.querySelector('.scores-container');

// Populate league select dropdown
LEAGUES.forEach((league) => {
    const option = document.createElement('option');
    option.value = league.id;
    option.textContent = league.name;
    leagueSelect.appendChild(option);
});

// Handle league selection change
leagueSelect.addEventListener('change', async () => {
    const selectedLeagueId = parseInt(leagueSelect.value);
    const response = await fetch(`${PROXY_URL}/leagues/${selectedLeagueId}/livescores`);
    const data = await response.json();
    const scoresHtml = data.data.map((match) => {
        return `
            <div class="score-item">
                <span class="team-name">${match.localTeam.data.name}</span>
                <span class="score">${match.scores.localteam_score} - ${match.scores.visitorteam_score}</span>
                <span class="team-name">${match.visitorTeam.data.name}</span>
            </div>
        `;
    }).join('');
    scoresContainer.innerHTML = scoresHtml;
});

// Initialize app
async function init() {
    const response = await fetch(`${PROXY_URL}/leagues`);
    const data = await response.json();
    const firstLeagueId = data.data[0].id;
    leagueSelect.value = firstLeagueId;
    leagueSelect.dispatchEvent(new Event('change'));
}

init();