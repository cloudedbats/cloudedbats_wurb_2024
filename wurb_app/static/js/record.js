

function recToggleSettings() {
    if (byId("recSettingsId").classList.contains("is-hidden")) {
        byId("recBodyId").classList.add("is-hidden");
        byId("recSettingsId").classList.remove("is-hidden");
        byId("recSettingsTextId").textContent = "Hide settings";
    } else {
        byId("recSettingsId").classList.add("is-hidden");
        byId("recBodyId").classList.remove("is-hidden");
        byId("recSettingsTextId").textContent = "Show settings";
    };
}

function geoToggleSettings() {
    if (byId("geoSettingsId").classList.contains("is-hidden")) {
        byId("geoBodyId").classList.add("is-hidden");
        byId("geoSettingsId").classList.remove("is-hidden");
        byId("geoSettingsTextId").textContent = "Hide settings";
    } else {
        byId("geoSettingsId").classList.add("is-hidden");
        byId("geoBodyId").classList.remove("is-hidden");
        byId("geoSettingsTextId").textContent = "Show settings";
    };
}

// Generic functions.
function hideDivision(divId) {
    if (divId != 'undefined') {
        divId.style.visibility = "hidden";
        divId.style.overflow = "hidden";
        divId.style.height = "0";
        divId.style.width = "0";
    }
};

function showDivision(divId) {
    if (divId != 'undefined') {
        divId.style.visibility = null;
        divId.style.overflow = null;
        divId.style.height = null;
        divId.style.width = null;
    }
};

// For detector mode.
function modeSelectOnChange(updateDetector) {
    let selectedValue = byId("recModeSelectId").options[byId("recModeSelectId").selectedIndex].value
    hideDivision(byId("recManualTriggeringId"));
    hideDivision(byId("recDetectorPowerOffId"));
    if (selectedValue == "mode-off") {
        // stopRecording()
        if (updateDetector) {
            saveSettings()
        }
    }
    else if (selectedValue == "mode-on") {
        if (updateDetector) {
            saveSettings()
        }
        // startRecording()
    }
    else if (selectedValue == "mode-auto") {
        if (updateDetector) {
            saveSettings()
        }
        // startRecording()
    }
    else if (selectedValue == "mode-manual") {
        showDivision(byId("recManualTriggeringId"));
        if (updateDetector) {
            saveSettings()
        }
        // startRecording()
    }
    else if (selectedValue == "mode-scheduler-on") {
        // stopRecording()
        if (updateDetector) {
            saveSettings()
        }
    }
    else if (selectedValue == "mode-scheduler-auto") {
        // stopRecording()
        if (updateDetector) {
            saveSettings()
        }
    }
    else if (selectedValue == "load-user-default") {
        stopRecording()
        loadSettings(settingsType = "user-default")
    }
    else if (selectedValue == "load-start-up") {
        stopRecording()
        loadSettings(settingsType = "start-up")
    }
    else if (selectedValue == "load-factory-default") {
        stopRecording()
        loadSettings(settingsType = "factory-default")
    }
    else if (selectedValue == "detector-power-off") {
        showDivision(byId("recDetectorPowerOffId"));
    }
    // Trigging Audio feedback sliders
    byId("liveFeedbackVolumeSliderId").oninput()
    byId("liveFeedbackPitchSliderId").oninput()
}

