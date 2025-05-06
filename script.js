// TaskPro - JavaScript implementation
// Main data store
let tasks = [
    {
        id: 1,
        title: "CS361 Assignment 3",
        dueDate: "2025-04-25",
        class: "CS361",
        priority: "high",
        status: "incomplete",
        description: "Complete the microservices implementation with appropriate API endpoints. Be sure to include error handling and documentation."
    },
    {
        id: 2,
        title: "Study for Midterm",
        dueDate: "2025-04-28",
        class: "MATH241",
        priority: "medium",
        status: "in-progress",
        description: "Review chapters 5-8 and practice problems from the study guide."
    }
];

// Current task ID (for tracking next task ID)
let currentTaskId = 3;

// DOM Elements
document.addEventListener('DOMContentLoaded', () => {
    // Page navigation
    setupNavigation();
    
    // Form submissions
    setupForms();
    
    // Task interactions
    setupTaskInteractions();
    
    // Keyboard shortcuts
    setupKeyboardShortcuts();
});

// Setup page navigation
function setupNavigation() {
    // Welcome page navigation
    document.getElementById('login-btn').addEventListener('click', () => {
        showPage('dashboard-page');
    });
    
    document.getElementById('signup-btn').addEventListener('click', () => {
        showPage('dashboard-page');
    });
    
    // Dashboard navigation
    document.getElementById('nav-dashboard').addEventListener('click', () => {
        showPage('dashboard-page');
    });
    
    document.getElementById('nav-add-task').addEventListener('click', () => {
        showPage('add-task-page');
    });
    
    document.getElementById('nav-help').addEventListener('click', () => {
        showPage('help-page');
    });
    
    document.getElementById('dashboard-add-task').addEventListener('click', () => {
        showPage('add-task-page');
    });
    
    // Add Task page navigation
    document.getElementById('nav-dashboard-from-add').addEventListener('click', () => {
        showPage('dashboard-page');
    });
    
    document.getElementById('nav-help-from-add').addEventListener('click', () => {
        showPage('help-page');
    });
    
    document.getElementById('cancel-add').addEventListener('click', () => {
        showPage('dashboard-page');
    });
    
    // Task Details page navigation
    document.getElementById('nav-dashboard-from-details').addEventListener('click', () => {
        showPage('dashboard-page');
    });
    
    document.getElementById('nav-add-task-from-details').addEventListener('click', () => {
        showPage('add-task-page');
    });
    
    document.getElementById('nav-help-from-details').addEventListener('click', () => {
        showPage('help-page');
    });
    
    document.getElementById('back-to-dashboard').addEventListener('click', () => {
        showPage('dashboard-page');
    });
    
    // Edit Task page navigation
    document.getElementById('nav-dashboard-from-edit').addEventListener('click', () => {
        if (hasUnsavedChanges()) {
            showConfirmationDialog(
                "You have unsaved changes. Are you sure you want to leave?",
                () => showPage('dashboard-page')
            );
        } else {
            showPage('dashboard-page');
        }
    });
    
    document.getElementById('nav-add-task-from-edit').addEventListener('click', () => {
        if (hasUnsavedChanges()) {
            showConfirmationDialog(
                "You have unsaved changes. Are you sure you want to leave?",
                () => showPage('add-task-page')
            );
        } else {
            showPage('add-task-page');
        }
    });
    
    document.getElementById('nav-help-from-edit').addEventListener('click', () => {
        if (hasUnsavedChanges()) {
            showConfirmationDialog(
                "You have unsaved changes. Are you sure you want to leave?",
                () => showPage('help-page')
            );
        } else {
            showPage('help-page');
        }
    });
    
    document.getElementById('cancel-edit').addEventListener('click', () => {
        if (hasUnsavedChanges()) {
            showConfirmationDialog(
                "You have unsaved changes. Are you sure you want to leave?",
                () => showPage('task-details-page')
            );
        } else {
            showPage('task-details-page');
        }
    });
    
    // Help page navigation
    document.getElementById('nav-dashboard-from-help').addEventListener('click', () => {
        showPage('dashboard-page');
    });
    
    document.getElementById('nav-add-task-from-help').addEventListener('click', () => {
        showPage('add-task-page');
    });
}

