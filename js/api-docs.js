export function initApiDocs() {
    const container = document.getElementById('hitl-queue-container');
    if (!container) return;

    const mockQueue = [
        { id: 'req_01', task: 'Deploy autonomous agent script', status: 'Pending Approval' },
        { id: 'req_02', task: 'Modify Virtual File System root', status: 'Pending Approval' }
    ];

    function render() {
        container.innerHTML = `
            <h4>Human-in-the-Loop Active Queue</h4>
            <div style="margin-top: 1rem; display: flex; flex-direction: column; gap: 0.75rem;">
                ${mockQueue.map(item => `
                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.75rem; background: var(--bg-primary); border-radius: 6px; border: 1px solid var(--border);">
                        <span><strong>[${item.id}]</strong>${item.task} — <em>${item.status}</em></span>${item.status === 'Pending Approval' ? `<button data-id="${item.id}" class="nav-btn approve-btn" style="padding: 0.25rem 0.5rem; font-size:0.8rem;">Approve</button>` : '<span style="color: #38bdf8;">Approved ✓</span>'}
                    </div>
                `).join('')}
            </div>
        `;

        container.querySelectorAll('.approve-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const id = e.target.dataset.id;
                const req = mockQueue.find(r => r.id === id);
                if (req) req.status = 'Approved';
                render();
            });
        });
    }

    render();
}