// For the geographic location tile.
function geoLocationSourceOnChange(updateDetector) {
    let selectedValue = byId("geoSourceSelectId").options[byId("geoSourceSelectId").selectedIndex].value
    byId("geoButtonTextId").innerHTML = "Save"
    if (selectedValue == "geo-not-used") {
        byId("geoLatitudeDdId").value = "0.0";
        byId("geoLongitudeDdId").value = "0.0";
        byId("geoLatitudeDdId").disabled = true;
        byId("geoLongitudeDdId").disabled = true;
        byId("geoLocationButtonId").disabled = true;
        if (updateDetector) {
            saveLocationSource()
        }
    }
    else if (selectedValue == "geo-manual") {
        getManualLocation();
        byId("geoButtonTextId").innerHTML = "Save lat/long"
        byId("geoLatitudeDdId").disabled = false;
        byId("geoLongitudeDdId").disabled = false;
        byId("geoLocationButtonId").disabled = false;
        if (updateDetector) {
            saveLocationSource()
        }
    }
    // Disabled, HTTPS is needed.
    // else if (selectedValue == "geo-client-gps") {
    //   activateGeoLocation()
    //   byId("geoLatitudeDdId").disabled = true;
    //   byId("geoLongitudeDdId").disabled = true;
    //   byId("geoLocationButtonId").disabled = false;
    //   if (updateDetector) {
    //     saveLocationSource()
    //   }
    // }
    else if (selectedValue == "geo-gps") {
        byId("geoButtonTextId").innerHTML = "Use as manually entered"
        byId("geoLatitudeDdId").disabled = true;
        byId("geoLongitudeDdId").disabled = true;
        byId("geoLocationButtonId").disabled = false;
        if (updateDetector) {
            saveLocationSource()
        }
    }
    else if (selectedValue == "geo-gps-or-manual") {
        byId("geoButtonTextId").innerHTML = "Save"
        byId("geoLatitudeDdId").disabled = true;
        byId("geoLongitudeDdId").disabled = true;
        byId("geoLocationButtonId").disabled = true;
        if (updateDetector) {
            saveLocationSource()
        }
    }
    else if (selectedValue == "geo-last-gps-or-manual") {
        byId("geoButtonTextId").innerHTML = "Save"
        byId("geoLatitudeDdId").disabled = true;
        byId("geoLongitudeDdId").disabled = true;
        byId("geoLocationButtonId").disabled = true;
        if (updateDetector) {
            saveLocationSource()
        }
    }
    else {
        byId("geoLatitudeDdId").disabled = true;
        byId("geoLongitudeDdId").disabled = true;
        byId("geoLocationButtonId").disabled = true;
    }
}

// Disabled, HTTPS is needed.
// function activateGeoLocation() {
//   if (navigator.geolocation) {
//     navigator.geolocation.getCurrentPosition(showPosition, errorCallback, { timeout: 10000 });
//     // navigator.geolocation.getCurrentPosition(showLocation);
//     // navigator.geolocation.watchPosition(showLocation);
//     // navigator.geolocation.clearWatch(showLocation);
//   } else {
//     alert(`Geo location from client:\nNot supported by this browser.`);
//   };
// };
// function showPosition(location) {
//   byId("geoLatitudeId").value = location.coords.latitude;
//   byId("geoLongitudeId").value = location.coords.longitude;
// };
// function errorCallback(error) {
//   alert(`Geo location from client:\nERROR(" + error.code + " : " + error.message);
// };

function audioFeedbackSliders() {
    // Update slider values.
    byId("liveFeedbackVolumeId").innerHTML = "[" + byId("liveFeedbackVolumeSliderId").value + "%]";
    byId("liveFeedbackPitchId").innerHTML = "[1/" + byId("liveFeedbackPitchSliderId").value + "]";
    // On changes.
    byId("liveFeedbackVolumeSliderId").oninput = function () {
        byId("liveFeedbackVolumeId").innerHTML = "[" + this.value + "%]";
    }
    byId("liveFeedbackVolumeSliderId").onchange = function () {
        // Send to server.
        byId("liveFeedbackVolumeId").innerHTML = "[" + this.value + "%]";
        setAudioFeedback()
    }
    byId("liveFeedbackPitchSliderId").oninput = function () {
        byId("liveFeedbackPitchId").innerHTML = "[1/" + this.value + "]";
    }
    byId("liveFeedbackPitchSliderId").onchange = function () {
        // Send to server.
        byId("liveFeedbackPitchId").innerHTML = "[1/" + this.value + "]";
        setAudioFeedback()
    }
}

