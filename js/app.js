import { initCryptoHasher } from './crypto-utils.js';
import { initApiDocs } from './api-docs.js';
import { initWebOS } from './web-os/window-manager.js';

document.addEventListener('DOMContentLoaded', () => {
    // Tab Navigation Router
    const navButtons = document.querySelectorAll('.nav-btn');
    const tabs = document.querySelectorAll('.tab-content');

    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            navButtons.forEach(b => b.classList.remove('active'));
            tabs.forEach(t => t.classList.remove('active'));
            
            btn.classList.add('active');
            const target = document.getElementById(`tab-${btn.dataset.tab}`);
            if (target) target.classList.add('active');
        });
    });

    // Theme Toggle
    const themeToggle = document.getElementById('theme-toggle');
    themeToggle.addEventListener('click', () => {
        const html = document.documentElement;
        const currentTheme = html.getAttribute('data-theme');
        html.setAttribute('data-theme', currentTheme === 'dark' ? 'light' : 'dark');
    });

    // Initialize Sub-Modules
    initCryptoHasher();
    initApiDocs();
    initWebOS();
});
