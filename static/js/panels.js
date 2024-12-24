document.addEventListener('DOMContentLoaded', () => {
    const rightPanel = document.querySelector('.right-panel');
    const leftPanel = document.querySelector('.left-panel');
    const resizeHandleLeft = document.querySelector('.resize-handle-left');
    const resizeHandleRight = document.querySelector('.resize-handle-right');

    let isResizingRight = false;
    let isResizingLeft = false;

    const handleResize = (e, panel, isRight) => {
        const newWidth = isRight ? window.innerWidth - e.clientX : e.clientX;
        if (newWidth >= 200 && newWidth <= 600) {
            panel.style.width = newWidth + 'px';
        }
    };

    resizeHandleRight.addEventListener('mousedown', (e) => {
        isResizingRight = true;
        document.body.style.cursor = 'ew-resize';
        e.preventDefault();
    });

    resizeHandleLeft.addEventListener('mousedown', (e) => {
        isResizingLeft = true;
        document.body.style.cursor = 'ew-resize';
        e.preventDefault();
    });

    document.addEventListener('mousemove', (e) => {
        if (isResizingRight) handleResize(e, rightPanel, true);
        if (isResizingLeft) handleResize(e, leftPanel, false);
    });

    document.addEventListener('mouseup', () => {
        isResizingRight = false;
        isResizingLeft = false;
        document.body.style.cursor = 'default';
    });
});

