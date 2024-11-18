// Tab switch
$(document).ready(function () {
    var pre = '{{ pre }}'
    console.log(pre)
    //When page loads...
    $('.tab_link').click(function (e) {
        e.preventDefault();
        //Get the link that was clicked
        var tabEntry = $(this).attr('data-w-tab');

        $('.tab_link').removeClass('w--current');
        $(this).addClass('w--current');

        //Hide all tab content
        $('.w-tab-pane').fadeOut(100);

        //Show the tab content that has the same data-w-tab as the link clicked
        $('.w-tab-pane[data-w-tab="' + tabEntry + '"]').fadeIn(300)
    });
    if (pre === 'student') {
        $('.tab_link[data-w-tab="Students"]').click();
    } else {
        $('.tab_link').first().click();
    }
})

// Deadline time picker
window.addEventListener('DOMContentLoaded', (event) => {
    flatpickr("#round1-submit", {
        enableTime: true,
        dateFormat: "Y-m-d H:i",
        time_24hr: true
    });

    flatpickr("#round1-result", {
        enableTime: true,
        dateFormat: "Y-m-d H:i",
        time_24hr: true
    });

    // 同样的设置也应用于 Round 2
    flatpickr("#round2-submit", {
        enableTime: true,
        dateFormat: "Y-m-d H:i",
        time_24hr: true
    });

    flatpickr("#round2-result", {
        enableTime: true,
        dateFormat: "Y-m-d H:i",
        time_24hr: true
    });
});

//Deadline form submit
$('#deadline-form-1, #deadline-form-2').submit(function (e) {
    e.preventDefault();
    var formID = $(this).attr('id');
    var roundNumber = formID === 'deadline-form-1' ? 1 : 2;
    var submit_time = $('#round' + roundNumber + '-submit').val();
    var result_time = $('#round' + roundNumber + '-result').val();
    var note = $('#round' + roundNumber + '-title').val();
    var isReset = $('#round' + roundNumber + '-submit-button').val() === 'Reset';
    console.log(isReset)

    if (isReset) {
        resetForm(roundNumber);
        return;
    }

    // Reset form
    function resetForm(roundNumber) {
        $.ajax({
            url: '/update_deadline',
            method: 'POST',
            data: {round_num: roundNumber, reset: 'true'},
            success: function (result) {
                $('#round' + roundNumber + '-submit').val('');
                $('#round' + roundNumber + '-result').val('');
                $('#round' + roundNumber + '-title').val('');
                $('#deadline-form-' + roundNumber + ' .submit-button').val('Save');
                location.reload()
            }
        })
    }

    // submit form
    $.ajax({
        url: '/update_deadline',
        method: 'POST',
        data: {
            submit_time: submit_time,
            result_time: result_time,
            note: note,
            round_num: roundNumber
        },
        success: function (result) {
            $('#round' + roundNumber + '-submit').val(submit_time)
            $('#round' + roundNumber + '-result').val(result_time)
            $('#round' + roundNumber + '-title').val(note)
            $('#deadline-form-' + roundNumber + ' .submit-button').val('Reset');
            location.reload()
        }
    })
})

// Delete note
$('.delete-note').click(function (e) {
    e.preventDefault()
    var noteID = $(this).data('note-id');
    var element = $(this).closest('.quick-stack-2')

    var confirmed = confirm("Are you sure you want to delete this topic?");

    if (confirmed) {
        $.ajax({
            url: '/delete_note/' + noteID,
            method: 'GET',
            success: function (result) {
                element.remove()
            }
        })
    }
})

// Pagination and Search
$(document).ready(function () {
    var pageSize = 5;
    var currentPage = 1;
    var students = $('.student-item');
    var visibleStudents = students;
    var pageCount = updatePageCount();

    function updatePageCount() {
        // Update the page count
        return Math.ceil(visibleStudents.length / pageSize);
    }

    function updateButtons() {
        // Update the buttons
        $('#pre-page').toggleClass('disabled', currentPage === 1);
        $('#last-page').toggleClass('disabled', currentPage === pageCount);
        $('#page-number').text(currentPage + ' / ' + pageCount);
    }

    function toggleNoResultsMessage(show) {
        // Used to show or hide the "No results found" message
        if (show) {
            $('#no-results-message').removeClass('hidden');
        } else {
            $('#no-results-message').addClass('hidden');
        }
    }

    function renderPage() {
        // Render the current page
        students.addClass('hidden').removeClass('visible');
        var start = (currentPage - 1) * pageSize;
        visibleStudents.slice(start, start + pageSize).removeClass('hidden').addClass('visible');
        updateButtons();
        toggleNoResultsMessage(visibleStudents.length === 0);
    }

    $('#pre-page').click(function () {
        if (currentPage > 1) {
            currentPage--;
            renderPage();
        }
    });

    $('#last-page').click(function () {
        if (currentPage < pageCount) {
            currentPage++;
            renderPage();
        }
    });

    // Search Function
    $('#search-student').submit(function (e) {
        e.preventDefault();
        var searchTerm = $('input[name="search-student"]').val().toLowerCase();
        visibleStudents = students.filter(function () {
            var student = $(this);
            var name = student.find('#student-name').text().toLowerCase();
            var classNum = student.find('#student-class-number').text().toLowerCase();
            var userName = student.find('#student-username').text().toLowerCase();
            return !searchTerm || name.includes(searchTerm) || classNum.includes(searchTerm) || userName.includes(searchTerm);
        });
        currentPage = 1;
        pageCount = updatePageCount();
        renderPage();
    });

    renderPage();
});