document.addEventListener("DOMContentLoaded", function () {
    const tableBody = document.querySelector("tbody");

    // Function to fetch tasks and populate the table
    async function fetchTasks() {
        const token = localStorage.getItem('access');
        try {
            const response = await fetch("/adminapp/api/tasks/", {
                method: "GET",
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
        
                },
            });
            console.log(response)
            if (!response.ok) {
                throw new Error("Failed to fetch tasks.");
            }

            const tasks = await response.json();

            // Clear the table before adding new rows
            tableBody.innerHTML = "";

            // Populate the table with tasks
            tasks.forEach((task) => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${task.app_name}</td>
                    <td>${task.username}</td>
                    <td>
                        <a href="${task.screenshot}" target="_blank">View Screenshot</a>
                    </td>
                    <td>
                        <button class="btn btn-success btn-sm accept-btn" data-id="${task.id}">Accept</button>
                        <button class="btn btn-danger btn-sm reject-btn" data-id="${task.id}">Reject</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });

            // Add event listeners to the action buttons
            addActionListeners();
        } catch (error) {
            console.error("Error fetching tasks:", error);
        }
    }

    // Function to handle task status update
    async function updateTaskStatus(taskId, status) {
        const token = localStorage.getItem('access');
        try {
            const response = await fetch(`/adminapp/api/tasks/${taskId}/`, {
                method: "PUT",
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ status }),
            });

            if (!response.ok) {
                throw new Error("Failed to update task status.");
            }

            // Fetch and refresh the task list after updating
            await fetchTasks();
        } catch (error) {
            console.error("Error updating task status:", error);
        }
    }

    // Function to add event listeners to Accept and Reject buttons
    function addActionListeners() {
        const acceptButtons = document.querySelectorAll(".accept-btn");
        const rejectButtons = document.querySelectorAll(".reject-btn");

        acceptButtons.forEach((button) => {
            button.addEventListener("click", function () {
                const taskId = this.getAttribute("data-id");
                updateTaskStatus(taskId, "Completed");
            });
        });

        rejectButtons.forEach((button) => {
            button.addEventListener("click", function () {
                const taskId = this.getAttribute("data-id");
                updateTaskStatus(taskId, "Rejected");
            });
        });
    }

    // Fetch tasks on page load
    fetchTasks();
});
