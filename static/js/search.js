$(document).ready(function () {
    $('#ticker').keyup(function () {
        var query = $(this).val();
        if (query !== '') {
            console.log("Fetching suggestions for query:", query); // Debugging line
            $.ajax({
                url: "/stock/suggestions",
                data: {
                    'query': query
                },
                dataType: 'json',
                success: function (data) {
                    console.log("Received suggestions:", data.suggestions); // Debugging line
                    var suggestions = data.suggestions;
                    var suggestionList = $('#suggestions');
                    suggestionList.empty();
                    if (suggestions.length > 0) {
                        $.each(suggestions, function (i, suggestion) {
                            suggestionList.append('<li class="suggestion">' + suggestion + '</li>');
                        });
                        $('.suggestions').show();
                    } else {
                        $('.suggestions').hide();
                    }
                }
            });
        } else {
            $('.suggestions').hide();
        }
    });

    $(document).on('click', '.suggestion', function () {
        var ticker = $(this).text();
        window.location.href = "/company?key=" + ticker;
    });

    $(document).mouseup(function (e) {
        var container = $(".suggestions-container");
        if (!container.is(e.target) && container.has(e.target).length === 0) {
            container.find('.suggestions').hide();
        }
    });
});