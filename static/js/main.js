// Main JavaScript for Thought Tracker

document.addEventListener('DOMContentLoaded', function() {
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in-up');
    });
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.classList.contains('show')) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 5000);
    });
    
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const content = form.querySelector('#content');
            const keywords = form.querySelector('#keywords');
            
            if (content && content.value.trim() === '') {
                e.preventDefault();
                showAlert('Vui lòng nhập nội dung suy nghĩ!', 'error');
                content.focus();
                return;
            }
            
            if (keywords && keywords.value.trim() === '') {
                e.preventDefault();
                showAlert('Vui lòng nhập ít nhất một keyword!', 'error');
                keywords.focus();
                return;
            }
        });
    });
    
    // Auto-resize textarea
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    });
    
    // Keyword suggestions (simple implementation)
    const keywordInput = document.getElementById('keywords');
    if (keywordInput) {
        const commonKeywords = [
            'học tập', 'công việc', 'cảm xúc', 'gia đình', 'bạn bè',
            'sức khỏe', 'giải trí', 'du lịch', 'ăn uống', 'thể thao',
            'nghệ thuật', 'âm nhạc', 'sách', 'phim', 'game',
            'tương lai', 'quá khứ', 'hiện tại', 'mục tiêu', 'ước mơ'
        ];
        
        keywordInput.addEventListener('input', function() {
            const value = this.value.toLowerCase();
            if (value.length > 1) {
                const suggestions = commonKeywords.filter(keyword => 
                    keyword.toLowerCase().includes(value)
                );
                
                if (suggestions.length > 0) {
                    showKeywordSuggestions(suggestions, this);
                }
            }
        });
    }
    
    // Delete confirmation
    const deleteButtons = document.querySelectorAll('a[href*="delete"]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Bạn có chắc muốn xóa thought này?')) {
                e.preventDefault();
            }
        });
    });
    
    // Search form enhancement
    const searchForm = document.querySelector('form[action*="search"]');
    if (searchForm) {
        searchForm.addEventListener('submit', function() {
            const keyword = this.querySelector('#keyword').value.trim();
            const minWeight = this.querySelector('#min_weight').value;
            const maxWeight = this.querySelector('#max_weight').value;
            
            if (!keyword && !minWeight && !maxWeight) {
                showAlert('Vui lòng nhập ít nhất một tiêu chí tìm kiếm!', 'warning');
                return false;
            }
        });
    }
});

// Helper functions
function showAlert(message, type = 'info') {
    const alertContainer = document.querySelector('.container');
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertContainer.insertBefore(alertDiv, alertContainer.firstChild);
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        if (alertDiv.classList.contains('show')) {
            const bsAlert = new bootstrap.Alert(alertDiv);
            bsAlert.close();
        }
    }, 5000);
}

