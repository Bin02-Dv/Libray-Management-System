function showToast(message, type = "success") {
    const icons = {
        success: "fa-check-circle",
        error: "fa-times-circle",
        info: "fa-info-circle",
        warning: "fa-exclamation-circle"
    };

    let toast = $(`
        <div class="toast ${type}">
            <i class="fa ${icons[type]}"></i>
            <span>${message}</span>
        </div>
    `);

    $("#toast-container").append(toast);

    // Remove toast after animation ends
    setTimeout(() => {
        toast.fadeOut(500, function() {
            $(this).remove();
        });
    }, 4000);
}