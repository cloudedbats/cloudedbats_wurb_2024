
function XXXXX() {
    alert("XXXXX...");
}

function annoToggleSettings() {
    if (byId("anno-settings-id").classList.contains("is-hidden")) {
        byId("anno-boddy-id").classList.add("is-hidden")
        byId("anno-settings-id").classList.remove("is-hidden")
        byId("anno-show-settings-text-id").textContent = "Hide settings"
    } else {
        byId("anno-settings-id").classList.add("is-hidden")
        byId("anno-boddy-id").classList.remove("is-hidden")
        byId("anno-show-settings-text-id").textContent = "Show settings"
    };
}

function annoSourceLoad() {
    getSourceDirs()
}

function annoSourceChanged() {
    var sourceId = byId("anno-select-source-id").value;
    getNights(sourceId);
}

function annoNightChanged() {
    var sourceId = byId("anno-select-source-id").value;
    var nightId = byId("anno-select-night-id").value;
    //    var recordId = byId("anno-record-id").value;
    getRecordInfo(sourceId, nightId, "");
}

function annoClearFilter() {
    try {
        byId("anno-filter-q0-id").checked = false;
        byId("anno-filter-q1-id").checked = false;
        byId("anno-filter-q2-id").checked = false;
        byId("anno-filter-q3-id").checked = false;
        byId("anno-filter-not-assigned-id").checked = false;
    } catch (err) {
        // Block of code to handle errors
    }
}

function annoSetFilter() {
    try {
        byId("anno-filter-q0-id").checked = true;
        byId("anno-filter-q1-id").checked = true;
        byId("anno-filter-q2-id").checked = true;
        byId("anno-filter-q3-id").checked = true;
        byId("anno-filter-not-assigned-id").checked = true;
    } catch (err) {
        // Block of code to handle errors
    }
}

function annoToggleViewFiles() {
    if (byId("anno-view-files-id").classList.contains("is-hidden")) {
        byId("anno-view-files-button-id").classList.add("is-inverted");
        byId("anno-view-files-id").classList.remove("is-hidden")
    } else {
        byId("anno-view-files-button-id").classList.remove("is-inverted");
        byId("anno-view-files-id").classList.add("is-hidden")
    };
}

function annoToggleViewOverview() {
    if (byId("anno-view-overview-id").classList.contains("is-hidden")) {
        byId("anno-view-overview-button-id").classList.add("is-inverted");
        byId("anno-view-overview-id").classList.remove("is-hidden")
    } else {
        byId("anno-view-overview-button-id").classList.remove("is-inverted");
        byId("anno-view-overview-id").classList.add("is-hidden")
    };
}

function annoToggleViewSpectrogram() {
    if (byId("anno-view-spectrogram-id").classList.contains("is-hidden")) {
        byId("anno-view-spectrogram-button-id").classList.add("is-inverted");
        byId("anno-view-spectrogram-id").classList.remove("is-hidden")
    } else {
        byId("anno-view-spectrogram-button-id").classList.remove("is-inverted");
        byId("anno-view-spectrogram-id").classList.add("is-hidden")
    };
}

function annoToggleViewDetails() {
    if (byId("anno-view-details-id").classList.contains("is-hidden")) {
        byId("anno-view-details-button-id").classList.add("is-inverted");
        byId("anno-view-details-id").classList.remove("is-hidden")
    } else {
        byId("anno-view-details-button-id").classList.remove("is-inverted");
        byId("anno-view-details-id").classList.add("is-hidden")
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
    byId("anno-q0-id").checked = true;
}
function annoSetQ1() {
    byId("anno-q1-id").checked = true;
}
function annoSetQ2() {
    byId("anno-q2-id").checked = true;
}
function annoSetQ3() {
    byId("anno-q3-id").checked = true;
}
function annoSetQNotAssigned() {
    byId("anno-not-assigned-id").checked = true;
}
function annoQuickClear() {
    byId("anno-not-assigned-id").checked = true;
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
    if (tagObject.classList.contains("is-inverted")) {
        tagObject.classList.remove("is-inverted")
    } else {
        tagObject.classList.add("is-inverted");
    };
}
