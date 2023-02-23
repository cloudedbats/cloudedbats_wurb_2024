

async function getSourceDirs() {
    // fetch("/module-admin/get-rec-sources", { method: "GET" })
    fetch("/annotations/sources", { method: "GET" })
        .then(function (response) {
            if (response.ok) {
                return response.json();
            } else {
                return Promise.reject(response);
            }
        })
        .then(function (json) {
            // Populate options to select list.
            var select = byId("anno-select-source-id");
            // Empty.
            while (select.firstChild) {
                select.removeChild(select.firstChild);
            }
            // Add first option.
            var option = document.createElement("option");
            option.textContent = "Select:";
            option.value = "select";
            select.appendChild(option);
            // Use received json.
            for (var i = 0; i < json.length; i++) {
                var content = json[i];
                var option = document.createElement("option");
                option.textContent = content.name;
                option.value = content.id;
                select.appendChild(option);
            }
        })
        .catch(function (err) {
            console.warn("Something went wrong.", err);
        })
};

async function getNights(sourceId) {
    fetch("/annotations/nights?" + new URLSearchParams({
        sourceId: sourceId,
    }), { method: "GET" })
        .then(function (response) {
            if (response.ok) {
                return response.json();
            } else {
                return Promise.reject(response);
            }
        })
        .then(function (json) {
            // Populate options to select list.
            var select = byId("anno-select-night-id");
            // Empty.
            while (select.firstChild) {
                select.removeChild(select.firstChild);
            }
            // Add first option.
            var option = document.createElement("option");
            option.textContent = "Select:";
            option.value = "select";
            select.appendChild(option);
            // Use received json.
            for (var i = 0; i < json.length; i++) {
                var content = json[i];
                var option = document.createElement("option");
                option.textContent = content.id;
                option.value = content.id;
                select.appendChild(option);
            }
        })
        .catch(function (err) {
            console.warn("Something went wrong.", err);
        })
};


async function getRecordInfo(sourceId, nightId, recordId) {
    fetch("/annotations/metadata?" + new URLSearchParams({
        sourceId: sourceId,
        nightId: nightId,
        recordId: recordId,
    }), { method: "GET" })
        .then(function (response) {
            if (response.ok) {
                return response.json();
            } else {
                return Promise.reject(response);
            }
        })
        .then(function (json) {
            var shortInfo = "Recording " + json.index + " of " + json.maxIndex + ": "
            byId("anno-recording-short-info").textContent = shortInfo;

            byId("anno-metadata-record-file").textContent = json.recordFile
            byId("anno-metadata-quality").textContent = json.quality
            byId("anno-metadata-tags").textContent = json.tags
            byId("anno-metadata-comments").textContent = json.comments
            // byId("anno-metadata-prefix").textContent = json.prefix
            byId("anno-metadata-local-date").textContent = json.localDate
            byId("anno-metadata-local-time").textContent = json.localTime
            // byId("anno-metadata-datetime-utc").textContent = json.dateTimeUtc
            byId("anno-metadata-latitude").textContent = json.latitude
            byId("anno-metadata-longitude").textContent = json.longitude

            // Save all received data in client.
            currentRecord = json
            annoSetQuality(json.quality);
            annoSetTags(json.tags);
            annoSetComments(json.comments);

        })
        .catch(function (err) {
            console.warn("Something went wrong.", err);
        })
};

async function saveRecordInfo(sourceId, nightId, recordId, quality, tags, comments) {
    fetch("/annotations/metadata?" + new URLSearchParams({
        sourceId: sourceId,
        nightId: nightId,
        recordId: recordId,
        quality: quality,
        tags: tags,
        comments: comments,
    }), { method: "PUT" })
        .then(function (response) {
            if (response.ok) {
                return response.json();
            } else {
                return Promise.reject(response);
            }
        })
        .then(function (json) {
            if (currentRecord.recordId == json.recordId) {
                byId("anno-metadata-quality").textContent = json.quality
                byId("anno-metadata-tags").textContent = json.tags
                byId("anno-metadata-comments").textContent = json.comments
            }
        })
        .catch(function (err) {
            console.warn("Something went wrong.", err);
        })
};
