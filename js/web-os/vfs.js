export class VirtualFileSystem {
    constructor() {
        this.files = {
            '/welcome.txt': 'Welcome to LibreHub Virtual File System!\nAll files are stored in browser memory.',
            '/notes.md': '# Developer Notes\n- Keep repos modular\n- Stay under 1GB limit'
        };
    }

    list() {
        return Object.keys(this.files);
    }

    read(path) {
        return this.files[path] || 'File not found.';
    }

    write(path, content) {
        this.files[path] = content;
        return `Successfully wrote to ${path}`;
    }
}
