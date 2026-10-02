export function initCryptoHasher() {
    const fileInput = document.getElementById('crypto-file-input');
    const outputBox = document.getElementById('crypto-output');

    if (!fileInput) return;

    fileInput.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        outputBox.textContent = `Computing SHA-256 for ${file.name}...`;
        try {
            const buffer = await file.arrayBuffer();
            const hashBuffer = await crypto.subtle.digest('SHA-256', buffer);
            const hashArray = Array.from(new Uint8Array(hashBuffer));
            const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
            outputBox.textContent = `SHA-256: ${hashHex}`;
        } catch (err) {
            outputBox.textContent = `Error hashing file: ${err.message}`;
        }
    });
}
