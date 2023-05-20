$(document).ready(function () {
    $('.abort-job-btn').click(function (event) {
        var button = $(this);
        var jobId = button.data("job-id");
        $.ajax({
            url: '/api/job/'+ jobId,
            type: 'DELETE',
            success: function (result) {
                setTimeout(function () {
                    location.reload();
                }, 2000);
            },
            error: function (result) {
                alert('Unable to abort job.');
            }
        })
    });

    $('.remove-instance-btn').click(function (event) {
        var instanceId = $(this).data('instance-id');
        console.log(instanceId)
        $.ajax({
            url: '/api/delete/?name=' + instanceId,
            type: 'GET',
            success: function (result) {
                var workerElementId = '# ' + 'instance-' + instanceId + '-well';
                $(workerElementId).remove();
            },
            error: function (result) {
                alert('Unable to remove worker.');
            }
        });
    });

    $("#add-job-form").submit(function (event) {
        event.preventDefault();
        var data = new FormData();
        data.append('job_name', $('#job_name')[0].value);
        data.append('input_file', $('#input_file')[0].files[0]);
        data.append('solution_file', $('#solution_file')[0].files[0]);
        $.ajax({
            url: '/api/job',
            type: 'POST',
            data: data,
            processData: false,
            contentType: false,
            success: function (result) {
                window.location = '/jobs'
            },
            error: function (error) {
                alert('Wrong data!');
            }

        })
    });
});