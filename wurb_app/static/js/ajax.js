
function fetchAjaxRecord() {
    $("#ajax-record-id").addClass("is-inverted");
    $("#ajax-live-id").addClass("is-inverted");
    $("#ajax-annotations-id").addClass("is-inverted");
    $("#ajax-files-id").addClass("is-inverted");

    $.ajax({
        // url: '/status/{{ uid }}',
        url: '/ajax-record/',
        type: 'get',
        success: function (data) {
            $("#hero-body-id").html(data);
            $("#ajax-record-id").removeClass("is-inverted");
        },
        error: function (xhr, status, error) {
            var errorMessage = xhr.status + ': ' + xhr.statusText
            alert('AJAX error: ' + errorMessage);
        }
    });
}

function fetchAjaxLive() {
    $("#ajax-record-id").addClass("is-inverted");
    $("#ajax-live-id").addClass("is-inverted");
    $("#ajax-annotations-id").addClass("is-inverted");
    $("#ajax-files-id").addClass("is-inverted");

    $.ajax({
        // url: '/status/{{ uid }}',
        url: '/ajax-live/',
        type: 'get',
        success: function (data) {
            $("#hero-body-id").html(data);
            $("#ajax-live-id").removeClass("is-inverted");
        },
        error: function (xhr, status, error) {
            var errorMessage = xhr.status + ': ' + xhr.statusText
            alert('AJAX error: ' + errorMessage);
        }
    });
}

function fetchAjaxAnnotations() {
    $("#ajax-record-id").addClass("is-inverted");
    $("#ajax-live-id").addClass("is-inverted");
    $("#ajax-annotations-id").addClass("is-inverted");
    $("#ajax-files-id").addClass("is-inverted");

    $.ajax({
        // url: '/status/{{ uid }}',
        url: '/ajax-annotations/',
        type: 'get',
        success: function (data) {
            $("#hero-body-id").html(data);
            $("#ajax-annotations-id").removeClass("is-inverted");
        },
        error: function (xhr, status, error) {
            var errorMessage = xhr.status + ': ' + xhr.statusText
            alert('AJAX error: ' + errorMessage);
        }
    });
}

function fetchAjaxFiles() {
    $("#ajax-record-id").addClass("is-inverted");
    $("#ajax-live-id").addClass("is-inverted");
    $("#ajax-annotations-id").addClass("is-inverted");
    $("#ajax-files-id").addClass("is-inverted");

    $.ajax({
        // url: '/status/{{ uid }}',
        url: '/ajax-files/',
        type: 'get',
        success: function (data) {
            $("#hero-body-id").html(data);
            $("#ajax-files-id").removeClass("is-inverted");
        },
        error: function (xhr, status, error) {
            var errorMessage = xhr.status + ': ' + xhr.statusText
            alert('AJAX error: ' + errorMessage);
        }
    });
}

function fetchAjaxAbout() {
    $("#ajax-record-id").addClass("is-inverted");
    $("#ajax-live-id").addClass("is-inverted");
    $("#ajax-annotations-id").addClass("is-inverted");
    $("#ajax-files-id").addClass("is-inverted");

    $.ajax({
        // url: '/status/{{ uid }}',
        url: '/ajax-about/',
        type: 'get',
        success: function (data) {
            $("#hero-body-id").html(data);
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


