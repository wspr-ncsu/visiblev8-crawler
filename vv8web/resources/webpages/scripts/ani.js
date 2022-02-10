let progressValue = 0;
const progressBar = document.querySelector(".current-progress");

progressBar.style.width = `${progressValue}%`;

const timer = setInterval(() => {
    if (progressValue < 100) {
        progressValue += 10;
        progressBar.style.width = `${progressValue}%`;

    }
    if (progressValue === 100) {
        clearInterval(timer);
    }
}, 1000);