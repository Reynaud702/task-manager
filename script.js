// TaskPro - Enhanced JavaScript implementation with Microservices Integration

// Main data store
let tasks = [
    {
        id: 1,
        title: "CS361 Assignment 3",
        dueDate: "2025-06-05",
        class: "CS361",
        priority: "high",
        status: "incomplete",
        description: "Complete the microservices implementation with appropriate API endpoints. Be sure to include error handling and documentation.",
        estimatedHours: 6,
        createdDate: "2025-05-15"
    },
    {
        id: 2,
        title: "Study for Midterm",
        dueDate: "2025-06-03",
        class: "MATH241",
        priority: "medium",
        status: "in-progress",
        description: "Review chapters 5-8 and practice problems from the study guide.",
        estimatedHours: 4,
        createdDate: "2025-05-20"
    }
];

// Current task ID and user info
let currentTaskId = 3;
let currentUser = {
    email: "student@oregonstate.edu",
    firstName: "John",
    lastName: "Doe"
};

// Microservice URLs
const MICROSERVICE_URLS = {
    DUE_DATE_CALCULATOR: 'http://localhost:5001',
    EMAIL_REMINDER: 'http://localhost:5002',
    TASK_STATS: 'http://localhost:5003'
};

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
    
    // Microservices integration
    setupMicroservicesIntegration();
    
    // Load initial data
    loadInitialData();
});

// Setup microservices integration
function setupMicroservicesIntegration() {
    // Add microservice features to the UI
    addMicroserviceFeatures();
    
    // Setup event handlers for microservice features
    setupMicroserviceEventHandlers();
}

function addMicroserviceFeatures() {
    // Add due date analysis to dashboard
    const dashboardActions = document.querySelector('.dashboard-actions');
    if (dashboardActions) {
        const dueDateWidget = document.createElement('div');
        dueDateWidget.className = 'due-date-widget';
        dueDateWidget.innerHTML = `
            <button id="analyze-due-dates" class="btn secondary-btn">
                <i class="fas fa-calendar-check"></i> Analyze Due Dates
            </button>
        `;
        dashboardActions.appendChild(dueDateWidget);
    }
    
    // Add stats widget to dashboard
    const dashboardContainer = document.querySelector('.dashboard-container');
    if (dashboardContainer) {
        const statsWidget = document.createElement('div');
        statsWidget.className = 'stats-widget';
        statsWidget.innerHTML = `
            <div class="widget-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <h3 style="margin: 0;">Task Statistics</h3>
                <button id="refresh-stats" class="btn tertiary-btn">Refresh</button>
            </div>
            <div id="stats-content" class="stats-content">
                <p>Loading statistics...</p>
            </div>
        `;
        statsWidget.style.cssText = `
            background: white; 
            border-radius: 8px; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
            padding: 20px; 
            margin-top: 20px;
        `;
        dashboardContainer.appendChild(statsWidget);
    }
    
    // Add reminder settings to help page
    const helpSection = document.querySelector('.help-section');
    if (helpSection) {
        const reminderSettings = document.createElement('div');
        reminderSettings.className = 'reminder-settings-section';
        reminderSettings.innerHTML = `
            <h3>Email Reminder Settings</h3>
            <div class="reminder-controls">
                <label>
                    <input type="checkbox" id="enable-reminders" checked> 
                    Enable email reminders
                </label>
                <br><br>
                <label for="reminder-timing">Send reminders:</label>
                <select id="reminder-timing">
                    <option value="1">1 day before due date</option>
                    <option value="3">3 days before due date</option>
                    <option value="7">7 days before due date</option>
                </select>
                <br><br>
                <button id="save-reminder-settings" class="btn primary-btn">Save Settings</button>
            </div>
        `;
        helpSection.appendChild(reminderSettings);
    }
}

