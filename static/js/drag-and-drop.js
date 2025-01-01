document.addEventListener('DOMContentLoaded', () => {
    const uploadContainer = document.getElementById('upload-container');
    const fileInput = document.getElementById('file-input');
    const uploadForm = document.getElementById('upload-form');
    const processButton = document.getElementById('process-btn');

    let uploadedFile = null;

    // Drag-and-Drop Events
    uploadContainer.addEventListener('dragover', (e) => {
        e.preventDefault();
        e.stopPropagation();
        uploadContainer.style.backgroundColor = '#f1f1f1';
    });

    uploadContainer.addEventListener('dragleave', (e) => {
        e.preventDefault();
        e.stopPropagation();
        uploadContainer.style.backgroundColor = '';
    });

    uploadContainer.addEventListener('drop', (e) => {
        e.preventDefault();
        e.stopPropagation();
        uploadContainer.style.backgroundColor = '';

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            uploadedFile = files[0];
            uploadContainer.textContent = `File Ready: ${uploadedFile.name}`;
        }
    });

    // File Input Selector
    uploadContainer.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', (e) => {
        const files = e.target.files;
        if (files.length > 0) {
            uploadedFile = files[0];
            uploadContainer.textContent = `File Ready: ${uploadedFile.name}`;
        }
    });

    // Process Button
    processButton.addEventListener('click', () => {
        if (!uploadedFile) {
            alert('Please upload a file first.');
            return;
        }

        const formData = new FormData(uploadForm);
        formData.append('file', uploadedFile);

        fetch('/drag-upload', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Image processed successfully!');
                window.location.href = `/download/${data.filename}`;
            } else {
                throw new Error(data.error || 'Unknown error');
            }
        })
        .catch(error => {
            console.error(error);
            alert('Error processing image. Please try again.');
        });
    });
});