// Show specific page and hide others
function showPage(pageId) {
    // Hide all pages
    const pages = document.querySelectorAll('.page');
    pages.forEach(page => page.classList.remove('active'));
    
    // Show requested page
    document.getElementById(pageId).classList.add('active');
    
    // Special actions for specific pages
    if (pageId === 'dashboard-page') {
        renderTasks();
    }
}

// Setup form submissions
function setupForms() {
    // Add Task form submission
    const addTaskForm = document.getElementById('add-task-form');
    addTaskForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // Get form values
        const title = document.getElementById('task-title').value;
        const dueDate = document.getElementById('due-date').value;
        const taskClass = document.getElementById('task-class').value;
        const priority = document.getElementById('task-priority').value;
        const description = document.getElementById('task-description').value;
        
        // Create new task
        const newTask = {
            id: currentTaskId++,
            title: title,
            dueDate: dueDate,
            class: taskClass,
            priority: priority,
            status: 'incomplete',
            description: description
        };
        
        // Add to tasks array
        tasks.push(newTask);
        
        // Reset form
        addTaskForm.reset();
        
        // Show success message
        alert('Task added successfully!');
        
        // Go back to dashboard
        showPage('dashboard-page');
    });
    
    // Edit Task form submission
    const editTaskForm = document.getElementById('edit-task-form');
    editTaskForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // Get form values
        const title = document.getElementById('edit-task-title').value;
        const dueDate = document.getElementById('edit-due-date').value;
        const taskClass = document.getElementById('edit-task-class').value;
        const priority = document.getElementById('edit-task-priority').value;
        const description = document.getElementById('edit-task-description').value;
        
        // Get current task ID
        const taskId = parseInt(editTaskForm.dataset.taskId);
        
        // Find and update task
        const taskIndex = tasks.findIndex(task => task.id === taskId);
        if (taskIndex !== -1) {
            tasks[taskIndex].title = title;
            tasks[taskIndex].dueDate = dueDate;
            tasks[taskIndex].class = taskClass;
            tasks[taskIndex].priority = priority;
            tasks[taskIndex].description = description;
            
            // Refresh task details
            loadTaskDetails(taskId);
            
            // Show success message
            alert('Task updated successfully!');
            
            // Go back to task details
            showPage('task-details-page');
        }
    });
}

// Setup task interactions
function setupTaskInteractions() {
    // Task marking as complete
    document.getElementById('mark-complete-btn').addEventListener('click', () => {
        const taskId = parseInt(document.getElementById('detail-task-title').dataset.taskId);
        const taskIndex = tasks.findIndex(task => task.id === taskId);
        
        if (taskIndex !== -1) {
            tasks[taskIndex].status = tasks[taskIndex].status === 'incomplete' ? 'complete' : 'incomplete';
            loadTaskDetails(taskId);
            renderTasks();
        }
    });
    
    // Task editing
    document.getElementById('edit-task-btn').addEventListener('click', () => {
        const taskId = parseInt(document.getElementById('detail-task-title').dataset.taskId);
        loadTaskForEditing(taskId);
        showPage('edit-task-page');
    });
    
    // Task deletion
    document.getElementById('delete-task-btn').addEventListener('click', () => {
        const taskId = parseInt(document.getElementById('detail-task-title').dataset.taskId);
        
        showConfirmationDialog(
            "This action cannot be undone. All task information will be permanently deleted.",
            () => {
                const taskIndex = tasks.findIndex(task => task.id === taskId);
                if (taskIndex !== -1) {
                    tasks.splice(taskIndex, 1);
                    showPage('dashboard-page');
                }
            }
        );
    });
    
    // Sort tasks
    document.getElementById('sort-tasks').addEventListener('change', (e) => {
        renderTasks(e.target.value);
    });
    
    // Search tasks
    document.getElementById('task-search').addEventListener('input', (e) => {
        filterTasks(e.target.value);
    });
    
    // Setup dialog confirmations
    document.getElementById('confirm-yes').addEventListener('click', () => {
        // Execute callback and close dialog
        const dialog = document.getElementById('confirmation-dialog');
        if (dialog.dataset.callback) {
            const callback = window[dialog.dataset.callback];
            if (typeof callback === 'function') {
                callback();
            }
        }
        dialog.classList.remove('active');
    });
    
    document.getElementById('confirm-no').addEventListener('click', () => {
        // Just close dialog
        document.getElementById('confirmation-dialog').classList.remove('active');
    });
}