// Used for the main tabs in the settings tile.
function hideShowSettingsTabs(tabName) {
    byId("tabSettingsBasicId").classList.remove("is-active");
    byId("tabSettingsMoreId").classList.remove("is-active");
    byId("tabSettingsSchedulerId").classList.remove("is-active");
    hideDivision(byId("divSettingsBasicId"))
    hideDivision(byId("divSettingsMoreId"))
    hideDivision(byId("divSettingsSchedulerId"))

    if (tabName == "basic") {
        byId("tabSettingsBasicId").classList.add("is-active");
        showDivision(byId("divSettingsBasicId"))
    } else if (tabName == "more") {
        byId("tabSettingsMoreId").classList.add("is-active");
        showDivision(byId("divSettingsMoreId"))
    } else if (tabName == "scheduler") {
        byId("tabSettingsSchedulerId").classList.add("is-active");
        showDivision(byId("divSettingsSchedulerId"))
    };
};
// Functions used to updates fields based on response contents.
function updateStatus(status) {
    byId("recStatusId").innerHTML = status.recStatus;
    if (status.deviceName != "") {
        byId("recStatusId").innerHTML += "<br>"
        byId("recStatusId").innerHTML += status.deviceName;
    }
    byId("recDetectorTimeId").innerHTML = status.detectorTime;
    byId("detectorTimeId").innerHTML = status.detectorTime;
    byId("geoStatusId").innerHTML = status.locationStatus;
}

function updateLocation(location) {
    byId("geoSourceSelectId").value = location.geoSource
    if (location.geoSource == "geo-manual") {
        byId("geoLatitudeDdId").value = location.manualLatitudeDd
        byId("geoLongitudeDdId").value = location.manualLongitudeDd
    } else {
        byId("geoLatitudeDdId").value = location.latitudeDd
        byId("geoLongitudeDdId").value = location.longitudeDd
    }
    // Check geolocation:
    geoLocationSourceOnChange(updateDetector = false);
}

function updateLatLong(latlong) {
    byId("geoLatitudeDdId").value = latlong.latitudeDd
    byId("geoLongitudeDdId").value = latlong.longitudeDd
}

function updateSettings(settings) {

    lastUsedSettings = settings

    byId("recModeSelectId").value = settings.recMode
    byId("recFileDirectoryId").value = settings.fileDirectory
    byId("recFileDirectoryDateOptionId").value = settings.fileDirectoryDateOption
    byId("recFilenamePrefixId").value = settings.filenamePrefix
    byId("recDetectionLimitId").value = settings.detectionLimitKhz
    byId("recDetectionSensitivityId").value = settings.detectionSensitivityDbfs
    byId("recDetectionAlgorithmId").value = settings.detectionAlgorithm
    byId("recRecLengthId").value = settings.recLengthS
    byId("recTypeId").value = settings.recType
    byId("liveFeedbackOnOffId").value = settings.feedbackOnOff
    byId("liveFeedbackVolumeSliderId").value = settings.feedbackVolume
    byId("liveFeedbackPitchSliderId").value = settings.feedbackPitch
    byId("liveFeedbackFilterLowId").value = settings.feedbackFilterLowKhz
    byId("liveFeedbackFilterLowId").value = settings.feedbackFilterHighKhz
    byId("settingsStartupOptionId").value = settings.startupOption
    byId("recSchedulerStartEventId").value = settings.schedulerStartEvent
    byId("recSchedulerStartAdjustId").value = settings.schedulerStartAdjust
    byId("recSchedulerStopEventId").value = settings.schedulerStopEvent
    byId("recSchedulerStopAdjustId").value = settings.schedulerStopAdjust
    // byId("recSchedulerPostActionId").value = settings.schedulerPostAction
    // byId("recSchedulerPostActionDelayId").value = settings.schedulerPostActionDelay

    modeSelectOnChange(updateDetector = false)

    // Trigging Audio feedback sliders
    byId("liveFeedbackVolumeSliderId").oninput()
    byId("liveFeedbackPitchSliderId").oninput()
}

function saveUserDefaultSettings() {
    saveSettings(settingsType = "user-defined")
}

function saveStartupSettings() {
    saveSettings(settingsType = "startup")
}

function updateLogTable(logRows) {
    htmlTableRows = ""
    for (rowIndex in logRows) {
        htmlTableRows += "<tr><td>"
        htmlTableRows += logRows[rowIndex]
        htmlTableRows += "</tr></td>"
    }
    byId("recLogTableId").innerHTML = htmlTableRows
}
