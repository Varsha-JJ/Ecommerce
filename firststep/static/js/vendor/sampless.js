$(document).ready(function() {
    $('.filter-checkbox').on('change', function() {
        var categoryIds = [];
        $('.filter-checkbox[data-filter="category"]:checked').each(function() {
            categoryIds.push($(this).val());
        });
        var minPrice = $('#min-price').val();
        var maxPrice = $('#max-price').val();
        $.ajax({
            url: '/filter-products/',
            data: {
                'category_ids': categoryIds,
                'min_price': minPrice,
                'max_price': maxPrice,
            },
            success: function(response) {
                $('#product-grid').html(response);
            }
        });
    });
});
