

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
    // // Trigging Audio feedback sliders
    // byId("feedbackVolumeSliderId").oninput()
    // byId("feedbackPitchSliderId").oninput()
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
//   byId("latitudeId").value = location.coords.latitude;
//   byId("longitudeId").value = location.coords.longitude;
// };
// function errorCallback(error) {
//   alert(`Geo location from client:\nERROR(${error.code}): ${error.message}`);
// };

function audioFeedbackSliders() {
    // Update slider values.
    byId("feedbackVolumeId").innerHTML = "[" + byId("feedbackVolumeSliderId").value + "%]";
    byId("feedbackPitchId").innerHTML = "[1/" + byId("feedbackPitchSliderId").value + "]";
    // On changes.
    byId("feedbackVolumeSliderId").oninput = function () {
        byId("feedbackVolumeId").innerHTML = "[" + this.value + "%]";
    }
    byId("feedbackVolumeSliderId").onchange = function () {
        // Send to server.
        byId("feedbackVolumeId").innerHTML = "[" + this.value + "%]";
        setAudioFeedback()
    }
    byId("feedbackPitchSliderId").oninput = function () {
        byId("feedbackPitchId").innerHTML = "[1/" + this.value + "]";
    }
    byId("feedbackPitchSliderId").onchange = function () {
        // Send to server.
        byId("feedbackPitchId").innerHTML = "[1/" + this.value + "]";
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
    byId("detectorStatusId").innerHTML = status.recStatus;
    if (status.deviceName != "") {
        byId("detectorStatusId").innerHTML += "<br>"
        byId("detectorStatusId").innerHTML += status.deviceName;
    }
    byId("detectorTimeId").innerHTML = status.detectorTime;
    byId("locationStatusId").innerHTML = status.locationStatus;
}

function updateLocation(location) {
    byId("locationSourceSelectId").value = location.geoSource
    if (location.geoSource == "geo-manual") {
        byId("latitudeDdId").value = location.manualLatitudeDd
        byId("longitudeDdId").value = location.manualLongitudeDd
    } else {
        byId("latitudeDdId").value = location.latitudeDd
        byId("longitudeDdId").value = location.longitudeDd
    }
    // Check geolocation:
    geoLocationSourceOnChange(updateDetector = false);
}

function updateLatLong(latlong) {
    byId("latitudeDdId").value = latlong.latitudeDd
    byId("longitudeDdId").value = latlong.longitudeDd
}

function updateSettings(settings) {

    lastUsedSettings = settings

    byId("recModeSelectId").value = settings.recMode
    byId("settingsFileDirectoryId").value = settings.fileDirectory
    byId("settingsFileDirectoryDateOptionId").value = settings.fileDirectoryDateOption
    byId("settingsFilenamePrefixId").value = settings.filenamePrefix
    byId("settingsDetectionLimitId").value = settings.detectionLimitKhz
    byId("settingsDetectionSensitivityId").value = settings.detectionSensitivityDbfs
    byId("settingsDetectionAlgorithmId").value = settings.detectionAlgorithm
    byId("settingsRecLengthId").value = settings.recLengthS
    byId("settingsRecTypeId").value = settings.recType
    byId("settingsFeedbackOnOffId").value = settings.feedbackOnOff
    byId("feedbackVolumeSliderId").value = settings.feedbackVolume
    byId("feedbackPitchSliderId").value = settings.feedbackPitch
    byId("settingsFeedbackFilterLowId").value = settings.feedbackFilterLowKhz
    byId("settingsFeedbackFilterHighId").value = settings.feedbackFilterHighKhz
    byId("settingsStartupOptionId").value = settings.startupOption
    byId("settingsSchedulerStartEventId").value = settings.schedulerStartEvent
    byId("settingsSchedulerStartAdjustId").value = settings.schedulerStartAdjust
    byId("settingsSchedulerStopEventId").value = settings.schedulerStopEvent
    byId("settingsSchedulerStopAdjustId").value = settings.schedulerStopAdjust
    byId("settingsSchedulerPostActionId").value = settings.schedulerPostAction
    byId("settingsSchedulerPostActionDelayId").value = settings.schedulerPostActionDelay

    modeSelectOnChange(updateDetector = false)

    // Trigging Audio feedback sliders
    byId("feedbackVolumeSliderId").oninput()
    byId("feedbackPitchSliderId").oninput()
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
