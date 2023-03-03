
var currentRecord = {};
var copyPasteBufferActive = false;
var copyPasteBufferQuality = "";
var copyPasteBufferTags = "";
var copyPasteBufferComments = "";

function XXXXX() {
    alert("XXXXX...");
}

function annoToggleSettings() {
    if (byId("annoSettingsId").classList.contains("is-hidden")) {
        byId("annoBodyId").classList.add("is-hidden");
        byId("annoSettingsId").classList.remove("is-hidden");
        byId("annoShowSettingsTextId").textContent = "Hide settings";
    } else {
        byId("annoSettingsId").classList.add("is-hidden");
        byId("annoBodyId").classList.remove("is-hidden");
        byId("annoShowSettingsTextId").textContent = "Show settings";
    };
}

function annoSourceLoad() {
    getSourceDirs()
}

function annoSourceChanged() {
    var sourceId = byId("annoSelectSourceId").value;
    getNights(sourceId);
}

function annoNightChanged() {
    var sourceId = byId("annoSelectSourceId").value;
    var nightId = byId("annoSelectNightId").value;
    //    var recordId = byId("annoRecordId").value;
    getRecordInfo(sourceId, nightId, "");
}

function annoClearFilter() {
    try {
        byId("annoFilterQ0Id").checked = false;
        byId("annoFilterQ1Id").checked = false;
        byId("annoFilterQ2Id").checked = false;
        byId("annoFilterQ3Id").checked = false;
        byId("annoFilterQNotAssignedId").checked = false;
    } catch (err) {
        // Block of code to handle errors
    }
}

function annoSetFilter() {
    try {
        byId("annoFilterQ0Id").checked = true;
        byId("annoFilterQ1Id").checked = true;
        byId("annoFilterQ2Id").checked = true;
        byId("annoFilterQ3Id").checked = true;
        byId("annoFilterQNotAssignedId").checked = true;
    } catch (err) {
        // Block of code to handle errors
    }
}

function annoToggleViewMetadata() {
    if (byId("annoViewMetadataId").classList.contains("is-hidden")) {
        byId("annoViewMetadataButtonId").classList.add("is-inverted");
        byId("annoViewMetadataId").classList.remove("is-hidden");
    } else {
        byId("annoViewMetadataButtonId").classList.remove("is-inverted");
        byId("annoViewMetadataId").classList.add("is-hidden");
    };
}

// function annoToggleViewOverview() {
//     if (byId("annoViewOverviewId").classList.contains("is-hidden")) {
//         byId("annoViewOverview-buttonId").classList.add("is-inverted");
//         byId("annoViewOverviewId").classList.remove("is-hidden");
//     } else {
//         byId("annoViewOverview-buttonId").classList.remove("is-inverted");
//         byId("annoViewOverviewId").classList.add("is-hidden");
//     };
// }

function annoToggleViewSpectrogram() {
    if (byId("annoViewSpectrogramId").classList.contains("is-hidden")) {
        byId("annoViewSpectrogramButtonId").classList.add("is-inverted");
        byId("annoViewSpectrogramId").classList.remove("is-hidden");
    } else {
        byId("annoViewSpectrogramButtonId").classList.remove("is-inverted");
        byId("annoViewSpectrogramId").classList.add("is-hidden");
    };
}

function annoToggleViewDetails() {
    if (byId("annoViewDetailsId").classList.contains("is-hidden")) {
        byId("annoViewDetailsButtonId").classList.add("is-inverted");
        byId("annoViewDetailsId").classList.remove("is-hidden");
    } else {
        byId("annoViewDetailsButtonId").classList.remove("is-inverted");
        byId("annoViewDetailsId").classList.add("is-hidden");
    };
}

function annoEnableDisableButtons() {
    if (copyPasteBufferActive == true) {
        byId("annoPasteId").disabled = false;
        byId("annoPasteNextId").disabled = false;
    } else {
        byId("annoPasteId").disabled = true;
        byId("annoPasteNextId").disabled = true;
    }
}

function annoFirst() {
    var textContent = byId("annoFirstTextId").textContent;
    if (textContent == "Previous night") {
        optionList = byId("annoSelectNightId");
        optionIndex = optionList.selectedIndex;
        optionList.selectedIndex = optionIndex - 1;
        var sourceId = byId("annoSelectSourceId").value;
        var nightId = byId("annoSelectNightId").value;
        getRecordInfo(sourceId, nightId, "");
    } else {
        var sourceId = byId("annoSelectSourceId").value;
        var nightId = byId("annoSelectNightId").value;
        var recordId = currentRecord.firstRecordId;
        getRecordInfo(sourceId, nightId, recordId);
    }
}
function annoPrevious() {
    var sourceId = byId("annoSelectSourceId").value;
    var nightId = byId("annoSelectNightId").value;
    var recordId = currentRecord.previousRecordId;
    getRecordInfo(sourceId, nightId, recordId);
}
function annoNext() {
    var sourceId = byId("annoSelectSourceId").value;
    var nightId = byId("annoSelectNightId").value;
    var recordId = currentRecord.nextRecordId;
    getRecordInfo(sourceId, nightId, recordId);
}
function annoLast() {
    var textContent = byId("annoLastTextId").textContent;
    if (textContent == "Next night") {
        optionList = byId("annoSelectNightId");
        optionIndex = optionList.selectedIndex;
        optionList.selectedIndex = optionIndex + 1;
        var sourceId = byId("annoSelectSourceId").value;
        var nightId = byId("annoSelectNightId").value;
        getRecordInfo(sourceId, nightId, "");
    } else {
        var sourceId = byId("annoSelectSourceId").value;
        var nightId = byId("annoSelectNightId").value;
        var recordId = currentRecord.lastRecordId;
        getRecordInfo(sourceId, nightId, recordId);
    }
}

