class AuthFormSwitcher {
    constructor() {
        this.loginForm = document.querySelector('.login-form');
        this.registerForm = document.querySelector('.register-form');
        this.toRegister = document.getElementById('toRegister');
        this.toLogin = document.getElementById('toLogin');

        this.init();
    }

    init() {
        if (this.toRegister) {
            this.toRegister.addEventListener('click', (event) => this.switchToRegister(event));
        }
        if (this.toLogin) {
            this.toLogin.addEventListener('click', (event) => this.switchToLogin(event));
        }
    }

    switchToRegister(event) {
        if (event) {
            event.preventDefault();
        }
        if (this.loginForm && this.registerForm) {
            this.loginForm.style.display = 'none';
            this.registerForm.style.display = 'flex';
        }
    }

    switchToLogin(event) {
        if (event) {
            event.preventDefault();
        }
        if (this.loginForm && this.registerForm) {
            this.registerForm.style.display = 'none';
            this.loginForm.style.display = 'flex';
        }
    }
}

document.addEventListener('DOMContentLoaded', () => new AuthFormSwitcher());