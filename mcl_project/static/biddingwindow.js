var mySocket = new WebSocket("ws://" + window.location.host + "/ws/ac/");

// ===============================
// RECEIVE BROADCAST DATA HERE
// ===============================

mySocket.onmessage = function(event) {
    let data = JSON.parse(event.data);

    // Update UI
    document.getElementById("live-bid").innerHTML = `
        <div class="text-center">
            <span class="d-block mb-2 text-warning">CURRENT BID: ₹${data.current_bid}</span>
            <span class="d-block text-white">PLAYER: ${data.player_id}</span>
            <span class="d-block text-danger mt-2">TEAM: ${data.team_name}</span>
        </div>
    `;
};