function setupMicroserviceEventHandlers() {
    // Due date analyzer
    const analyzeDueDatesBtn = document.getElementById('analyze-due-dates');
    if (analyzeDueDatesBtn) {
        analyzeDueDatesBtn.addEventListener('click', analyzeDueDates);
    }
    
    // Stats refresher
    const refreshStatsBtn = document.getElementById('refresh-stats');
    if (refreshStatsBtn) {
        refreshStatsBtn.addEventListener('click', refreshStats);
    }
    
    // Reminder settings
    const saveReminderBtn = document.getElementById('save-reminder-settings');
    if (saveReminderBtn) {
        saveReminderBtn.addEventListener('click', saveReminderSettings);
    }
}

// Microservice API calls
async function callMicroservice(service, endpoint, method = 'GET', data = null) {
    try {
        const url = `${MICROSERVICE_URLS[service]}${endpoint}`;
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            }
        };
        
        if (data && (method === 'POST' || method === 'PUT')) {
            options.body = JSON.stringify(data);
        }
        
        console.log(`=== MICROSERVICE CALL ===`);
        console.log(`Service: ${service}`);
        console.log(`Making ${method} request to ${url}`);
        console.log('Request data:', data);
        console.log('========================');
        
        const response = await fetch(url, options);
        const responseData = await response.json();
        
        console.log('Response status:', response.status);
        console.log('Response data:', responseData);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${responseData.error || 'Unknown error'}`);
        }
        
        return responseData;
    } catch (error) {
        console.error(`Error calling ${service} microservice:`, error);
        return { success: false, error: error.message };
    }
}

// Due Date Calculator Integration (Microservice B)
async function analyzeDueDates() {
    // Get upcoming tasks using the batch endpoint
    const tasksData = {
        tasks: tasks.map(task => ({
            id: task.id,
            title: task.title,
            due_date: task.dueDate
        }))
    };
    
    const result = await callMicroservice('DUE_DATE_CALCULATOR', '/api/duedate/batch-calculate', 'POST', tasksData);
    
    if (result.success) {
        // Update task display with priority suggestions
        updateTasksWithAnalysis(result.results);
        
        // Get upcoming tasks summary
        const upcomingResult = await callMicroservice('DUE_DATE_CALCULATOR', '/api/duedate/upcoming', 'GET');
        
        if (upcomingResult.success) {
            const { overdue, urgent, due_soon } = upcomingResult.summary;
            let message = `Due Date Analysis:\n`;
            if (overdue > 0) message += `• ${overdue} overdue tasks\n`;
            if (urgent > 0) message += `• ${urgent} urgent tasks\n`;
            if (due_soon > 0) message += `• ${due_soon} tasks due soon\n`;
            
            alert(message || 'All tasks have ample time!');
        }
    } else {
        alert(`Error analyzing due dates: ${result.error}`);
    }
}

function updateTasksWithAnalysis(analysisResults) {
    // Add priority suggestions to task items
    const taskItems = document.querySelectorAll('.task-item');
    
    taskItems.forEach(taskItem => {
        const taskId = parseInt(taskItem.dataset.taskId);
        const analysis = analysisResults.find(r => r.task_id === taskId);
        
        if (analysis && !analysis.error) {
            // Remove existing priority badges
            const existingBadge = taskItem.querySelector('.priority-badge');
            if (existingBadge) {
                existingBadge.remove();
            }
            
            // Add new priority badge
            const priorityBadge = document.createElement('span');
            priorityBadge.className = 'priority-badge';
            priorityBadge.textContent = `Suggested: ${analysis.suggested_priority.toUpperCase()}`;
            priorityBadge.style.cssText = `
                background: ${analysis.suggested_priority === 'high' ? '#e74c3c' : analysis.suggested_priority === 'medium' ? '#f39c12' : '#27ae60'};
                color: white;
                padding: 2px 8px;
                border-radius: 12px;
                font-size: 0.8em;
                margin-left: 10px;
            `;
            
            const taskDetails = taskItem.querySelector('.task-details');
            taskDetails.appendChild(priorityBadge);
        }
    });
}

// Task Stats Integration (Microservice D)
async function refreshStats() {
    const statsContent = document.getElementById('stats-content');
    statsContent.innerHTML = '<p>Loading statistics...</p>';
    
    // Get dashboard data
    const result = await callMicroservice('TASK_STATS', `/api/stats/dashboard-data?user_email=${currentUser.email}`);
    
    if (result.success) {
        const stats = result.dashboard.overall_stats;
        const categoryBreakdown = result.dashboard.category_breakdown;
        const recentCompletions = result.dashboard.recent_completions;
        
        statsContent.innerHTML = `
            <div class="stats-grid">
                <div class="stat-item">
                    <h4>${stats.total_completed}</h4>
                    <p>Total Completed</p>
                </div>
                <div class="stat-item">
                    <h4>${stats.this_week}</h4>
                    <p>This Week</p>
                </div>
                <div class="stat-item">
                    <h4>${stats.average_completion_time}</h4>
                    <p>Avg Days to Complete</p>
                </div>
            </div>
            
            <div class="category-breakdown">
                <h4>By Category:</h4>
                ${Object.entries(categoryBreakdown).length > 0 ? 
                    Object.entries(categoryBreakdown).map(([category, count]) => 
                        `<span class="category-badge">${category}: ${count}</span>`
                    ).join(' ') :
                    '<p>No completed tasks yet</p>'
                }
            </div>
            
            <div class="recent-completions">
                <h4>Recent Completions:</h4>
                ${recentCompletions.length > 0 ? 
                    recentCompletions.map(task => 
                        `<div class="recent-task">${task.task_title} (${task.completion_date})</div>`
                    ).join('') : 
                    '<p>No recent completions</p>'
                }
            </div>
        `;
        
        // Add CSS for stats display
        if (!document.querySelector('#stats-styles')) {
            const style = document.createElement('style');
            style.id = 'stats-styles';
            style.textContent = `
                .stats-grid { display: flex; gap: 15px; margin-bottom: 15px; }
                .stat-item { text-align: center; flex: 1; }
                .stat-item h4 { margin: 0; font-size: 1.5em; color: var(--primary-color); }
                .stat-item p { margin: 5px 0 0 0; font-size: 0.9em; color: var(--dark-gray); }
                .category-badge { background: var(--light-gray); padding: 3px 8px; border-radius: 10px; margin: 2px; display: inline-block; font-size: 0.85em; }
                .recent-task { font-size: 0.9em; margin: 5px 0; padding: 5px; background: var(--bg-color); border-radius: 4px; }
            `;
            document.head.appendChild(style);
        }
    } else {
        statsContent.innerHTML = `<p style="color: red;">Error loading stats: ${result.error}</p>`;
    }
}

// Email Reminder Integration (Microservice C)
async function saveReminderSettings() {
    const enableReminders = document.getElementById('enable-reminders').checked;
    const reminderTiming = parseInt(document.getElementById('reminder-timing').value);
    
    const data = {
        user_email: currentUser.email,
        reminders_enabled: enableReminders,
        reminder_timing: reminderTiming,
        email_notifications: true
    };
    
    const result = await callMicroservice('EMAIL_REMINDER', '/api/reminder/settings', 'PUT', data);
    
    if (result.success) {
        alert('Reminder settings saved successfully!');
    } else {
        alert(`Error saving settings: ${result.error}`);
    }
}

async function scheduleTaskReminder(taskId, taskTitle, dueDate, priority) {
    const data = {
        user_email: currentUser.email,
        task_id: taskId,
        task_title: taskTitle,
        due_date: dueDate,
        priority: priority
    };
    
    const result = await callMicroservice('EMAIL_REMINDER', '/api/reminder/schedule', 'POST', data);
    
    if (result.success && result.reminder_id) {
        console.log(`Reminder scheduled for task ${taskId} with ID ${result.reminder_id}`);
    } else {
        console.warn(`Failed to schedule reminder for task ${taskId}: ${result.error}`);
    }
}

async function recordTaskCompletion(task) {
    const data = {
        task_id: task.id,
        user_email: currentUser.email,
        task_title: task.title,
        category: task.class,
        completion_date: new Date().toISOString().split('T')[0],
        created_date: task.createdDate || new Date().toISOString().split('T')[0]
    };
    
    const result = await callMicroservice('TASK_STATS', '/api/stats/record-completion', 'POST', data);
    
    if (result.success) {
        console.log(`Task completion recorded for task ${task.id}`);
        // Refresh stats display
        setTimeout(refreshStats, 500);
    } else {
        console.warn(`Failed to record completion for task ${task.id}: ${result.error}`);
    }
}

// Load initial data and setup
async function loadInitialData() {
    // Load user reminder settings
    const settingsResult = await callMicroservice('EMAIL_REMINDER', `/api/reminder/settings?user_email=${currentUser.email}`);
    if (settingsResult.success) {
        const settings = settingsResult.settings;
        const enableCheckbox = document.getElementById('enable-reminders');
        const timingSelect = document.getElementById('reminder-timing');
        
        if (enableCheckbox) enableCheckbox.checked = settings.reminders_enabled;
        if (timingSelect) timingSelect.value = settings.reminder_timing;
    }
    
    // Load initial stats
    refreshStats();
    
    // Schedule reminders for existing incomplete tasks
    tasks.forEach(task => {
        if (task.status !== 'complete') {
            scheduleTaskReminder(task.id, task.title, task.dueDate, task.priority);
        }
    });
}

// Enhanced task management functions
function addTaskWithMicroservices(taskData) {
    // Add task to local storage
    const newTask = {
        ...taskData,
        id: currentTaskId++,
        createdDate: new Date().toISOString().split('T')[0]
    };
    
    tasks.push(newTask);
    
    // Schedule reminder for new task
    scheduleTaskReminder(newTask.id, newTask.title, newTask.dueDate, newTask.priority);
    
    return newTask;
}

function markTaskCompleteWithMicroservices(taskId) {
    const task = tasks.find(t => t.id === taskId);
    if (task) {
        task.status = 'complete';
        
        // Record completion in stats microservice
        recordTaskCompletion(task);
        
        // Update UI
        renderTasks();
    }
}

// Setup page navigation (existing function enhanced)
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
        refreshStats();
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
        
        // Create new task using microservices
        const newTask = addTaskWithMicroservices({
            title: title,
            dueDate: dueDate,
            class: taskClass,
            priority: priority,
            status: 'incomplete',
            description: description
        });
        
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
            
            // Schedule new reminder for updated task
            scheduleTaskReminder(taskId, title, dueDate, priority);
            
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
        const task = tasks.find(t => t.id === taskId);
        
        if (task) {
            if (task.status === 'incomplete') {
                markTaskCompleteWithMicroservices(taskId);
                loadTaskDetails(taskId);
            } else {
                task.status = 'incomplete';
                loadTaskDetails(taskId);
                renderTasks();
            }
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
            if (checkbox.checked) {
                markTaskCompleteWithMicroservices(task.id);
            } else {
                task.status = 'incomplete';
                renderTasks(document.getElementById('sort-tasks').value);
            }
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
    
    // Auto-analyze due dates after rendering
    setTimeout(analyzeDueDates, 1000);
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

// Console logging for demonstration
function logMicroserviceCall(service, endpoint, method, data) {
    console.log(`=== MICROSERVICE CALL ===`);
    console.log(`Service: ${service}`);
    console.log(`Endpoint: ${endpoint}`);
    console.log(`Method: ${method}`);
    console.log(`Data:`, data);
    console.log(`========================`);
}