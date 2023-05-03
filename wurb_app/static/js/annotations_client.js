
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
            var select = byId("annoSelectSourceId");
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
            var select = byId("annoSelectNightId");
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
            var shortInfo = " for file " + json.index + " of " + json.maxIndex
            byId("annoRecordingShortInfoId").textContent = shortInfo;

            byId("annoMetadataRecordFileId").textContent = json.recordFile
            byId("annoMetadataQualityId").textContent = json.quality
            byId("annoMetadataTagsId").textContent = json.tags
            byId("annoMetadataCommentsId").textContent = json.comments
            // byId("annoMetadataPrefixId").textContent = json.prefix
            byId("annoMetadataLocalDateId").textContent = json.localDate
            byId("annoMetadataLocalTimeId").textContent = json.localTime
            // byId("annoMetadataDatetimeUtcId").textContent = json.dateTimeUtc
            byId("annoMetadataLatitudeId").textContent = json.latitude
            byId("annoMetadataLongitudeId").textContent = json.longitude

            // Save all received data in client.
            currentRecord = json
            annoSetQuality(json.quality);
            annoSetTags(json.tags);
            annoSetComments(json.comments);

            // imageSrc = "http://localhost:8001/annotations/spectrogram?"
            imageSrc = "/annotations/spectrogram?"
            imageSrc += "sourceId="
            imageSrc += sourceId
            imageSrc += "&nightId="
            imageSrc += nightId
            imageSrc += "&recordId="
            imageSrc += recordId
            byId("annoSpectrogramSrcId").src = imageSrc;

            //  fileSrc = "http://localhost:8001/annotations/file?"
            fileSrc = "/annotations/file?"
            fileSrc += "sourceId="
            fileSrc += sourceId
            fileSrc += "&nightId="
            fileSrc += nightId
            fileSrc += "&recordId="
            fileSrc += recordId
            byId("annoDownloadId").href = fileSrc;
            byId("annoDownloadId").download = json.recordFile;

            byId("annoFirstTextId").textContent = "First"
            byId("annoLastTextId").textContent = "Last"
            byId("annoFirstId").disabled = false;
            byId("annoPreviousId").disabled = false;
            byId("annoNextId").disabled = false;
            byId("annoLastId").disabled = false;
            var optionList = byId("annoSelectNightId");
            var optionIndex = optionList.selectedIndex;
            if (json.maxIndex <= 1) {
                byId("annoPreviousId").disabled = true;
                byId("annoNextId").disabled = true;
                if (optionIndex > 1) {
                    byId("annoFirstTextId").textContent = "Previous night"
                    byId("annoFirstId").disabled = false;
                }
                if (optionIndex < optionList.options.length - 1) {
                    byId("annoLastTextId").textContent = "Next night"
                    byId("annoLastId").disabled = false;
                }
            }
            else if (json.index == 1) {
                byId("annoPreviousId").disabled = true;
                byId("annoFirstId").disabled = true;
                if (optionIndex > 1) {
                    byId("annoFirstTextId").textContent = "Previous night"
                    byId("annoFirstId").disabled = false;
                }
            }
            else if (json.index == json.maxIndex) {
                byId("annoNextId").disabled = true;
                byId("annoLastId").disabled = true;
                if (optionIndex < optionList.options.length - 1) {
                    byId("annoLastTextId").textContent = "Next night"
                    byId("annoLastId").disabled = false;
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
                byId("annoMetadataQualityId").textContent = json.quality
                byId("annoMetadataTagsId").textContent = json.tags
                byId("annoMetadataCommentsId").textContent = json.comments
            }
        })
        .catch(function (err) {
            console.warn("Something went wrong.", err);
        })
};
