// =========================
//   REAL-TIME STATES
// =========================
let currentBid = 0;
let currentPlayer = "N/A";
let teamCode = "N/A";
let biddingActive = false;

// =========================
//  WebSocket Setup
// =========================
var mySocket = new WebSocket("ws://" + window.location.host + "/ws/ac/");

mySocket.onopen = function() {
    console.log("WebSocket connected successfully");
};

mySocket.onerror = function() {
    console.log("WebSocket error occurred");
};

mySocket.onclose = function() {
    console.log("WebSocket closed");
};

// Receive updates from backend (GLOBAL)
// mySocket.onmessage = function(event) {
//     let data = JSON.parse(event.data);
//     console.log("Received broadcast:", data);

//     // OPTIONAL: Auto-update UI when server pushes latest bid
//     if (data.current_bid !== undefined) currentBid = data.current_bid;
//     if (data.team_name !== undefined) teamCode = data.team_name;
//     if (data.player_id !== undefined) currentPlayer = data.player_id;

//     renderDisplay();
// };

// =========================
//   SWITCH PANEL
// =========================
let alterN = false;
const rightBox = document.getElementById('right-control-box');

function switcherButton() {
    alterN = !alterN;
    alterN ? loadTeamPanel() : loadIncrementPanel();
}

// -------------------------
//   INCREMENT PANEL
// -------------------------
function loadIncrementPanel() {
    rightBox.innerHTML = `
        <div class="control-card h-100 p-4">
            <div class="row g-3 mb-4">
                <div class="col-6"><button class="btn btn-control btn-time-control" onclick="handleIncrement(5)">+5</button></div>
                <div class="col-6"><button class="btn btn-control btn-time-control" onclick="handleIncrement(10)">+10</button></div>
            </div>
            <div class="row g-3">
                <div class="col-6"><button class="btn btn-increment btn-control" onclick="handleUpdate(50)">50</button></div>
                <div class="col-6"><button class="btn btn-increment btn-control" onclick="handleUpdate(100)">100</button></div>
                <div class="col-6"><button class="btn btn-increment btn-control" onclick="handleUpdate(200)">200</button></div>
                <div class="col-6"><button class="btn btn-increment btn-control" onclick="handleUpdate(300)">300</button></div>
                <div class="col-6"><button class="btn btn-increment btn-control" onclick="handleUpdate(500)">500</button></div>
                <div class="col-6"><button class="btn btn-increment btn-control" onclick="handleUpdate(1000)">1000</button></div>
            </div>
        </div>
    `;
}

// -------------------------
//   TEAM PANEL
// -------------------------
function loadTeamPanel() {
    const teams = ["KKR", "RR", "CSK", "GT", "RCB", "MI", "LSG", "SRH"];
    let buttons = teams.map(t => `
        <div class="col-6"><button class="btn btn-control btn-team" onclick="handleTeam('${t}')">${t}</button></div>
    `).join("");

    rightBox.innerHTML = `
        <div class="control-card h-100 p-4">
            <div class="row g-3 mb-4">
                ${buttons}
            </div>
        </div>
    `;
}

// =========================
//   DISPLAY RENDERER
// =========================
const displayElement = document.getElementById('current-display');

function renderDisplay() {
    if (!biddingActive) {
        displayElement.textContent = "READY: Select Player to Start";
        return;
    }

    displayElement.innerHTML = `
        <div class="text-center">
            <span class="d-block mb-2 text-warning">CURRENT BID: ₹${currentBid}</span>
            <span class="d-block text-white">PLAYER: ${currentPlayer}</span>
            <span class="d-block text-danger mt-2">TEAM NAME: ${teamCode}</span>
        </div>
    `;
}

// =========================
//   HANDLERS
// =========================
function handleIncrement(amount) {
    if (!biddingActive) return alert("Start bidding first!");

    currentBid += amount;
    renderDisplay();
    switcherButton();
}

function handleUpdate(amount) {
    if (!biddingActive) return alert("Start bidding first!");

    currentBid = amount;
    renderDisplay();
    switcherButton();
}

// =======================================
//   SEND DATA TO SERVER ON TEAM SELECTION
// =======================================
function handleTeam(team) {
    if (!biddingActive) return alert("Start bidding first!");

    teamCode = team;
    
    console.log("Sending bid update to server...");
    
    if (mySocket.readyState === WebSocket.OPEN) {
        mySocket.send(JSON.stringify({
            'team_name' : teamCode,
            'current_bid' : currentBid,
            'player_id' : currentPlayer
        }));
    } else {
        console.log("WebSocket not ready:", mySocket.readyState);
    }
    
    renderDisplay();
    switcherButton();
}

// =========================
//   NEXT / SOLD LOGIC
// =========================
function handleAction(action) {
    if (action === "sold") {
        alert(`Player ${currentPlayer} SOLD to ${teamCode} for ₹${currentBid}`);
        currentBid = 0;
        biddingActive = false;
        teamCode = "N/A";
    }

    if (action === "next") {
        currentBid = 0;
        teamCode = "N/A";
        currentPlayer = "P-" + (Math.floor(Math.random() * 900 + 100));
        biddingActive = true;
    }

    renderDisplay();
}

// =========================
//   INITIAL LOAD
// =========================
document.addEventListener("DOMContentLoaded", () => {
    currentPlayer = "P-101";
    biddingActive = true;
    renderDisplay();
    loadIncrementPanel();
});
