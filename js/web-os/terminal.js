import { VirtualFileSystem } from './vfs.js';

export function initTerminal(container) {
    const vfs = new VirtualFileSystem();
    
    container.innerHTML = `
        <div class="terminal-output" style="height: 200px; overflow-y: auto; margin-bottom: 0.5rem; white-space: pre-wrap;">LibreHub Shell v1.0.0 (x86_64-browser)
Type 'help' to see available commands.
</div>
        <div style="display: flex; gap: 0.5rem;">
            <span style="color: var(--accent);">&gt;</span>
            <input type="text" class="terminal-input" style="flex: 1; background: transparent; border: none; color: var(--text-primary); font-family: var(--font-mono); outline: none;" autofocus>
        </div>
    `;

    const output = container.querySelector('.terminal-output');
    const input = container.querySelector('.terminal-input');

    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            const cmd = input.value.trim();
            output.textContent += `\n> ${cmd}\n`;
            
            const parts = cmd.split(' ');
            if (parts[0] === 'help') {
                output.textContent += `Available commands: help, ls, cat <file>, clear, matrix`;
            } else if (parts[0] === 'ls') {
                output.textContent += vfs.list().join('\n');
            } else if (parts[0] === 'cat') {
                output.textContent += vfs.read(parts[1]);
            } else if (parts[0] === 'clear') {
                output.textContent = '';
            } else if (parts[0] === 'matrix') {
                output.textContent += `Wake up, Neo...\nThe matrix has you.`;
            } else if (cmd !== '') {
                output.textContent += `Command not found: ${parts[0]}`;
            }

            input.value = '';
            output.scrollTop = output.scrollHeight;
        }
    });
}
