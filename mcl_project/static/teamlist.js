document.addEventListener('DOMContentLoaded', function() {
    const teamSelector = document.getElementById('team-selector');
    const teamLogoImg = document.getElementById('team-logo-display');
    // const teamResevedPlayer = document.getElementById('player-list-table');
    
    // IMPORTANT: Define the Django URL endpoint for AJAX
    const AJAX_BASE_URL = '/api/get-team-data/';

    // ----------------------------------------
    // Function to handle the AJAX call and DOM updates
    // ----------------------------------------
    function updateTeamData(teamId) {
        if (!teamId) return;

        // 1. Show Loading State (Optional: Add spinner/loading class here)
        teamLogoImg.src = ''; // Clear image
        teamLogoImg.alt = 'Loading...';
        // pointsBox.textContent = 'Pts Remain : Loading...'; 

        // 2. Fetch Data (AJAX) using the selected ID
        fetch(`${AJAX_BASE_URL}${teamId}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log("Received data:", data);

                // 3. Update the Logo's src attribute
                if (data.team_logo_url) {
                    teamLogoImg.src = data.team_logo_url;
                    teamLogoImg.alt = data.team_name || 'Team Logo';
                } else {
                    // Fallback if no URL is returned
                    teamLogoImg.src = ''; 
                    teamLogoImg.alt = 'Logo Not Available';
                }

                // 4. Update other dynamic sections
                // pointsBox.textContent = `Pts Remain : $ ${data.remaining_points || 'N/A'}`;
                // updatePlayerList(data.players, playerTableBody);
                // updateManagerList(data.managers, managerList);
            })
            .catch(error => {
                console.error('Error fetching team data:', error);
                teamLogoImg.alt = 'Error fetching data.';
                // Optional: Display error message on other elements
            });
    }

    // ----------------------------------------
    // 💥 NEW: Initial State Setup
    // ----------------------------------------
    // Get the initial selected value from the dropdown. 
    // This value is set by the server-side template (Django/Jinja).
    const initialSelectedValue = teamSelector.value;
    
    // Call the data update function immediately on load
    updateTeamData(initialSelectedValue);

    // ----------------------------------------
    // Event Listener: Fires when the dropdown changes
    // ----------------------------------------
    teamSelector.addEventListener('change', function() {
        const selectedValue = this.value;
        updateTeamData(selectedValue);
    });
});
