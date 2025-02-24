function toggleDivs() {
    var checkbox = document.getElementById('customTopicCheckbox');
    var customDiv = document.getElementById('customTopicDiv');
    var inlimiteDiv = document.getElementById('inlimiteContainerDiv');
    var check_form = document.getElementById('check_form');

    if ('{{ selection.if_custom }}' === 'True') {
        check_form.style.display = 'none';
        customDiv.style.display = 'block';
        inlimiteDiv.style.display = 'none';
    } else if (checkbox.checked) {
        customDiv.style.display = 'block';
        inlimiteDiv.style.display = 'none';
    } else if ('{{ selection.if_custom }}' === 'False') {
        customDiv.style.display = 'none';
        inlimiteDiv.style.display = 'block';
    } else {
        customDiv.style.display = 'none';
        inlimiteDiv.style.display = 'block';
    }
}

document.getElementById('customTopicCheckbox')?.addEventListener('change', toggleDivs);
document.addEventListener('DOMContentLoaded', toggleDivs);

function refreshPageContent() {
    $('#inlimiteContainerDiv').load('/student #inlimiteContainerDiv');
}

// Display existing selection
$(document).ready(function () {
    if ('{{ selection.if_custom }}' === 'False') {
        if ('{{ selection.first_topic_name }}') {
            $('#choose1_form .text-field_topic').val('{{ selection.first_topic_name }}').prop('disabled', true).addClass('disabled-color');
            $('#choose1_form .submit-button').val('Reset');
        }
        if ('{{ selection.second_topic_name }}') {
            $('#choose2_form .text-field_topic').val('{{ selection.second_topic_name }}').prop('disabled', true).addClass('disabled-color');
            $('#choose2_form .submit-button').val('Reset');
        }
        if ('{{ selection.third_topic_name }}') {
            $('#choose3_form .text-field_topic').val('{{ selection.third_topic_name }}').prop('disabled', true).addClass('disabled-color');
            $('#choose3_form .submit-button').val('Reset');
        }
    } else {
        if ('{{ selection.if_custom }}' === 'True') {
            $('#customTopicDiv #custom_topic_name').val('{{ selection.first_topic_name }}').prop('disabled', true).addClass('disabled-color');
            $('#supervisor_id').val('{{ selection.custom_supervisor_id }}').prop('disabled', true).addClass('disabled-color');
            $('#type_id').val('{{ selection.custom_type_id }}').prop('disabled', true).addClass('disabled-color');
            $('#customTopicDiv #field-2').val('{{ selection.custom_description }}').prop('disabled', true).addClass('disabled-color');
            $('#customFormSubmit').val('Reset');
        }
    }


    // submit application
    $('.student_submit_form').submit(function (e) {
        e.preventDefault();
        var formId = $(this).attr('id');
        var choiceNumber = formId.replace('choose', '').replace('_form', '');
        var topicId = $(this).find('.text-field_topic').val();
        var isReset = $(this).find('.submit-button').val() === 'Reset';
        console.log(isReset)

        // if reset
        if (isReset) {
            resetSelection(formId, choiceNumber);
            return;
        }

        // reset selection
        function resetSelection(formId, choiceNumber) {
            $.ajax({
                url: '/update_selection',
                method: 'POST',
                data: {choice_number: choiceNumber, reset: 'true'},
                success: function (response) {
                    var data = JSON.parse(response);
                    if (data.success) {
                        $('#' + formId + ' .text-field_topic').val('');
                        $('#' + formId + ' .submit-button').val('Save');
                    }
                    location.reload();
                }
            });
        }

        // submit
        $.ajax({
            url: '/update_selection',
            method: 'POST',
            data: {topic_id: topicId, choice_number: choiceNumber},
            success: function (response) {
                console.log(response)
                var data = JSON.parse(response);
                if (data.success) {
                    console.log('success')
                    if (data.reset) {
                        $('#' + formId + ' .text-field_topic').val('');
                        $('#' + formId + ' .submit-button').val('Save');
                        location.reload();
                    } else {
                        $('#' + formId + ' .text-field_topic').val(response.topic_name);
                        $('#' + formId + ' .submit-button').val('Reset');
                        location.reload();
                    }
                } else {
                    alert(data.error)
                }
            }
        });
    });

    // submit custom topic
    $('#customFormSubmit').click(function (e) {
        e.preventDefault();
        var supervisorId = $(this).parent().find('#supervisor_id').val();
        var typeId = $(this).parent().find('#type_id').val();
        var description = $(this).parent().find('#field-2').val();
        var topicName = $(this).parent().find('#custom_topic_name').val();
        var isReset = $('#customFormSubmit').val() === 'Reset';

        // if reset
        if (isReset) {
            console.log('reset')
            resetCustomTopic();
            return;
        }

        function resetCustomTopic() {
            console.log('reset')
            $.ajax({
                url: '/update_custom_topic',
                method: 'POST',
                data: {reset: 'true'},
                success: function (response) {
                    var data = JSON.parse(response);
                    if (data.success) {
                        $('#custom_form #custom_topic_name').val('');
                        $('#supervisor_id').val('');
                        $('#type_id').val('');
                        $('#custom_form #field-2').val('');
                        $('#customFormSubmit').val('Save');
                    }
                    location.reload();
                }
            });
        }

        // submit
        $.ajax({
            url: '/update_custom_topic',
            method: 'POST',
            data: {
                supervisor_id: supervisorId,
                type_id: typeId,
                description: description,
                topic_name: topicName
            },
            success: function (response) {
                console.log(response)
                var data = JSON.parse(response);
                if (data.success) {
                    console.log('success')
                    if (data.reset) {
                        $('#custom_form #custom_topic_name').val('');
                        $('#supervisor_id').val('');
                        $('#type_id').val('');
                        $('#custom_form #field-2').val('');
                        $('#customFormSubmit').val('Save');
                        location.reload();
                    } else {
                        $('#customTopicDiv #custom_topic_name').val('{{ selection.first_topic_name }}');
                        $('#supervisor_id').val('{{ selection.custom_supervisor_id }}');
                        $('#type_id').val('{{ selection.custom_type_id }}');
                        $('#customTopicDiv #field-2').val('{{ selection.custom_description }}');
                        $('#customFormSubmit').val('Reset');
                        location.reload();
                    }
                } else {
                    alert(data.error)
                }
            }
        });
    });
});

