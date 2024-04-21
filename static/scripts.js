function loadParks(groupId) {
    const url = `/get-parks/${groupId}`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const parksContainer = document.getElementById(`group-${groupId}`);
            parksContainer.style.display = 'block';
            parksContainer.innerHTML = '';
            data.park_groups.forEach(park => {
                const parkLink = document.createElement('a');
                parkLink.href = `/park/${park.id}`;
                parkLink.textContent = park.name;
                parksContainer.appendChild(parkLink);
                parksContainer.appendChild(document.createElement('br'));  
            });
        })
}