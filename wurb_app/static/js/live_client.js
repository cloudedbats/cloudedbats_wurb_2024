

async function setAudioFeedback() {
    try {
        let volume = feedback_volume_slider_id.value;
        let pitch = feedback_pitch_slider_id.value;
        let url_string = "/live/set-audio-feedback/?volume=${volume}&pitch=${pitch}";
        await fetch(url_string);
    } catch (err) {
        alert("ERROR setAudioFeedback: ${err}");
        console.log(err);
    };
};

