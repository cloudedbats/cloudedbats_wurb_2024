

async function startRecording() {
    try {
        byId("recStatusId").innerHTML = "Waiting...";
        // // Save settings before recording starts.
        // saveSettings()
        await fetch("/record/start-rec/");
    } catch (err) {
        alert("ERROR startRecording: " + err);
        console.log(err);
    };
};

async function stopRecording() {
    try {
        byId("recStatusId").innerHTML = "Waiting...";
        await fetch("/record/stop-rec/");
    } catch (err) {
        alert("ERROR stopRecording: " + err);
        console.log(err);
    };
};

// async function recModeOnChange() {
//     try {
//         // let recmode = byId("recModeSelectId").value;
//         // let urlString = "/record/save-rec-mode/?recmode=" + recmode;
//         // await fetch(urlString);
//         let data = {
//             recMode: byId("recModeSelectId").value,
//         }
//         await fetch("/record/save-rec-mode/",
//         {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/json"
//             },
//             body: JSON.stringify(data)
//         })
//     } catch (err) {
//         alert("ERROR recModeOnChange: " + err);
//         console.log(err);
//     };
// };

async function saveLocationSource() {
    try {
        let location = {
            geoSource: byId("geoSourceSelectId").value,
            latitudeDd: byId("geoLatitudeDdId").value,
            longitudeDd: byId("geoLongitudeDdId").value,
        }
        await fetch("/record/save-location/",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(location)
            })
    } catch (err) {
        alert("ERROR saveLocation: " + err);
        console.log(err);
    };
};

async function saveLocation() {
    try {
        let location = {
            geoSource: byId("geoSourceSelectId").value,
            latitudeDd: byId("geoLatitudeDdId").value,
            longitudeDd: byId("geoLongitudeDdId").value,
        }
        if (byId("geoSourceSelectId").value == "geo-manual") {
            location["manualLatitudeDd"] = byId("geoLatitudeDdId").value
            location["manualLongitudeDd"] = byId("geoLongitudeDdId").value
        }
        if (byId("geoSourceSelectId").value == "geo-gps") {
            location["geoSource"] = "geo-manual"
            location["manualLatitudeDd"] = byId("geoLatitudeDdId").value
            location["manualLongitudeDd"] = byId("geoLongitudeDdId").value
        }
        if (byId("geoSourceSelectId").value == "geo-gps-or-manual") {
            location["geoSource"] = "geo-manual"
            location["manualLatitudeDd"] = byId("geoLatitudeDdId").value
            location["manualLongitudeDd"] = byId("geoLongitudeDdId").value
        }
        if (byId("geoSourceSelectId").value == "geo-last-gps-or-manual") {
            location["geoSource"] = "geo-manual"
            location["manualLatitudeDd"] = byId("geoLatitudeDdId").value
            location["manualLongitudeDd"] = byId("geoLongitudeDdId").value
        }
        await fetch("/record/save-location/",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(location)
            })
    } catch (err) {
        alert("ERROR saveLocation: " + err);
        console.log(err);
    };
};

async function getLocation() {
    try {
        let response = await fetch("/record/get-location/");
        let data = await response.json();
        updateLocation(data);
    } catch (err) {
        alert("ERROR getLocation: " + err);
        console.log(err);
    };
};

async function getManualLocation() {
    try {
        let response = await fetch("/record/get-location/");
        let location = await response.json();
        byId("geoLatitudeDdId").value = location.manualLatitudeDd
        byId("geoLongitudeDdId").value = location.manualLongitudeDd
    } catch (err) {
        alert("ERROR getManualLocation: " + err);
        console.log(err);
    };
};

async function setDetectorTime() {
    try {
        let posixTimeMs = new Date().getTime();
        // let urlString = "/record/setTime/?posixtime=" + posixTimeMs;
        let urlString = "/record/set-time/?posixtime=" + posixTimeMs;
        await fetch(urlString);
    } catch (err) {
        alert("ERROR setDetectorTime: " + err);
        console.log(err);
    };
};

