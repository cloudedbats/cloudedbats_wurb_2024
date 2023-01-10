
function XXXXX() {
    alert("XXXXX...");
}

function annoFolderChanged() {
    $("#anno-select-night-id").val("select");
}

function annoNightChanged() {
    var value = $("#anno-select-night-id").val();
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
function annoSetQ04() {
    $("#anno-q4-id").prop("checked", true);
}
function annoSetQNA() {
    $("#anno-not-assigned-id").prop("checked", true);
}

