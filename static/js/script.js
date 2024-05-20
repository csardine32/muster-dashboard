$(document).ready(function() {
    function fetchData() {
        $.getJSON('/data', function(data) {
            $('#musterTable tbody').empty();
            data.forEach(function(item) {
                $('#musterTable tbody').append('<tr><td>' + item.name + '</td><td>' + item.status + '</td></tr>');
            });
        });
    }
    fetchData();
    setInterval(fetchData, 5000);  // Update every 5 seconds
});