async function saveSettings(settingsType) {
    try {
        let urlString = "/record/save-settings/";
        if (settingsType == "user-defined") {
            urlString = "/record/save-settings-user/";
        }
        else if (settingsType == "startup") {
            urlString = "/record/save-settings-startup/";
        }
        let settings = {
            recMode: byId("recModeSelectId").value,
            fileDirectory: byId("recFileDirectoryId").value,
            fileDirectoryDateOption: byId("recFileDirectoryDateOptionId").value,
            filenamePrefix: byId("recFilenamePrefixId").value,
            detectionLimitKhz: byId("recDetectionLimitId").value,
            detectionSensitivityDbfs: byId("recDetectionSensitivityId").value,
            detectionAlgorithm: byId("recDetectionAlgorithmId").value,
            recLengthS: byId("recRecLengthId").value,
            recType: byId("recTypeId").value,
            feedbackOnOff: byId("liveFeedbackOnOffId").value,
            feedbackVolume: byId("liveFeedbackVolumeSliderId").value,
            feedbackPitch: byId("liveFeedbackPitchSliderId").value,
            feedbackFilterLowKhz: byId("liveFeedbackFilterLowId").value,
            feedbackFilterHighKhz: byId("liveFeedbackFilterHighId").value,
            startupOption: byId("settingsStartupOptionId").value,
            schedulerStartEvent: byId("recSchedulerStartEventId").value,
            schedulerStartAdjust: byId("recSchedulerStartAdjustId").value,
            schedulerStopEvent: byId("recSchedulerStopEventId").value,
            schedulerStopAdjust: byId("recSchedulerStopAdjustId").value,
            // schedulerPostAction: byId("recSchedulerPostActionId").value,
            // schedulerPostActionDelay: byId("recSchedulerPostActionDelayId").value,
        }
        await fetch(urlString,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(settings)
            })
    } catch (err) {
        alert("ERROR saveSettings: " + err);
        console.log(err);
    };
};

async function getSettings() {
    try {
        let response = await fetch("/record/get-settings/?default=false");
        let data = await response.json();
        updateSettings(data);
    } catch (err) {
        alert("ERROR getSettings: " + err);
        console.log(err);
    };
};

async function getDefaultSettings() {
    try {
        let response = await fetch("/record/get-settings/?default=true");
        let data = await response.json();
        updateSettings(data);
    } catch (err) {
        alert("ERROR getDefaultSettings: " + err);
        console.log(err);
    };
};

async function loadSettings(settingsType) {
    try {
        let response = await fetch("/record/load-settings/?settingsType=" + settingsType);
        await response.json();
    } catch (err) {
        alert("ERROR getSettings: " + err);
        console.log(err);
    };
};

async function manualTrigger() {
    try {
        let urlString = "/record/rec-manual-trigger/";
        await fetch(urlString);
    } catch (err) {
        alert("ERROR manualTrigger: " + err);
        console.log(err);
    };
};

async function raspberryPiControl(command) {
    try {
        if (command == "rpiCancel") {
            byId("recModeSelectId").value = lastUsedSettings.recMode
            modeSelectOnChange(updateDetector = true)
        } else {
            byId("recModeSelectId").value = lastUsedSettings.recMode
            modeSelectOnChange(updateDetector = true)
            let urlString = "/record/rpi-control/?command=" + command;
            await fetch(urlString);
        }
    } catch (err) {
        alert("ERROR raspberryPiControl: " + err);
        console.log(err);
    };
};

let waitTextNr = 0

function startWebsocket(wsUrl) {
    // let ws = new WebSocket("ws://localhost:8000/ws");
    let ws = new WebSocket(wsUrl);
    ws.onmessage = function (event) {
        let dataJson = JSON.parse(event.data);
        if ("status" in dataJson === true) {
            updateStatus(dataJson.status)
        }
        if ("location" in dataJson === true) {
            updateLocation(dataJson.location)
        }
        if ("latlong" in dataJson === true) {
            updateLatLong(dataJson.latlong)
        }
        if ("settings" in dataJson === true) {
            updateSettings(dataJson.settings)
        }
        if ("logRows" in dataJson === true) {
            updateLogTable(dataJson.logRows)
        }
    }
    ws.onclose = function () {
        // Try to reconnect in 5th seconds. Will continue...
        ws = null;

        if (waitTextNr == 0) {
            waitText = "Waiting for response from detector..."
        } else if (waitTextNr == 1) {
            waitText = "Waiting for response from detector."
        } else if (waitTextNr == 2) {
            waitText = "Waiting for response from detector.."
        }
        waitTextNr += 1
        if (waitTextNr >= 3) {
            waitTextNr = 0
        }

        let statusWhenDisconnected = {
            recStatus: waitText,
            deviceName: "",
            detectorTime: "",
            locationStatus: ""
        }
        updateStatus(statusWhenDisconnected)

        setTimeout(function () { startWebsocket(wsUrl) }, 5000);
    };
};