// Setup keyboard shortcuts
function setupKeyboardShortcuts() {
    // Enter key for login
    document.getElementById('password').addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            document.getElementById('login-btn').click();
        }
    });
    
    // Enter key for search
    document.getElementById('task-search').addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            document.getElementById('search-btn').click();
        }
    });
    
    // Ctrl+S for save in edit form
    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 's') {
            if (document.getElementById('edit-task-page').classList.contains('active')) {
                e.preventDefault();
                document.getElementById('edit-task-form').dispatchEvent(new Event('submit'));
            }
        }
    });
}

// Render tasks in the dashboard
function renderTasks(sortBy = 'due-date') {
    const tasksContainer = document.getElementById('tasks-container');
    tasksContainer.innerHTML = '';
    
    // Sort tasks
    let sortedTasks = [...tasks];
    if (sortBy === 'due-date') {
        sortedTasks.sort((a, b) => new Date(a.dueDate) - new Date(b.dueDate));
    } else if (sortBy === 'priority') {
        const priorityOrder = { high: 1, medium: 2, low: 3 };
        sortedTasks.sort((a, b) => priorityOrder[a.priority] - priorityOrder[b.priority]);
    } else if (sortBy === 'class') {
        sortedTasks.sort((a, b) => a.class.localeCompare(b.class));
    }
    
    // Create task elements
    sortedTasks.forEach(task => {
        const taskElement = document.createElement('div');
        taskElement.className = 'task-item';
        taskElement.dataset.taskId = task.id;
        
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.className = 'task-checkbox';
        checkbox.id = `task-${task.id}`;
        checkbox.checked = task.status === 'complete';
        checkbox.setAttribute('aria-label', `Mark ${task.title} as complete`);
        
        // Checkbox event listener
        checkbox.addEventListener('change', () => {
            task.status = checkbox.checked ? 'complete' : 'incomplete';
        });
        
        const content = document.createElement('div');
        content.className = 'task-content';
        
        const title = document.createElement('h3');
        title.className = 'task-title';
        title.textContent = task.title;
        
        const details = document.createElement('div');
        details.className = 'task-details';
        
        const dueDate = document.createElement('span');
        dueDate.className = 'task-due';
        dueDate.textContent = `Due: ${formatDate(task.dueDate)}`;
        
        const taskClass = document.createElement('span');
        taskClass.className = 'task-class';
        taskClass.textContent = task.class;
        
        const status = document.createElement('span');
        status.className = 'task-status';
        status.textContent = capitalizeFirstLetter(task.status);
        
        details.appendChild(dueDate);
        details.appendChild(taskClass);
        details.appendChild(status);
        
        content.appendChild(title);
        content.appendChild(details);
        
        const actions = document.createElement('div');
        actions.className = 'task-actions';
        
        const editBtn = document.createElement('button');
        editBtn.className = 'edit-task icon-btn';
        editBtn.innerHTML = '<i class="fas fa-edit"></i>';
        editBtn.setAttribute('aria-label', `Edit ${task.title}`);
        
        editBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            loadTaskForEditing(task.id);
            showPage('edit-task-page');
        });
        
        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'delete-task icon-btn';
        deleteBtn.innerHTML = '<i class="fas fa-trash"></i>';
        deleteBtn.setAttribute('aria-label', `Delete ${task.title}`);
        
        deleteBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            showConfirmationDialog(
                "This action cannot be undone. All task information will be permanently deleted.",
                () => {
                    const taskIndex = tasks.findIndex(t => t.id === task.id);
                    if (taskIndex !== -1) {
                        tasks.splice(taskIndex, 1);
                        renderTasks(document.getElementById('sort-tasks').value);
                    }
                }
            );
        });
        
        actions.appendChild(editBtn);
        actions.appendChild(deleteBtn);
        
        taskElement.appendChild(checkbox);
        taskElement.appendChild(content);
        taskElement.appendChild(actions);
        
        // Make entire task clickable to view details
        taskElement.addEventListener('click', (e) => {
            if (e.target !== checkbox && !e.target.closest('.task-actions')) {
                loadTaskDetails(task.id);
                showPage('task-details-page');
            }
        });
        
        tasksContainer.appendChild(taskElement);
    });
    
    // Show empty state if no tasks
    if (sortedTasks.length === 0) {
        const emptyState = document.createElement('div');
        emptyState.className = 'empty-state';
        emptyState.textContent = 'No tasks found. Create a new task to get started!';
        tasksContainer.appendChild(emptyState);
    }
}

