
function XXXXX() {
    alert("XXXXX...");
}

function annoToggleSettings() {
    if ($("#anno-settings-id").hasClass("is-hidden")) {
        $("#anno-boddy-id").addClass("is-hidden")
        $("#anno-settings-id").removeClass("is-hidden")
        $("#anno-show-settings-text-id").text("Hide settings")
    } else {
        $("#anno-settings-id").addClass("is-hidden")
        $("#anno-boddy-id").removeClass("is-hidden")
        $("#anno-show-settings-text-id").text("Show settings")
    };
}

function annoFolderChanged() {
    $("#anno-select-event-id").val("select");
    getEventsDirs()
}

function annoNightChanged() {
    var value = $("#anno-select-event-id").val();
    getRecordingInfo()
    alert("TEST: " + value);
}

function annoClearFilter() {
    try {
        $("#anno-filter-q0-id").prop("checked", false);
        $("#anno-filter-q1-id").prop("checked", false);
        $("#anno-filter-q2-id").prop("checked", false);
        $("#anno-filter-q3-id").prop("checked", false);
        $("#anno-filter-not-assigned-id").prop("checked", false);
    } catch (err) {
        // Block of code to handle errors
    }
}

function annoSetFilter() {
    try {
        $("#anno-filter-q0-id").prop("checked", true);
        $("#anno-filter-q1-id").prop("checked", true);
        $("#anno-filter-q2-id").prop("checked", true);
        $("#anno-filter-q3-id").prop("checked", true);
        $("#anno-filter-not-assigned-id").prop("checked", true);
    } catch (err) {
        // Block of code to handle errors
    }
}

function annoToggleViewFiles() {
    if ($("#anno-view-files-id").hasClass("is-hidden")) {
        $("#anno-view-files-button-id").addClass("is-inverted");
        $("#anno-view-files-id").removeClass("is-hidden")
    } else {
        $("#anno-view-files-button-id").removeClass("is-inverted");
        $("#anno-view-files-id").addClass("is-hidden")
    };
}

function annoToggleViewOverview() {
    if ($("#anno-view-overview-id").hasClass("is-hidden")) {
        $("#anno-view-overview-button-id").addClass("is-inverted");
        $("#anno-view-overview-id").removeClass("is-hidden")
    } else {
        $("#anno-view-overview-button-id").removeClass("is-inverted");
        $("#anno-view-overview-id").addClass("is-hidden")
    };
}

function annoToggleViewSpectrogram() {
    if ($("#anno-view-spectrogram-id").hasClass("is-hidden")) {
        $("#anno-view-spectrogram-button-id").addClass("is-inverted");
        $("#anno-view-spectrogram-id").removeClass("is-hidden")
    } else {
        $("#anno-view-spectrogram-button-id").removeClass("is-inverted");
        $("#anno-view-spectrogram-id").addClass("is-hidden")
    };
}

function annoToggleViewDetails() {
    if ($("#anno-view-details-id").hasClass("is-hidden")) {
        $("#anno-view-details-button-id").addClass("is-inverted");
        $("#anno-view-details-id").removeClass("is-hidden")
    } else {
        $("#anno-view-details-button-id").removeClass("is-inverted");
        $("#anno-view-details-id").addClass("is-hidden")
    };
}

function annoFirst() {
    alert("annoFirst...");
}
function annoPrevious() {
    alert("annoPrevious...");
}
function annoNext() {
    alert("annoNext...");
}
function annoLast() {
    alert("annoLast...");
}

function annoSetQ0() {
    $("#anno-q0-id").prop("checked", true);
}
function annoSetQ1() {
    $("#anno-q1-id").prop("checked", true);
}
function annoSetQ2() {
    $("#anno-q2-id").prop("checked", true);
}
function annoSetQ03() {
    $("#anno-q3-id").prop("checked", true);
}
function annoSetQNotAssigned() {
    $("#anno-not-assigned-id").prop("checked", true);
}
function annoQuickClear() {
    $("#anno-not-assigned-id").prop("checked", true);
    // TODO: Clear settings.
}
function annoQuickCopy() {
    alert("annoQuickCopy...");
}
function annoQuickPaste() {
    alert("annoQuickPaste...");
}
function annoQuickPasteNext() {
    alert("annoQuickPasteNext...");
}



function toggleTag(tagObject) {
    if ($(tagObject).hasClass("is-inverted")) {
        $(tagObject).removeClass("is-inverted")
    } else {
        $(tagObject).addClass("is-inverted");
     };
}
