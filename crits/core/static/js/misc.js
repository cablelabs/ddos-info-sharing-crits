$(document).ready(function() {
$('#object_misc').editable(function(value, settings) {
    var revert = this.revert;
    return function(value, settings, elem) {
        var data = {
            type: subscription_type,
            id: subscription_id,
            misc: value,
        };
        $.ajax({
            type: "POST",
            async: false,
            url: misc_update,
            data: data,
            success: function(data) {
                if (!data.success) {
                    value = revert;
                    $('#object_misc_error').text(' Error: ' + data.message);
                }
            }
        });
        var escapes = {
            '&': '&amp;',
            '"': '&quot;',
            "'": '&apos;',
            '>': '&gt;',
            '<': '&lt;'
        };

        return value.replace(/&(?!amp;|quot;|apos;|gt;|lt;)|["'><]/g,
                             function (s) { return escapes[s]; });
    }(value, settings, this);
    },
    {
        type: 'textarea',
        height: "50px",
        width: "400px",
        tooltip: "",
        cancel: "Cancel",
        submit: "Ok",
        onblur: 'ignore',
});
});
