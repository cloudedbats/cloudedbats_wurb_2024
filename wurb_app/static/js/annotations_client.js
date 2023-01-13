

async function getSourceDirs() {
    try {
        let response = await fetch("/ajax-admin/get-source-dirs/");
        let data = await response.json();
        //   updateLocation(data);
    } catch (err) {
        alert(`ERROR getSourceDirs: ${err}`);
        console.log(err);
    };
};


async function getEventsDirs() {
    try {
        let response = await fetch("/ajax-admin/get-events-dirs/");
        let events = await response.json();
        // Clear options.
        $('#anno-select-event-id')
            .empty()
            .append(new Option("Please select:", "select"))
            .find('option:first')
            .attr("selected", "selected");
        // Add new options.
        $.each(events, function (i, event) {
            $('#anno-select-event-id').append(new Option(event, event));
        });
    } catch (err) {
        alert(`ERROR getEventsDirs: ${err}`);
        console.log(err);
    };
};

async function getRecordingInfo() {
    try {
        let response = await fetch("/ajax-admin/get-recording-info/");
        let rec_info = await response.json();

        alert(response)

    } catch (err) {
        alert(`ERROR getEventsDirs: ${err}`);
        console.log(err);
    };
};
