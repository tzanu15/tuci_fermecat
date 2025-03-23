document.addEventListener("DOMContentLoaded", () => {
    const voteButtons = document.querySelectorAll(".btn-vote");

    voteButtons.forEach(button => {
        button.addEventListener("click", () => {
            const dishId = button.getAttribute("data-dish-id");

            fetch("/vote/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: `dish_id=${dishId}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    updateVoteCount(dishId);
                } else {
                    showModal("Ai votat deja acest preparat!");
                }
            });
        });
    });

    // Countdown Timer
    startCountdownToFriday();

    // Show winner pop-up if voting is over
    checkWinnerPopup();

    // Helper functions
    function getCSRFToken() {
        const cookie = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
        return cookie ? cookie.split('=')[1] : '';
    }

    function updateVoteCount(dishId) {
        const voteCountEl = document.querySelector(`.vote-count[data-dish-id='${dishId}']`);
        const current = parseInt(voteCountEl.textContent.replace(/\D/g, "")) || 0;
        voteCountEl.textContent = `Voturi: ${current + 1}`;
    }

    function showModal(message) {
        const modal = document.createElement("div");
        modal.className = "custom-modal animate__animated animate__fadeInDown";
        modal.innerHTML = `
            <div class="custom-modal-content">
                <p>${message}</p>
            </div>
        `;
        document.body.appendChild(modal);
        setTimeout(() => modal.remove(), 3000);
    }

    function startCountdownToFriday() {
        const container = document.createElement("div");
        container.className = "countdown animate__animated animate__fadeIn";
        document.querySelector("h1").insertAdjacentElement("afterend", container);

        const updateCountdown = () => {
            const now = new Date();
            const nextFriday = new Date(now);
            nextFriday.setDate(now.getDate() + ((5 - now.getDay() + 7) % 7 || 7));
            nextFriday.setHours(23, 59, 59, 999);

            const diff = nextFriday - now;

            if (diff <= 0) {
                container.innerHTML = `<strong>Votul s-a încheiat!</strong>`;
                return;
            }

            const days = Math.floor(diff / (1000 * 60 * 60 * 24));
            const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
            const minutes = Math.floor((diff / (1000 * 60)) % 60);
            const seconds = Math.floor((diff / 1000) % 60);

            container.innerHTML = `
                <div><strong>${days}</strong> zile</div>
                <div><strong>${hours}</strong> ore</div>
                <div><strong>${minutes}</strong> min</div>
                <div><strong>${seconds}</strong> sec</div>
            `;
        };

        updateCountdown();
        setInterval(updateCountdown, 1000);
    }

    function checkWinnerPopup() {
        const now = new Date();
        const isFriday = now.getDay() === 5 && now.getHours() >= 23;

        if (isFriday) {
            fetch("/winner/")
                .then(res => res.json())
                .then(data => {
                    if (data && data.winner) {
                        const modal = document.createElement("div");
                        modal.className = "winner-modal animate__animated animate__fadeInUp";
                        modal.innerHTML = `
                            <div class="winner-content">
                                <h3>🏆 Preparatul câștigător: ${data.winner.name}</h3>
                                <img src="${data.winner.image}" alt="${data.winner.name}" />
                                <p>Au votat:</p>
                                <ul>
                                    ${data.winner.voters.map(u => `<li>${u}</li>`).join('')}
                                </ul>
                            </div>
                        `;
                        document.body.appendChild(modal);
                    }
                });
        }
    }
});
