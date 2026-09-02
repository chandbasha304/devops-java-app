// API Base URL
const API_URL = '/api/v1/tasks';

// State
let tasks = [];
let activeFilter = 'ALL';
let searchQuery = '';

// DOM Elements
const tasksTableBody = document.getElementById('tasks-table-body');
const statTotal = document.getElementById('stat-total');
const statDeployed = document.getElementById('stat-deployed');
const statInProgress = document.getElementById('stat-in-progress');
const statPending = document.getElementById('stat-pending');

const taskModal = document.getElementById('task-modal');
const taskForm = document.getElementById('task-form');
const modalTitle = document.getElementById('modal-title');
const taskIdInput = document.getElementById('task-id');
const serviceNameInput = document.getElementById('service-name');
const serviceVersionInput = document.getElementById('service-version');
const serviceEnvSelect = document.getElementById('service-env');
const serviceStatusSelect = document.getElementById('service-status');
const serviceDeployerInput = document.getElementById('service-deployer');

const openModalBtn = document.getElementById('open-modal-btn');
const closeModalBtn = document.getElementById('close-modal-btn');
const cancelModalBtn = document.getElementById('cancel-modal-btn');
const refreshBtn = document.getElementById('refresh-btn');
const searchInput = document.getElementById('search-input');
const filterBtns = document.querySelectorAll('.filter-btn');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadData();
    setupEventListeners();
});

function setupEventListeners() {
    // Modal Open/Close
    openModalBtn.addEventListener('click', () => openModal());
    closeModalBtn.addEventListener('click', () => closeModal());
    cancelModalBtn.addEventListener('click', () => closeModal());
    
    // Close modal on click outside
    taskModal.addEventListener('click', (e) => {
        if (e.target === taskModal) closeModal();
    });

    // Form Submit (Create / Update)
    taskForm.addEventListener('submit', handleFormSubmit);

    // Refresh Button
    refreshBtn.addEventListener('click', () => {
        loadData();
        showToast('Refreshed data from H2 database', 'success');
    });

    // Search Input
    searchInput.addEventListener('input', (e) => {
        searchQuery = e.target.value.toLowerCase().trim();
        renderTable();
    });

    // Filter Buttons
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            activeFilter = btn.dataset.filter;
            renderTable();
        });
    });
}

// 1. READ (Fetch Data & Stats)
async function loadData() {
    try {
        const [tasksRes, statsRes] = await Promise.all([
            fetch(API_URL),
            fetch(`${API_URL}/stats`)
        ]);

        if (tasksRes.ok) {
            tasks = await tasksRes.json();
            renderTable();
        }

        if (statsRes.ok) {
            const stats = await statsRes.json();
            updateStatsUI(stats);
        }
    } catch (err) {
        console.error('Failed to load data:', err);
        showToast('Error connecting to backend API', 'error');
    }
}

function updateStatsUI(stats) {
    statTotal.textContent = stats.total || 0;
    statDeployed.textContent = stats.deployed || 0;
    statInProgress.textContent = stats.inProgress || 0;
    statPending.textContent = stats.pending || 0;
}

