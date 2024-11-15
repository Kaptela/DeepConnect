$(window).on('load', function () {
    const pick_btns = $('.pick-btn');

    pick_btns.each(function () {
        $(this).on('click', function () {
            const type = $(this).attr('item-type');
            const id = $(this).attr('item-id');
            $.ajax({
                url: '/api/pick_item/',
                method: 'POST',
                contentType: 'application/json', // Specify content type
                dataType: 'json', // Expect JSON response
                data: JSON.stringify({ // Преобразование данных в JSON
                    item_type: type,
                    item_id: id
                }),
                success: function (data) {
                    location.reload();
                },
                error: function (xhr, status, error) {
                    console.log(xhr);
                    alert('An error occurred. Please try again.');
                }
            });
        });
    });
});