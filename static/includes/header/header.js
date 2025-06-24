document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const highContrastBtn = document.getElementById('highContrastBtn');
    const fontIncreaseBtn = document.getElementById('fontIncreaseBtn');
    const fontDecreaseBtn = document.getElementById('fontDecreaseBtn');
    const fontResetBtn = document.getElementById('fontResetBtn');
    const dyslexicFontBtn = document.getElementById('dyslexicFontBtn');
    const underlineLinksBtn = document.getElementById('underlineLinksBtn');
    const body = document.body;
    const root = document.documentElement;
    const mainContent = document.querySelector('main');

    // Load saved settings
    loadSettings();

    // Event Listeners
    highContrastBtn.addEventListener('click', toggleHighContrast);
    fontIncreaseBtn.addEventListener('click', () => changeFontSize(1));
    fontDecreaseBtn.addEventListener('click', () => changeFontSize(-1));
    fontResetBtn.addEventListener('click', resetFontSize);
    dyslexicFontBtn.addEventListener('click', toggleDyslexicFont);
    underlineLinksBtn.addEventListener('click', toggleUnderlineMode);

    // Functions
    function loadSettings() {
        if (localStorage.getItem('highContrast') === 'true') {
            body.classList.add('high-contrast');
            document.documentElement.style.backgroundColor = "#000";
            if (mainContent) mainContent.style.background = "#000";
        }
        if (localStorage.getItem('dyslexicFont') === 'true') {
            body.classList.add('dyslexic-font');
        }
        if (localStorage.getItem('fontSize')) {
            root.style.fontSize = localStorage.getItem('fontSize');
        }
        if (localStorage.getItem('underlineMode') === 'true') {
            body.classList.add('underline-mode');
            underlineLinksBtn.classList.add('active');
        }
    }

    function toggleHighContrast() {
        body.classList.toggle('high-contrast');
        highContrastBtn.classList.toggle('active');

        if (body.classList.contains('high-contrast')) {
            document.documentElement.style.backgroundColor = "#000";
            if (mainContent) mainContent.style.background = "#000";
            // Force header and footer colors
            document.querySelector('header').style.color = "yellow";
            if (document.querySelector('footer')) {
                document.querySelector('footer').style.color = "yellow";
            }
        } else {
            document.documentElement.style.backgroundColor = "";
            if (mainContent) mainContent.style.background = "";
            // Reset header and footer colors
            document.querySelector('header').style.color = "";
            if (document.querySelector('footer')) {
                document.querySelector('footer').style.color = "";
            }
        }

        localStorage.setItem('highContrast', body.classList.contains('high-contrast'));
    }

    function changeFontSize(direction) {
        const currentSize = parseFloat(getComputedStyle(root).fontSize);
        let newSize = direction > 0 ? currentSize * 1.2 : currentSize * 0.8;
        newSize = Math.min(Math.max(newSize, 12), 24);
        root.style.fontSize = `${newSize}px`;
        localStorage.setItem('fontSize', `${newSize}px`);
    }

    function resetFontSize() {
        root.style.fontSize = '';
        localStorage.removeItem('fontSize');
    }

    function toggleDyslexicFont() {
        body.classList.toggle('dyslexic-font');
        dyslexicFontBtn.classList.toggle('active');
        localStorage.setItem('dyslexicFont', body.classList.contains('dyslexic-font'));
    }

    function toggleUnderlineMode() {
        body.classList.toggle('underline-mode');
        underlineLinksBtn.classList.toggle('active');
        localStorage.setItem('underlineMode', body.classList.contains('underline-mode'));
    }
});