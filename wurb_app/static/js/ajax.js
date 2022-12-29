
function fetchAjaxRecord() {
    $.ajax({
        // url: '/status/{{ uid }}',
        url: '/ajax-record/',
        type: 'get',
        success: function (data) {
            $("#id-hero-body").html(data);
        },
        error: function (xhr, status, error) {
            var errorMessage = xhr.status + ': ' + xhr.statusText
            alert('AJAX error: ' + errorMessage);
        }
    });
}

function fetchAjaxLive() {
    $.ajax({
        // url: '/status/{{ uid }}',
        url: '/ajax-live/',
        type: 'get',
        success: function (data) {
            $("#id-hero-body").html(data);
        },
        error: function (xhr, status, error) {
            var errorMessage = xhr.status + ': ' + xhr.statusText
            alert('AJAX error: ' + errorMessage);
        }
    });
}

function fetchAjaxAnnotations() {
    $.ajax({
        // url: '/status/{{ uid }}',
        url: '/ajax-annotations/',
        type: 'get',
        success: function (data) {
            $("#id-hero-body").html(data);
        },
        error: function (xhr, status, error) {
            var errorMessage = xhr.status + ': ' + xhr.statusText
            alert('AJAX error: ' + errorMessage);
        }
    });
}

function fetchAjaxFiles() {
    $.ajax({
        // url: '/status/{{ uid }}',
        url: '/ajax-files/',
        type: 'get',
        success: function (data) {
            $("#id-hero-body").html(data);
        },
        error: function (xhr, status, error) {
            var errorMessage = xhr.status + ': ' + xhr.statusText
            alert('AJAX error: ' + errorMessage);
        }
    });
}

function fetchAjaxAbout() {
    $.ajax({
        // url: '/status/{{ uid }}',
        url: '/ajax-about/',
        type: 'get',
        success: function (data) {
            $("#id-hero-body").html(data);
        },
        error: function (xhr, status, error) {
            var errorMessage = xhr.status + ': ' + xhr.statusText
            alert('AJAX error: ' + errorMessage);
        }
    });
}

// $(document).ready(function () {
//     setTimeout(fetch_ajax_about, 1000);
// });


