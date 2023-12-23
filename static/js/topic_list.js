// Truncate text
function truncateText(selector, maxLength) {
    const elements = document.querySelectorAll(selector);
    elements.forEach(function (element) {
        let truncated = element.innerText;
        if (truncated.length > maxLength) {
            truncated = truncated.substring(0, maxLength) + '...';
        }
        element.innerText = truncated;
    });
}

$(document).ready(function () {
    // Clear other filters besides the current one
    function clearOtherFilters(currentFilter) {
        if (currentFilter !== 'type') {
            $('.type_link').removeClass('accent');
        }
        if (currentFilter !== 'supervisor') {
            $('.supervisor_link').removeClass('accent');
        }
        if (currentFilter !== 'search') {
            $('.topic_list').val('');
        }
    }


    var filterConditions = {typeId: [], supervisorId: [], topicId: []};

    function handleTopicFilter() {
        let selectedTopicsNumber = 0;
        let topics = $('#topic-section').children();
        topics.each(function () {
            let show = true;
            for (let filterCategory in filterConditions) {
                if (filterConditions[filterCategory].length > 0 &&
                    !(filterConditions[filterCategory].includes($(this).data(filterCategory)))) {
                    show = false
                }
            }
            if (show) {
                selectedTopicsNumber += 1;
                $(this).removeClass('hidden');
            } else {
                $(this).addClass('hidden');
            }
        })

        if (selectedTopicsNumber === 0) {
            $('#no-results-message').removeClass('hidden');
        } else {
            $('#no-results-message').addClass('hidden');
        }
    }

    // Filter by type
    $('.type_link').click(function () {
        var type_id = $(this).data('id');
        $(this).toggleClass('accent');
        if ($(this).hasClass('accent')) { // select
            filterConditions['typeId'].push(type_id);
        } else { // deselect
            filterConditions['typeId'] = $.grep(filterConditions['typeId'], function (n) {
                return n !== type_id;
            });
        }
        handleTopicFilter();
    });

    // Filter by supervisor
    $('.supervisor_link').click(function () {
        let supervisor_id = $(this).data('id');
        $(this).toggleClass('accent');
        if ($(this).hasClass('accent')) { // select
            filterConditions['supervisorId'].push(supervisor_id);
        } else { // deselect
            filterConditions['supervisorId'] = $.grep(filterConditions['supervisorId'], function (n) {
                return n !== supervisor_id;
            });

        }
        handleTopicFilter();
    });

    // Search function
    $('.topic_list').keyup(function () {
        var search_query = $(this).val();
        if ($.trim(search_query).length > 0) {
            $.ajax({
                url: '/topic_search',
                data: {'search_query': search_query},
                type: 'GET',
                success: function (response) {
                    let topic_ids = JSON.parse(response).topic_ids;
                    filterConditions["topicId"] = topic_ids;
                    handleTopicFilter();
                }
            });
        } else {
            filterConditions['topicId'] = [];
            handleTopicFilter();
        }
    });

    // Reset function
    $('#reset').click(function (e) {
        e.preventDefault();
        clearOtherFilters('');
        $('#topic-section').children('a').removeClass('hidden');
        $('#no-results-message').addClass('hidden');
    });
});
