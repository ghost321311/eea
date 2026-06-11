// ===== To-Do List Application =====
// Local Storage based task management

class TodoApp {
    constructor() {
        // DOM Elements
        this.taskInput = document.getElementById('taskInput');
        this.addBtn = document.getElementById('addBtn');
        this.tasksList = document.getElementById('tasksList');
        this.emptyState = document.getElementById('emptyState');
        this.clearBtn = document.getElementById('clearBtn');
        this.filterBtns = document.querySelectorAll('.filter-btn');

        // Stats
        this.totalTasksEl = document.getElementById('totalTasks');
        this.completedTasksEl = document.getElementById('completedTasks');
        this.activeTasksEl = document.getElementById('activeTasks');

        // State
        this.tasks = [];
        this.currentFilter = 'all';
        this.storageKey = 'todoApp_tasks';

        // Initialize
        this.init();
    }

    init() {
        // Load tasks from localStorage
        this.loadTasks();

        // Event listeners
        this.addBtn.addEventListener('click', () => this.addTask());
        this.taskInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.addTask();
        });
        this.taskInput.addEventListener('keypress', (e) => {
            if (e.key === 'Escape') this.taskInput.value = '';
        });

        this.clearBtn.addEventListener('click', () => this.clearCompleted());

        this.filterBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.filterBtns.forEach(b => b.classList.remove('active'));
                e.target.closest('.filter-btn').classList.add('active');
                this.currentFilter = e.target.closest('.filter-btn').dataset.filter;
                this.render();
            });
        });

        // Initial render
        this.render();
    }

    // ===== Task Management =====

    addTask() {
        const text = this.taskInput.value.trim();

        if (!text) {
            this.taskInput.focus();
            return;
        }

        const task = {
            id: Date.now(),
            text: text,
            completed: false,
            createdAt: new Date().toISOString()
        };

        this.tasks.unshift(task);
        this.taskInput.value = '';
        this.taskInput.focus();

        this.saveTasks();
        this.render();
    }

    deleteTask(id) {
        this.tasks = this.tasks.filter(task => task.id !== id);
        this.saveTasks();
        this.render();
    }

    toggleComplete(id) {
        const task = this.tasks.find(t => t.id === id);
        if (task) {
            task.completed = !task.completed;
            this.saveTasks();
            this.render();
        }
    }

    clearCompleted() {
        const completedCount = this.tasks.filter(t => t.completed).length;

        if (completedCount === 0) {
            alert('No completed tasks to clear!');
            return;
        }

        if (confirm(`Clear ${completedCount} completed task(s)?`)) {
            this.tasks = this.tasks.filter(task => !task.completed);
            this.saveTasks();
            this.render();
        }
    }

    // ===== Filtering =====

    getFilteredTasks() {
        switch (this.currentFilter) {
            case 'active':
                return this.tasks.filter(t => !t.completed);
            case 'completed':
                return this.tasks.filter(t => t.completed);
            case 'all':
            default:
                return this.tasks;
        }
    }

    // ===== Statistics =====

    updateStats() {
        const total = this.tasks.length;
        const completed = this.tasks.filter(t => t.completed).length;
        const active = total - completed;

        this.totalTasksEl.textContent = total;
        this.completedTasksEl.textContent = completed;
        this.activeTasksEl.textContent = active;
    }

    // ===== Rendering =====

    render() {
        this.updateStats();
        this.renderTasks();
    }

    renderTasks() {
        const filteredTasks = this.getFilteredTasks();

        // Clear list
        this.tasksList.innerHTML = '';

        if (this.tasks.length === 0) {
            this.emptyState.classList.remove('hidden');
            return;
        }

        this.emptyState.classList.add('hidden');

        // Render tasks
        filteredTasks.forEach(task => {
            const li = document.createElement('li');
            li.className = `task-item ${task.completed ? 'completed' : ''}`;

            li.innerHTML = `
                <input 
                    type="checkbox" 
                    class="checkbox" 
                    ${task.completed ? 'checked' : ''}
                    data-id="${task.id}"
                >
                <span class="task-text">${this.escapeHtml(task.text)}</span>
                <button class="delete-btn" data-id="${task.id}">
                    <i class="fas fa-trash"></i>
                </button>
            `;

            // Add event listeners
            const checkbox = li.querySelector('.checkbox');
            checkbox.addEventListener('change', () => this.toggleComplete(task.id));

            const deleteBtn = li.querySelector('.delete-btn');
            deleteBtn.addEventListener('click', () => this.deleteTask(task.id));

            this.tasksList.appendChild(li);
        });
    }

    // ===== Local Storage =====

    saveTasks() {
        try {
            localStorage.setItem(this.storageKey, JSON.stringify(this.tasks));
        } catch (error) {
            console.error('Error saving tasks:', error);
            alert('Failed to save tasks. Storage may be full.');
        }
    }

    loadTasks() {
        try {
            const saved = localStorage.getItem(this.storageKey);
            this.tasks = saved ? JSON.parse(saved) : [];
        } catch (error) {
            console.error('Error loading tasks:', error);
            this.tasks = [];
        }
    }

    // ===== Utilities =====

    escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, m => map[m]);
    }

    // ===== Export Data =====

    exportTasks() {
        const dataStr = JSON.stringify(this.tasks, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `tasks_${new Date().getTime()}.json`;
        link.click();
        URL.revokeObjectURL(url);
    }

    // ===== Import Data =====

    importTasks(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const imported = JSON.parse(e.target.result);
                if (Array.isArray(imported)) {
                    this.tasks = imported;
                    this.saveTasks();
                    this.render();
                    alert('Tasks imported successfully!');
                } else {
                    alert('Invalid file format');
                }
            } catch (error) {
                alert('Error importing tasks: ' + error.message);
            }
        };
        reader.readAsText(file);
    }
}

// ===== Initialize App =====
document.addEventListener('DOMContentLoaded', () => {
    new TodoApp();
});
