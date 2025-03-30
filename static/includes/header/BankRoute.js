class BankRoute {
    constructor() {
        this.homeButton = document.getElementById("homeButton");
        this.loginButton = document.getElementById("loginButton");
        this.servicesButton = document.getElementById("servicesButton");
        this.aboutButton = document.getElementById("aboutButton");

        this.init();
    }

    init() {
        if (this.homeButton) {
            this.homeButton.addEventListener("click", () => this.redirectTo('/'));
        }
        if (this.loginButton) {
            this.loginButton.addEventListener("click", () => this.redirectTo('/login'));
        }
        if (this.servicesButton) {
            this.servicesButton.addEventListener("click", () => this.redirectTo('/services'));
        }
        if (this.aboutButton) {
            this.aboutButton.addEventListener("click", () => this.redirectTo('/about'));
        }
    }

    redirectTo(pageUrl) {
        window.location.href = pageUrl;
    }
}

document.addEventListener("DOMContentLoaded", () => new BankRoute());