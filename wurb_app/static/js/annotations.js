
var currentRecord = {};
var copyPasteBufferActive = false;
var copyPasteBufferQuality = "";
var copyPasteBufferTags = "";
var copyPasteBufferComments = "";

function XXXXX() {
    alert("XXXXX...");
}

function annoToggleSettings() {
    if (byId("anno-settings-id").classList.contains("is-hidden")) {
        byId("anno-boddy-id").classList.add("is-hidden");
        byId("anno-settings-id").classList.remove("is-hidden");
        byId("anno-show-settings-text-id").textContent = "Hide settings";
    } else {
        byId("anno-settings-id").classList.add("is-hidden");
        byId("anno-boddy-id").classList.remove("is-hidden");
        byId("anno-show-settings-text-id").textContent = "Show settings";
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

function annoToggleViewMetadata() {
    if (byId("anno-view-metadata-id").classList.contains("is-hidden")) {
        byId("anno-view-metadata-button-id").classList.add("is-inverted");
        byId("anno-view-metadata-id").classList.remove("is-hidden");
    } else {
        byId("anno-view-metadata-button-id").classList.remove("is-inverted");
        byId("anno-view-metadata-id").classList.add("is-hidden");
    };
}

// function annoToggleViewOverview() {
//     if (byId("anno-view-overview-id").classList.contains("is-hidden")) {
//         byId("anno-view-overview-button-id").classList.add("is-inverted");
//         byId("anno-view-overview-id").classList.remove("is-hidden");
//     } else {
//         byId("anno-view-overview-button-id").classList.remove("is-inverted");
//         byId("anno-view-overview-id").classList.add("is-hidden");
//     };
// }

function annoToggleViewSpectrogram() {
    if (byId("anno-view-spectrogram-id").classList.contains("is-hidden")) {
        byId("anno-view-spectrogram-button-id").classList.add("is-inverted");
        byId("anno-view-spectrogram-id").classList.remove("is-hidden");
    } else {
        byId("anno-view-spectrogram-button-id").classList.remove("is-inverted");
        byId("anno-view-spectrogram-id").classList.add("is-hidden");
    };
}

function annoToggleViewDetails() {
    if (byId("anno-view-details-id").classList.contains("is-hidden")) {
        byId("anno-view-details-button-id").classList.add("is-inverted");
        byId("anno-view-details-id").classList.remove("is-hidden");
    } else {
        byId("anno-view-details-button-id").classList.remove("is-inverted");
        byId("anno-view-details-id").classList.add("is-hidden");
    };
}

function annoEnableDisableButtons() {
    if (copyPasteBufferActive == true) {
        byId("anno-paste-id").disabled = false;
        byId("anno-paste-next-id").disabled = false;
    } else {
        byId("anno-paste-id").disabled = true;
        byId("anno-paste-next-id").disabled = true;
    }
}

function annoFirst() {
    var textContent = byId("anno-first-id").textContent;
    if (textContent == "Previous night") {
        optionList = byId("anno-select-night-id");
        optionIndex = optionList.selectedIndex;
        optionList.selectedIndex = optionIndex - 1;
        var sourceId = byId("anno-select-source-id").value;
        var nightId = byId("anno-select-night-id").value;
        getRecordInfo(sourceId, nightId, "");
    } else {
        var sourceId = byId("anno-select-source-id").value;
        var nightId = byId("anno-select-night-id").value;
        var recordId = currentRecord.firstRecordId;
        getRecordInfo(sourceId, nightId, recordId);
    }
}
function annoPrevious() {
    var sourceId = byId("anno-select-source-id").value;
    var nightId = byId("anno-select-night-id").value;
    var recordId = currentRecord.previousRecordId;
    getRecordInfo(sourceId, nightId, recordId);
}
function annoNext() {
    var sourceId = byId("anno-select-source-id").value;
    var nightId = byId("anno-select-night-id").value;
    var recordId = currentRecord.nextRecordId;
    getRecordInfo(sourceId, nightId, recordId);
}
function annoLast() {
    var textContent = byId("anno-last-id").textContent;
    if (textContent == "Next night") {
        optionList = byId("anno-select-night-id");
        optionIndex = optionList.selectedIndex;
        optionList.selectedIndex = optionIndex + 1;
        var sourceId = byId("anno-select-source-id").value;
        var nightId = byId("anno-select-night-id").value;
        getRecordInfo(sourceId, nightId, "");
    } else {
        var sourceId = byId("anno-select-source-id").value;
        var nightId = byId("anno-select-night-id").value;
        var recordId = currentRecord.lastRecordId;
        getRecordInfo(sourceId, nightId, recordId);
    }
}

function annoSetQ0() {
    byId("anno-q0-id").checked = true;
    annoSaveAnnotations();
}
function annoSetQ1() {
    byId("anno-q1-id").checked = true;
    annoSaveAnnotations();
}
function annoSetQ2() {
    byId("anno-q2-id").checked = true;
    annoSaveAnnotations();
}
function annoSetQ3() {
    byId("anno-q3-id").checked = true;
    annoSaveAnnotations();
}
function annoSetQNotAssigned() {
    byId("anno-not-assigned-id").checked = true;
    annoSaveAnnotations();
}
function toggleTag(tagObject) {
    if (tagObject.classList.contains("is-inverted")) {
        tagObject.classList.remove("is-inverted");
    } else {
        tagObject.classList.add("is-inverted");
    };
    tags_as_str = annoGetTags()
    annoSaveAnnotations();
}

function annoQuickClear() {
    annoSetQuality("Not assigned");
    annoSetTags("");
    annoSetComments("");
    annoSaveAnnotations();
    // copyPasteBufferActive = false;
    // copyPasteBufferQuality = "";
    // copyPasteBufferTags = "";
    // copyPasteBufferComments = "";
    // annoEnableDisableButtons();

}
function annoQuickCopy() {
    annoCopyAnnotations();
    copyPasteBufferActive = true;
    annoEnableDisableButtons();
}
function annoQuickPaste() {
    annoPasteAnnotations();
    annoSaveAnnotations();
}
function annoQuickPasteNext() {
    annoPasteAnnotations();
    annoSaveAnnotations();
    annoNext();
}

function annoSaveAnnotations() {
    var sourceId = currentRecord.sourceId;
    var nightId = currentRecord.nightId;
    var recordId = currentRecord.recordId;
    var quality = annoGetQuality();
    var tags = annoGetTags();
    var comments = annoGetComments();
    saveRecordInfo(sourceId, nightId, recordId, quality, tags, comments)
}

function annoCopyAnnotations() {
    copyPasteBufferQuality = annoGetQuality();
    copyPasteBufferTags = annoGetTags();
    copyPasteBufferComments = annoGetComments();
    copyPasteBufferActive = true;
}

function annoPasteAnnotations() {
    annoSetQuality(copyPasteBufferQuality);
    annoSetTags(copyPasteBufferTags);
    annoSetComments(copyPasteBufferComments);
}

function annoGetQuality() {
    var quality = ""
    if (byId("anno-q0-id").checked == true) {
        quality = "Q0";
    }
    else if (byId("anno-q1-id").checked == true) {
        quality = "Q1";
    }
    else if (byId("anno-q2-id").checked == true) {
        quality = "Q2";
    }
    else if (byId("anno-q3-id").checked == true) {
        quality = "Q3";
    }
    else if (byId("anno-not-assigned-id").checked == true) {
        quality = "Not assigned";
    }
    return quality;
}

function annoSetQuality(quality) {
    if (quality == "Q0") {
        byId("anno-q0-id").checked = true;
    }
    else if (quality == "Q1") {
        byId("anno-q1-id").checked = true;
    }
    else if (quality == "Q2") {
        byId("anno-q2-id").checked = true;
    }
    else if (quality == "Q3") {
        byId("anno-q3-id").checked = true;
    }
    else if (quality == "Not assigned") {
        byId("anno-not-assigned-id").checked = true;
    }
}

function annoGetTags() {
    tags = ""
    if (byId("anno-FM-CF-FM-id").classList.contains("is-inverted")) {
        tags += "FM-CF-FM,"
    }
    if (byId("anno-FM-id").classList.contains("is-inverted")) {
        tags += "FM,"
    }
    if (byId("anno-FM-QCF-id").classList.contains("is-inverted")) {
        tags += "FM-QCF,"
    }
    if (byId("anno-QCF-id").classList.contains("is-inverted")) {
        tags += "QCF,"
    }
    if (byId("anno-FM+H2-id").classList.contains("is-inverted")) {
        tags += "FM+H2,"
    }
    if (byId("anno-QCF+FM-id").classList.contains("is-inverted")) {
        tags += "QCF+FM,"
    }

    if (byId("anno-Social-id").classList.contains("is-inverted")) {
        tags += "Social,"
    }
    if (byId("anno-Birds-id").classList.contains("is-inverted")) {
        tags += "Birds,"
    }
    if (byId("anno-Mammals-id").classList.contains("is-inverted")) {
        tags += "Mammals,"
    }
    if (byId("anno-Crickets-id").classList.contains("is-inverted")) {
        tags += "Crickets,"
    }
    if (tags.length > 1) {
        tags = tags.substring(0, tags.length - 1)
    }
    return tags;
}

function annoSetTags(tags_as_str) {
    // Add trailing/leading , for compare strings.
    tags_as_str = "," + tags_as_str + ","
    if (tags_as_str.includes(",FM-CF-FM,")) {
        byId("anno-FM-CF-FM-id").classList.add("is-inverted")
    } else {
        byId("anno-FM-CF-FM-id").classList.remove("is-inverted")
    }
    if (tags_as_str.includes(",FM,")) {
        byId("anno-FM-id").classList.add("is-inverted")
    } else {
        byId("anno-FM-id").classList.remove("is-inverted")
    }
    if (tags_as_str.includes(",FM-QCF,")) {
        byId("anno-FM-QCF-id").classList.add("is-inverted")
    } else {
        byId("anno-FM-QCF-id").classList.remove("is-inverted")
    }
    if (tags_as_str.includes(",QCF,")) {
        byId("anno-QCF-id").classList.add("is-inverted")
    } else {
        byId("anno-QCF-id").classList.remove("is-inverted")
    }
    if (tags_as_str.includes(",FM+H2,")) {
        byId("anno-FM+H2-id").classList.add("is-inverted")
    } else {
        byId("anno-FM+H2-id").classList.remove("is-inverted")
    }
    if (tags_as_str.includes(",QCF+FM,")) {
        byId("anno-QCF+FM-id").classList.add("is-inverted")
    } else {
        byId("anno-QCF+FM-id").classList.remove("is-inverted")
    }

    if (tags_as_str.includes(",Social,")) {
        byId("anno-Social-id").classList.add("is-inverted")
    } else {
        byId("anno-Social-id").classList.remove("is-inverted")
    }
    if (tags_as_str.includes(",Birds,")) {
        byId("anno-Birds-id").classList.add("is-inverted")
    } else {
        byId("anno-Birds-id").classList.remove("is-inverted")
    }
    if (tags_as_str.includes(",Mammals,")) {
        byId("anno-Mammals-id").classList.add("is-inverted")
    } else {
        byId("anno-Mammals-id").classList.remove("is-inverted")
    }
    if (tags_as_str.includes(",Crickets,")) {
        byId("anno-Crickets-id").classList.add("is-inverted")
    } else {
        byId("anno-Crickets-id").classList.remove("is-inverted")
    }
}

function annoGetComments() {
    var comments = byId("anno-comments-id").value
    return comments;
}

function annoSetComments(comment) {
    byId("anno-comments-id").value = comment
}
