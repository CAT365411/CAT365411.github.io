import { initTerminal } from './terminal.js';

export function initWebOS() {
    const workspace = document.getElementById('desktop-workspace');
    if (!workspace) return;

    function createWindow(title, contentBuilder) {
        const win = document.createElement('div');
        win.className = 'os-window';
        win.style.top = `${50 + workspace.children.length * 30}px`;
        win.style.left = `${50 + workspace.children.length * 30}px`;

        win.innerHTML = `
            <div class="window-header">
                <span>${title}</span>
                <div class="window-controls">
                    <button class="win-btn win-minimize"></button>
                    <button class="win-btn win-close"></button>
                </div>
            </div>
            <div class="window-body"></div>
        `;

        workspace.appendChild(win);
        contentBuilder(win.querySelector('.window-body'));

        // Close window
        win.querySelector('.win-close').addEventListener('click', () => win.remove());

        // Simple Dragging Logic
        const header = win.querySelector('.window-header');
        let isDragging = false, startX, startY;

        header.addEventListener('mousedown', (e) => {
            isDragging = true;
            startX = e.clientX - win.offsetLeft;
            startY = e.clientY - win.offsetTop;
            win.style.zIndex = 10;
        });

        document.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            win.style.left = `${e.clientX - startX}px`;
            win.style.top = `${e.clientY - startY}px`;
        });

        document.addEventListener('mouseup', () => isDragging = false);
    }

    // Auto-launch initial terminal window on Web OS tab load
    createWindow('Retro Terminal Shell', (body) => initTerminal(body));

    // Start menu binding
    document.getElementById('start-menu-btn')?.addEventListener('click', () => {
        createWindow('Terminal Shell (New)', (body) => initTerminal(body));
    });
}
