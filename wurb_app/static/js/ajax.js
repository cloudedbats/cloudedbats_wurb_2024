
function clearButtonsForAjax() {
    $("#ajax-record-id").removeClass("is-inverted");
    $("#ajax-live-id").removeClass("is-inverted");
    $("#ajax-annotations-id").removeClass("is-inverted");
    $("#ajax-adm-id").removeClass("is-inverted");
    // $("#ajax-record-id").addClass("is-inverted");
    // $("#ajax-live-id").addClass("is-inverted");
    // $("#ajax-annotations-id").addClass("is-inverted");
    // $("#ajax-adm-id").addClass("is-inverted");
}

function fetchAjaxRecord() {
    clearButtonsForAjax()
    $.ajax({
        // url: '/status/{{ uid }}',
        url: '/ajax-record/',
        type: 'get',
        success: function (data) {
            $("#hero-body-id").html(data);
            $("#ajax-record-id").addClass("is-inverted");
        },
        error: function (xhr, status, error) {
            var errorMessage = xhr.status + ': ' + xhr.statusText
            alert('AJAX error: ' + errorMessage);
        }
    });
}

function fetchAjaxLive() {
    clearButtonsForAjax()
    $.ajax({
        // url: '/status/{{ uid }}',
        url: '/ajax-live/',
        type: 'get',
        success: function (data) {
            $("#hero-body-id").html(data);
            $("#ajax-live-id").addClass("is-inverted");
        },
        error: function (xhr, status, error) {
            var errorMessage = xhr.status + ': ' + xhr.statusText
            alert('AJAX error: ' + errorMessage);
        }
    });
}

function fetchAjaxAnnotations() {
    clearButtonsForAjax()
    $.ajax({
        // url: '/status/{{ uid }}',
        url: '/ajax-annotations/',
        type: 'get',
        success: function (data) {
            $("#hero-body-id").html(data);
            $("#ajax-annotations-id").addClass("is-inverted");
        },
        error: function (xhr, status, error) {
            var errorMessage = xhr.status + ': ' + xhr.statusText
            alert('AJAX error: ' + errorMessage);
        }
    });
}

function fetchAjaxAdministration() {
    clearButtonsForAjax()
    $.ajax({
        // url: '/status/{{ uid }}',
        url: '/ajax-admin/',
        type: 'get',
        success: function (data) {
            $("#hero-body-id").html(data);
            $("#ajax-adm-id").addClass("is-inverted");
        },
        error: function (xhr, status, error) {
            var errorMessage = xhr.status + ': ' + xhr.statusText
            alert('AJAX error: ' + errorMessage);
        }
    });
}

function fetchAjaxAbout() {
    clearButtonsForAjax()
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