// Filter tasks by search term
function filterTasks(searchTerm) {
    const tasksContainer = document.getElementById('tasks-container');
    const taskItems = tasksContainer.querySelectorAll('.task-item');
    
    searchTerm = searchTerm.toLowerCase();
    
    taskItems.forEach(taskItem => {
        const taskId = parseInt(taskItem.dataset.taskId);
        const task = tasks.find(t => t.id === taskId);
        
        if (task) {
            const matchesSearch = 
                task.title.toLowerCase().includes(searchTerm) ||
                task.class.toLowerCase().includes(searchTerm) ||
                task.description.toLowerCase().includes(searchTerm);
            
            taskItem.style.display = matchesSearch ? 'flex' : 'none';
        }
    });
}

// Load task details into details page
function loadTaskDetails(taskId) {
    const task = tasks.find(task => task.id === taskId);
    
    if (task) {
        const titleElement = document.getElementById('detail-task-title');
        titleElement.textContent = task.title;
        titleElement.dataset.taskId = taskId;
        
        document.getElementById('detail-due-date').textContent = formatDate(task.dueDate);
        document.getElementById('detail-class').textContent = task.class;
        document.getElementById('detail-priority').textContent = capitalizeFirstLetter(task.priority);
        document.getElementById('detail-status').textContent = capitalizeFirstLetter(task.status);
        document.getElementById('detail-description').textContent = task.description;
        
        // Update button text based on status
        const markCompleteBtn = document.getElementById('mark-complete-btn');
        markCompleteBtn.textContent = task.status === 'incomplete' ? 'Mark Complete' : 'Mark Incomplete';
    }
}

// Load task for editing
function loadTaskForEditing(taskId) {
    const task = tasks.find(task => task.id === taskId);
    
    if (task) {
        const editForm = document.getElementById('edit-task-form');
        editForm.dataset.taskId = taskId;
        
        document.getElementById('edit-task-title').value = task.title;
        document.getElementById('edit-due-date').value = task.dueDate;
        document.getElementById('edit-task-class').value = task.class;
        document.getElementById('edit-task-priority').value = task.priority;
        document.getElementById('edit-task-description').value = task.description;
    }
}

// Show confirmation dialog
function showConfirmationDialog(message, callback) {
    const dialog = document.getElementById('confirmation-dialog');
    document.getElementById('dialog-message').textContent = message;
    
    // Store callback in dialog's dataset
    dialog.dataset.callback = callback.name;
    
    // Add callback to window object to make it accessible
    const callbackName = 'dialogCallback' + Date.now();
    window[callbackName] = callback;
    dialog.dataset.callback = callbackName;
    
    dialog.classList.add('active');
}

// Check if form has unsaved changes
function hasUnsavedChanges() {
    // For now, just return false (no checking implemented)
    // In a real app, this would compare current form values with original values
    return false;
}

// Helper function to format date
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// Helper function to capitalize first letter
function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}