// 2. RENDER TABLE WITH FILTERS
function renderTable() {
    let filtered = tasks.filter(t => {
        const matchesFilter = (activeFilter === 'ALL') || (t.environment === activeFilter);
        const matchesSearch = !searchQuery || 
            t.serviceName.toLowerCase().includes(searchQuery) ||
            t.version.toLowerCase().includes(searchQuery) ||
            t.environment.toLowerCase().includes(searchQuery) ||
            (t.deployedBy && t.deployedBy.toLowerCase().includes(searchQuery));
        return matchesFilter && matchesSearch;
    });

    if (filtered.length === 0) {
        tasksTableBody.innerHTML = `
            <tr>
                <td colspan="8" class="empty-state">
                    No deployment records found. Click <strong>"New Deployment"</strong> to add one!
                </td>
            </tr>
        `;
        return;
    }

    tasksTableBody.innerHTML = filtered.map(t => `
        <tr>
            <td><span class="code-tag">#${t.id}</span></td>
            <td>
                <div class="service-title">
                    <span>${escapeHtml(t.serviceName)}</span>
                </div>
            </td>
            <td><span class="code-tag">${escapeHtml(t.version)}</span></td>
            <td>
                <span class="badge badge-${t.environment.toLowerCase()}">${t.environment}</span>
            </td>
            <td>
                <span class="badge badge-${t.status.toLowerCase()}">${t.status}</span>
            </td>
            <td style="color: var(--text-muted); font-size: 0.8rem;">
                ${escapeHtml(t.deployedBy || 'Cloud Build')}
            </td>
            <td style="color: var(--text-sub); font-size: 0.75rem; font-family: var(--font-mono);">
                ${formatDate(t.createdAt)}
            </td>
            <td>
                <div class="action-btns">
                    <button class="btn btn-secondary btn-sm" onclick="editTask(${t.id})">Edit</button>
                    <button class="btn btn-danger btn-sm" onclick="deleteTask(${t.id})">Delete</button>
                </div>
            </td>
        </tr>
    `).join('');
}

// 3. CREATE / UPDATE (POST / PUT)
async function handleFormSubmit(e) {
    e.preventDefault();
    
    const id = taskIdInput.value;
    const taskData = {
        serviceName: serviceNameInput.value.trim(),
        version: serviceVersionInput.value.trim(),
        environment: serviceEnvSelect.value,
        status: serviceStatusSelect.value,
        deployedBy: serviceDeployerInput.value.trim() || 'Cloud Run DevOps User'
    };

    try {
        let response;
        if (id) {
            // Update
            response = await fetch(`${API_URL}/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(taskData)
            });
        } else {
            // Create
            response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(taskData)
            });
        }

        if (response.ok) {
            closeModal();
            showToast(id ? 'Deployment updated successfully!' : 'New deployment created!', 'success');
            loadData();
        } else {
            showToast('Failed to save deployment', 'error');
        }
    } catch (err) {
        console.error('Error saving task:', err);
        showToast('Network error while saving', 'error');
    }
}

// 4. EDIT TASK MODAL
window.editTask = function(id) {
    const task = tasks.find(t => t.id === id);
    if (!task) return;

    taskIdInput.value = task.id;
    serviceNameInput.value = task.serviceName;
    serviceVersionInput.value = task.version;
    serviceEnvSelect.value = task.environment;
    serviceStatusSelect.value = task.status;
    serviceDeployerInput.value = task.deployedBy || '';

    modalTitle.textContent = `Edit Deployment #${task.id}`;
    taskModal.classList.add('active');
};

// 5. DELETE TASK
window.deleteTask = async function(id) {
    if (!confirm(`Are you sure you want to delete Deployment #${id}?`)) return;

    try {
        const res = await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
        if (res.ok) {
            showToast(`Deployment #${id} deleted`, 'success');
            loadData();
        } else {
            showToast('Failed to delete deployment', 'error');
        }
    } catch (err) {
        console.error('Error deleting task:', err);
        showToast('Network error while deleting', 'error');
    }
};

// MODAL UTILITIES
function openModal() {
    taskIdInput.value = '';
    taskForm.reset();
    modalTitle.textContent = 'Create Deployment Task';
    serviceEnvSelect.value = 'DEV';
    serviceStatusSelect.value = 'PENDING';
    serviceDeployerInput.value = 'Cloud Run User';
    taskModal.classList.add('active');
    serviceNameInput.focus();
}

function closeModal() {
    taskModal.classList.remove('active');
}

// TOAST HELPER
function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function formatDate(dateStr) {
    if (!dateStr) return 'Just now';
    const date = new Date(dateStr);
    return date.toLocaleString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
}

function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/[&<>'"]/g, 
        tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
    );
}
