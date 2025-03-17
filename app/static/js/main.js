/**
 * EduVision - Simplified Lecture Notes Organizer
 * Main JavaScript file
 */

document.addEventListener('DOMContentLoaded', function() {
    // File input validation
    const fileInput = document.getElementById('file');
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            validateFileInput(this);
        });
    }

    // Initialize any tooltips
    initializeTooltips();
});

/**
 * Validates the file input to ensure only allowed extensions are uploaded
 */
function validateFileInput(input) {
    const allowedExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf'];
    const fileName = input.value;

    if (fileName) {
        const fileExtension = fileName.substring(fileName.lastIndexOf('.')).toLowerCase();

        if (!allowedExtensions.includes(fileExtension)) {
            alert('Sorry, only JPG, JPEG, PNG, GIF, and PDF files are allowed.');
            input.value = '';
            return false;
        }

        // Check file size (max 16MB)
        if (input.files[0].size > 16 * 1024 * 1024) {
            alert('File size cannot exceed 16MB.');
            input.value = '';
            return false;
        }
    }

    return true;
}

/**
 * Initializes Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}