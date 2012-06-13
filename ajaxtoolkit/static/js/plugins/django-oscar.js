/**
 * Django ajax toolkit oscar plugin
 * Copyright (c) 2012 Eleni Lixourioti
 *
 * Requires ui.js from django-oscar>=0.2
 */



// Override this to change default error behaviour
oscar.messages.jsonParsingError = function(e, xhr, settings) {
    var self = oscar.messages;
    self.warning("There was an error with your last request, please try again.");
}

oscar.messages.ajaxInit = function() {
    var self = oscar.messages;
    $('#messages').ajaxSuccess(function(e, xhr, settings) {
        var resp_data;
        try {
            resp_data = $.parseJSON(xhr.responseText);
        } catch(err) {
            self.jsonParsingError(e, xhr, settings)
        }
        if (resp_data && resp_data['django_messages']) {
            var django_messages = resp_data['django_messages'];
            var i = django_messages.length, message;
            for (i; i--; ){
                message = django_messages[i];
                self.addMessage(message['extra_tags'], message['message']);
            }
        }
    });
}

$(function(){
    oscar.messages.ajaxInit();
});