function annoSetQ0() {
    byId("annoQ0Id").checked = true;
    annoSaveAnnotations();
}
function annoSetQ1() {
    byId("annoQ1Id").checked = true;
    annoSaveAnnotations();
}
function annoSetQ2() {
    byId("annoQ2Id").checked = true;
    annoSaveAnnotations();
}
function annoSetQ3() {
    byId("annoQ3Id").checked = true;
    annoSaveAnnotations();
}
function annoSetQNotAssigned() {
    byId("annoQNotAssignedId").checked = true;
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
    if (byId("annoQ0Id").checked == true) {
        quality = "Q0";
    }
    else if (byId("annoQ1Id").checked == true) {
        quality = "Q1";
    }
    else if (byId("annoQ2Id").checked == true) {
        quality = "Q2";
    }
    else if (byId("annoQ3Id").checked == true) {
        quality = "Q3";
    }
    else if (byId("annoQNotAssignedId").checked == true) {
        quality = "Not assigned";
    }
    return quality;
}

function annoSetQuality(quality) {
    if (quality == "Q0") {
        byId("annoQ0Id").checked = true;
    }
    else if (quality == "Q1") {
        byId("annoQ1Id").checked = true;
    }
    else if (quality == "Q2") {
        byId("annoQ2Id").checked = true;
    }
    else if (quality == "Q3") {
        byId("annoQ3Id").checked = true;
    }
    else if (quality == "Not assigned") {
        byId("annoQNotAssignedId").checked = true;
    }
}

function annoGetTags() {
    tags = ""
    if (byId("anno-FM-CF-FM-Id").classList.contains("is-inverted")) {
        tags += "FM-CF-FM,"
    }
    if (byId("anno-FM-Id").classList.contains("is-inverted")) {
        tags += "FM,"
    }
    if (byId("anno-FM-QCF-Id").classList.contains("is-inverted")) {
        tags += "FM-QCF,"
    }
    if (byId("anno-QCF-Id").classList.contains("is-inverted")) {
        tags += "QCF,"
    }
    if (byId("anno-FM+H2-Id").classList.contains("is-inverted")) {
        tags += "FM+H2,"
    }
    if (byId("anno-QCF+FM-Id").classList.contains("is-inverted")) {
        tags += "QCF+FM,"
    }

    if (byId("anno-Social-Id").classList.contains("is-inverted")) {
        tags += "Social,"
    }
    if (byId("anno-Birds-Id").classList.contains("is-inverted")) {
        tags += "Birds,"
    }
    if (byId("anno-Mammals-Id").classList.contains("is-inverted")) {
        tags += "Mammals,"
    }
    if (byId("anno-Crickets-Id").classList.contains("is-inverted")) {
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
        byId("anno-FM-CF-FM-Id").classList.add("is-inverted")
    } else {
        byId("anno-FM-CF-FM-Id").classList.remove("is-inverted")
    }
    if (tags_as_str.includes(",FM,")) {
        byId("anno-FM-Id").classList.add("is-inverted")
    } else {
        byId("anno-FM-Id").classList.remove("is-inverted")
    }
    if (tags_as_str.includes(",FM-QCF,")) {
        byId("anno-FM-QCF-Id").classList.add("is-inverted")
    } else {
        byId("anno-FM-QCF-Id").classList.remove("is-inverted")
    }
    if (tags_as_str.includes(",QCF,")) {
        byId("anno-QCF-Id").classList.add("is-inverted")
    } else {
        byId("anno-QCF-Id").classList.remove("is-inverted")
    }
    if (tags_as_str.includes(",FM+H2,")) {
        byId("anno-FM+H2-Id").classList.add("is-inverted")
    } else {
        byId("anno-FM+H2-Id").classList.remove("is-inverted")
    }
    if (tags_as_str.includes(",QCF+FM,")) {
        byId("anno-QCF+FM-Id").classList.add("is-inverted")
    } else {
        byId("anno-QCF+FM-Id").classList.remove("is-inverted")
    }

    if (tags_as_str.includes(",Social,")) {
        byId("anno-Social-Id").classList.add("is-inverted")
    } else {
        byId("anno-Social-Id").classList.remove("is-inverted")
    }
    if (tags_as_str.includes(",Birds,")) {
        byId("anno-Birds-Id").classList.add("is-inverted")
    } else {
        byId("anno-Birds-Id").classList.remove("is-inverted")
    }
    if (tags_as_str.includes(",Mammals,")) {
        byId("anno-Mammals-Id").classList.add("is-inverted")
    } else {
        byId("anno-Mammals-Id").classList.remove("is-inverted")
    }
    if (tags_as_str.includes(",Crickets,")) {
        byId("anno-Crickets-Id").classList.add("is-inverted")
    } else {
        byId("anno-Crickets-Id").classList.remove("is-inverted")
    }
}

function annoGetComments() {
    var comments = byId("annoCommentsId").value
    return comments;
}

function annoSetComments(comment) {
    byId("annoCommentsId").value = comment
}
