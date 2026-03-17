/* AI Work Generator Framework - JavaScript */

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Navbar scroll effect
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.background = 'rgba(7, 17, 31, 0.98)';
        navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.5)';
    } else {
        navbar.style.background = 'rgba(7, 17, 31, 0.95)';
        navbar.style.boxShadow = 'none';
    }
});

// Animate elements on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe feature cards, doc cards, and example cards
document.querySelectorAll('.feature-card, .doc-card, .example-card, .step').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

// Copy code blocks on click
document.querySelectorAll('.code-block pre').forEach(codeBlock => {
    codeBlock.addEventListener('click', () => {
        const code = codeBlock.textContent;
        navigator.clipboard.writeText(code).then(() => {
            // Show feedback
            const originalBg = codeBlock.style.background;
            codeBlock.style.background = 'rgba(139, 232, 168, 0.2)';
            setTimeout(() => {
                codeBlock.style.background = originalBg;
            }, 1000);
        }).catch(err => {
            console.error('Failed to copy:', err);
        });
    });
    codeBlock.style.cursor = 'pointer';
    codeBlock.title = 'Click to copy';
});

// Terminal typing animation (optional enhancement)
function typeTerminalText() {
    const terminalBody = document.querySelector('.terminal-body pre code');
    if (!terminalBody) return;

    const text = terminalBody.innerHTML;
    terminalBody.innerHTML = '';
    
    let i = 0;
    const typeInterval = setInterval(() => {
        if (i < text.length) {
            terminalBody.innerHTML += text.charAt(i);
            i++;
        } else {
            clearInterval(typeInterval);
        }
    }, 10);
}

// Run terminal animation on page load
window.addEventListener('load', typeTerminalText);

// Mobile menu toggle (if needed in future)
function toggleMobileMenu() {
    const navLinks = document.querySelector('.nav-links');
    navLinks.classList.toggle('active');
}

// Console welcome message
console.log('%c🚀 GitHub Work Generator', 'font-size: 20px; font-weight: bold; color: #6be8ff;');
console.log('%cAI-powered automation for GitHub projects', 'font-size: 12px; color: #8da2c9;');
console.log('%cLearn more: https://github.com/vkumar-dev/github-work-generator', 'font-size: 10px; color: #5f749d;');

// Copy implementation prompt
function copyPrompt() {
    const promptContent = document.getElementById('implementation-prompt');
    const success = document.getElementById('copy-success');
    const copyBtn = document.querySelector('.copy-button');
    const copyLabel = copyBtn.querySelector('.copy-label');
    
    navigator.clipboard.writeText(promptContent.textContent.trim()).then(() => {
        // Show success message
        success.classList.add('show');
        copyLabel.textContent = 'Copied!';
        
        setTimeout(() => {
            success.classList.remove('show');
            copyLabel.textContent = 'Copy Prompt';
        }, 2500);
    }).catch(err => {
        console.error('Failed to copy:', err);
        success.innerHTML = '<span>✗ Failed to copy</span>';
        success.classList.add('show');
        setTimeout(() => {
            success.classList.remove('show');
        }, 2500);
    });
}

// Toggle manual implementation section
function toggleManual() {
    const manualSection = document.getElementById('manual-section');
    const chevron = document.querySelector('.toggle-chevron');
    
    if (manualSection.style.display === 'none') {
        manualSection.style.display = 'block';
        chevron.style.transform = 'rotate(180deg)';
    } else {
        manualSection.style.display = 'none';
        chevron.style.transform = 'rotate(0deg)';
    }
}
