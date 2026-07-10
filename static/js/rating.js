document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll(".rating").forEach(function (container) {

        const fieldName = container.dataset.name;
        const hiddenInput = document.getElementById(fieldName);

        for (let i = 1; i <= 5; i++) {

            const star = document.createElement("span");

            star.innerHTML = "★";
            star.dataset.value = i;

            container.appendChild(star);
        }

        const stars = container.querySelectorAll("span");

        stars.forEach(function (star) {

            star.addEventListener("click", function () {

                if (hiddenInput) {
                    hiddenInput.value = this.dataset.value;
                }

                stars.forEach(function (s) {
                    s.style.color = "#d3d3d3";
                });

                for (let i = 0; i < Number(this.dataset.value); i++) {
                    stars[i].style.color = "gold";
                }

        });
        });

    });

});