function showKeywordSuggestions(suggestions, input) {
    // Remove existing suggestions
    const existingSuggestions = document.querySelector('.keyword-suggestions');
    if (existingSuggestions) {
        existingSuggestions.remove();
    }
    
    if (suggestions.length === 0) return;
    
    const suggestionsDiv = document.createElement('div');
    suggestionsDiv.className = 'keyword-suggestions position-absolute bg-white border rounded shadow-sm';
    suggestionsDiv.style.cssText = `
        top: 100%;
        left: 0;
        right: 0;
        z-index: 1000;
        max-height: 200px;
        overflow-y: auto;
    `;
    
    suggestions.slice(0, 5).forEach(suggestion => {
        const suggestionItem = document.createElement('div');
        suggestionItem.className = 'p-2 border-bottom cursor-pointer';
        suggestionItem.textContent = suggestion;
        suggestionItem.style.cursor = 'pointer';
        
        suggestionItem.addEventListener('click', function() {
            const currentKeywords = input.value.split(',').map(k => k.trim()).filter(k => k);
            if (!currentKeywords.includes(suggestion)) {
                input.value = currentKeywords.concat(suggestion).join(', ');
            }
            suggestionsDiv.remove();
            input.focus();
        });
        
        suggestionsDiv.appendChild(suggestionItem);
    });
    
    input.parentNode.style.position = 'relative';
    input.parentNode.appendChild(suggestionsDiv);
    
    // Hide suggestions when clicking outside
    document.addEventListener('click', function(e) {
        if (!input.contains(e.target) && !suggestionsDiv.contains(e.target)) {
            suggestionsDiv.remove();
        }
    });
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Loading state for forms
function setLoadingState(form, loading = true) {
    const submitButton = form.querySelector('button[type="submit"]');
    if (submitButton) {
        if (loading) {
            submitButton.disabled = true;
            submitButton.innerHTML = '<span class="loading"></span> Đang xử lý...';
        } else {
            submitButton.disabled = false;
            submitButton.innerHTML = '<i class="fas fa-save me-2"></i>Lưu suy nghĩ';
        }
    }
}

// Bubble Chart Interactions
function initBubbleChart() {
    const bubbles = document.querySelectorAll('.bubble');
    const container = document.querySelector('.bubble-chart-container');
    
    if (!bubbles.length || !container) return;
    
    // Create tooltip
    const tooltip = document.createElement('div');
    tooltip.className = 'bubble-tooltip';
    document.body.appendChild(tooltip);
    
    // Drag and drop variables
    let isDragging = false;
    let currentBubble = null;
    let startX = 0;
    let startY = 0;
    let startLeft = 0;
    let startTop = 0;
    let dragThreshold = 5; // Minimum distance to consider as drag (in pixels)
    let hasMoved = false;
    
    // Add hover effects and drag functionality
    bubbles.forEach(bubble => {
        // Hover effects
        bubble.addEventListener('mouseenter', function(e) {
            if (!isDragging) {
                const keyword = this.dataset.keyword;
                const weight = this.dataset.weight;
                
                tooltip.innerHTML = `
                    <strong>${keyword}</strong><br>
                    Tổng trọng số: ${weight} điểm<br>
                    <small>Kéo để di chuyển</small>
                `;
                tooltip.classList.add('show');
                
                // Position tooltip
                const rect = this.getBoundingClientRect();
                tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
                tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';
            }
        });
        
        bubble.addEventListener('mouseleave', function() {
            if (!isDragging) {
                tooltip.classList.remove('show');
            }
        });
        
        bubble.addEventListener('mousemove', function(e) {
            if (!isDragging) {
                const rect = this.getBoundingClientRect();
                tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
                tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';
            }
        });
        
        // Mouse drag events
        bubble.addEventListener('mousedown', function(e) {
            e.preventDefault();
            isDragging = false; // Don't set to true yet
            hasMoved = false;
            currentBubble = this;
            
            startX = e.clientX;
            startY = e.clientY;
            startLeft = parseFloat(this.style.left) || 0;
            startTop = parseFloat(this.style.top) || 0;
            
            // Disable text selection
            document.body.style.userSelect = 'none';
        });
        
        // Click to search (only if not dragging)
        bubble.addEventListener('click', function(e) {
            if (!hasMoved) { // Only if mouse hasn't moved much
                const keyword = this.dataset.keyword;
                const searchUrl = `/search?keyword=${encodeURIComponent(keyword)}`;
                window.open(searchUrl, '_blank');
            }
        });
    });
    
    // Global mouse events for dragging
    document.addEventListener('mousemove', function(e) {
        if (currentBubble) {
            const deltaX = e.clientX - startX;
            const deltaY = e.clientY - startY;
            const distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
            
            // Check if mouse has moved enough to start dragging
            if (distance > dragThreshold && !isDragging) {
                isDragging = true;
                hasMoved = true;
                currentBubble.classList.add('dragging');
                tooltip.classList.remove('show');
            }
            
            if (isDragging && currentBubble) {
                e.preventDefault();
                
                const containerRect = container.getBoundingClientRect();
                const bubbleSize = currentBubble.offsetWidth;
                
                // Calculate new position in percentage
                const newLeft = startLeft + (deltaX / containerRect.width) * 100;
                const newTop = startTop + (deltaY / containerRect.height) * 100;
                
                // Constrain to container bounds
                const minLeft = 0;
                const maxLeft = 100 - (bubbleSize / containerRect.width) * 100;
                const minTop = 0;
                const maxTop = 100 - (bubbleSize / containerRect.height) * 100;
                
                const constrainedLeft = Math.max(minLeft, Math.min(maxLeft, newLeft));
                const constrainedTop = Math.max(minTop, Math.min(maxTop, newTop));
                
                currentBubble.style.left = constrainedLeft + '%';
                currentBubble.style.top = constrainedTop + '%';
            }
        }
    });
    
    document.addEventListener('mouseup', function(e) {
        if (currentBubble) {
            if (isDragging) {
                // Add bounce animation
                currentBubble.classList.add('dropped');
                setTimeout(() => {
                    currentBubble.classList.remove('dropped');
                }, 600);
                
                currentBubble.classList.remove('dragging');
            }
            
            // Reset all variables
            isDragging = false;
            currentBubble = null;
            hasMoved = false;
            
            // Re-enable text selection
            document.body.style.userSelect = '';
        }
    });
    
    // Touch events for mobile
    bubbles.forEach(bubble => {
        bubble.addEventListener('touchstart', function(e) {
            e.preventDefault();
            const touch = e.touches[0];
            isDragging = false; // Don't set to true yet
            hasMoved = false;
            currentBubble = this;
            
            startX = touch.clientX;
            startY = touch.clientY;
            startLeft = parseFloat(this.style.left) || 0;
            startTop = parseFloat(this.style.top) || 0;
        });
        
        // Touch click to search
        bubble.addEventListener('touchend', function(e) {
            if (!hasMoved) { // Only if touch hasn't moved much
                const keyword = this.dataset.keyword;
                const searchUrl = `/search?keyword=${encodeURIComponent(keyword)}`;
                window.open(searchUrl, '_blank');
            }
        });
    });
    
    document.addEventListener('touchmove', function(e) {
        if (currentBubble) {
            const touch = e.touches[0];
            const deltaX = touch.clientX - startX;
            const deltaY = touch.clientY - startY;
            const distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
            
            // Check if touch has moved enough to start dragging
            if (distance > dragThreshold && !isDragging) {
                isDragging = true;
                hasMoved = true;
                currentBubble.classList.add('dragging');
                tooltip.classList.remove('show');
            }
            
            if (isDragging && currentBubble) {
                e.preventDefault();
                
                const containerRect = container.getBoundingClientRect();
                const bubbleSize = currentBubble.offsetWidth;
                
                const newLeft = startLeft + (deltaX / containerRect.width) * 100;
                const newTop = startTop + (deltaY / containerRect.height) * 100;
                
                const minLeft = 0;
                const maxLeft = 100 - (bubbleSize / containerRect.width) * 100;
                const minTop = 0;
                const maxTop = 100 - (bubbleSize / containerRect.height) * 100;
                
                const constrainedLeft = Math.max(minLeft, Math.min(maxLeft, newLeft));
                const constrainedTop = Math.max(minTop, Math.min(maxTop, newTop));
                
                currentBubble.style.left = constrainedLeft + '%';
                currentBubble.style.top = constrainedTop + '%';
            }
        }
    });
    
    document.addEventListener('touchend', function(e) {
        if (currentBubble) {
            if (isDragging) {
                // Add bounce animation
                currentBubble.classList.add('dropped');
                setTimeout(() => {
                    currentBubble.classList.remove('dropped');
                }, 600);
                
                currentBubble.classList.remove('dragging');
            }
            
            // Reset all variables
            isDragging = false;
            currentBubble = null;
            hasMoved = false;
        }
    });
    
    // Add random positioning for better distribution
    bubbles.forEach((bubble, index) => {
        if (index > 0) {
            const randomX = Math.random() * 80 + 10; // 10% to 90%
            const randomY = Math.random() * 60 + 20; // 20% to 80%
            
            bubble.style.left = randomX + '%';
            bubble.style.top = randomY + '%';
        }
    });
    
    // Add floating animation
    bubbles.forEach((bubble, index) => {
        const delay = index * 0.5; // Stagger animation
        bubble.style.animationDelay = delay + 's';
    });
    
    // Reset layout button
    const resetBtn = document.getElementById('resetBubbleLayout');
    if (resetBtn) {
        resetBtn.addEventListener('click', function() {
            bubbles.forEach((bubble, index) => {
                if (index === 0) {
                    // First bubble in center
                    bubble.style.left = '50%';
                    bubble.style.top = '50%';
                } else {
                    // Arrange in a circle
                    const angle = (index - 1) * (2 * Math.PI) / (bubbles.length - 1);
                    const radius = 30; // 30% from center
                    const centerX = 50;
                    const centerY = 50;
                    
                    const x = centerX + radius * Math.cos(angle);
                    const y = centerY + radius * Math.sin(angle);
                    
                    bubble.style.left = x + '%';
                    bubble.style.top = y + '%';
                }
                
                // Add animation
                bubble.style.transition = 'all 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
                setTimeout(() => {
                    bubble.style.transition = '';
                }, 800);
            });
        });
    }
    
    // Shuffle bubbles button
    const shuffleBtn = document.getElementById('shuffleBubbles');
    if (shuffleBtn) {
        shuffleBtn.addEventListener('click', function() {
            bubbles.forEach((bubble, index) => {
                const randomX = Math.random() * 80 + 10; // 10% to 90%
                const randomY = Math.random() * 60 + 20; // 20% to 80%
                
                bubble.style.left = randomX + '%';
                bubble.style.top = randomY + '%';
                
                // Add staggered animation
                bubble.style.transition = 'all 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
                bubble.style.transitionDelay = (index * 0.1) + 's';
                
                setTimeout(() => {
                    bubble.style.transition = '';
                    bubble.style.transitionDelay = '';
                }, 600 + (index * 100));
            });
        });
    }
}

// Initialize bubble chart when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Wait a bit for the page to fully load
    setTimeout(initBubbleChart, 500);
});
