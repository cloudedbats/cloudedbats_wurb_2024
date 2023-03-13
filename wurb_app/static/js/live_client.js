

async function setAudioFeedback() {
    try {
        let volume = byId("feedbackVolumeSliderId").value;
        let pitch = byId("feedbackPitchSliderId").value;
        let urlString = "/live/set-audio-feedback/?volume=${volume}&pitch=${pitch}";
        await fetch(urlString);
    } catch (err) {
        alert("ERROR setAudioFeedback: ${err}");
        console.log(err);
    };
};

