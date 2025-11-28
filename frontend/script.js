const ticketForm = document.getElementById("ticketForm");
const openList = document.getElementById("open-tickets");
const inProgressList = document.getElementById("in-progress-tickets");
const doneList = document.getElementById("done-tickets");

// Fetch tickets from backend
async function fetchTickets() {
    const response = await fetch("/tickets");
    const tickets = await response.json();

    // Clear lists
    openList.innerHTML = "";
    inProgressList.innerHTML = "";
    doneList.innerHTML = "";

    tickets.forEach(ticket => {
        const li = document.createElement("li");
        li.classList.add("ticket");
        li.innerHTML = `
            <strong>${ticket.title}</strong> (${ticket.category})<br>
            ${ticket.description}<br>
            Status:
            <select class="status-dropdown" data-id="${ticket.id}">
                <option value="open" ${ticket.status === 'open' ? 'selected' : ''}>Open</option>
                <option value="in-progress" ${ticket.status === 'in-progress' ? 'selected' : ''}>In Progress</option>
                <option value="done" ${ticket.status === 'done' ? 'selected' : ''}>Done</option>
            </select>
        `;

        const dropdown = li.querySelector(".status-dropdown");
        dropdown.addEventListener("change", async (e) => {
            await updateStatus(ticket.id, e.target.value);
            fetchTickets();
        });

        if(ticket.status === "open") openList.appendChild(li);
        else if(ticket.status === "in-progress") inProgressList.appendChild(li);
        else if(ticket.status === "done") doneList.appendChild(li);
    });
}

// Submit new ticket
ticketForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const newTicket = {
        title: document.getElementById("title").value,
        description: document.getElementById("description").value,
        category: document.getElementById("category").value
    };

    await fetch("/tickets", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newTicket)
    });

    ticketForm.reset();
    fetchTickets();
});

// Update ticket status
async function updateStatus(id, status) {
    await fetch(`/tickets/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status })
    });
}

// Load tickets on page load
fetchTickets();
