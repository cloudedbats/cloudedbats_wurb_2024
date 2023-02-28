

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


            // During development.
            byId("anno-select-source-id").value = "local";
            var sourceId = byId("anno-select-source-id").value;
            getNights(sourceId);




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


            // During development.
            byId("anno-select-night-id").value = "Taberg-1_2022-12-21";
            var sourceId = byId("anno-select-source-id").value;
            var nightId = byId("anno-select-night-id").value;
            getRecordInfo(sourceId, nightId, "");




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
            var shortInfo = " for file " + json.index + " of " + json.maxIndex
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

            // image_src = "http://localhost:8001/annotations/spectrogram?"
            image_src = "/annotations/spectrogram?"
            image_src += "sourceId="
            image_src += sourceId
            image_src += "&nightId="
            image_src += nightId
            image_src += "&recordId="
            image_src += recordId
            byId("anno-spectrogram-src-id").src = image_src;

            //  file_src = "http://localhost:8001/annotations/file?"
            file_src = "/annotations/file?"
            file_src += "sourceId="
            file_src += sourceId
            file_src += "&nightId="
            file_src += nightId
            file_src += "&recordId="
            file_src += recordId
            byId("anno-download-id").href = file_src;
            byId("anno-download-id").download = json.recordFile;


            byId("anno-first-id").textContent = "First"
            byId("anno-last-id").textContent = "Last"
            byId("anno-first-id").disabled = false;
            byId("anno-previous-id").disabled = false;
            byId("anno-next-id").disabled = false;
            byId("anno-last-id").disabled = false;
            var optionList = byId("anno-select-night-id");
            var optionIndex = optionList.selectedIndex;
            if (json.maxIndex <= 1) {
                byId("anno-previous-id").disabled = true;
                byId("anno-next-id").disabled = true;
                if (optionIndex > 1) {
                    byId("anno-first-id").textContent = "Previous night"
                    byId("anno-first-id").disabled = false;
                }
                if (optionIndex < optionList.options.length -1) {
                    byId("anno-last-id").textContent = "Next night"
                    byId("anno-last-id").disabled = false;
                }
            }
            else if (json.index == 1) {
                byId("anno-previous-id").disabled = true;
                byId("anno-first-id").disabled = true;
                if (optionIndex > 1) {
                    byId("anno-first-id").textContent = "Previous night"
                    byId("anno-first-id").disabled = false;
                }
            }
            else if (json.index == json.maxIndex) {
                byId("anno-next-id").disabled = true;
                byId("anno-last-id").disabled = true;
                if (optionIndex < optionList.options.length - 1) {
                    byId("anno-last-id").textContent = "Next night"
                    byId("anno-last-id").disabled = false;
                }
            }
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
