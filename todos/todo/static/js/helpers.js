/*
 * By default, jQuery 1.4+ uses recursive serialization, which Django does
 * not support. Disable this feature.
 */
jQuery.ajaxSettings.traditional = true;

// Append a slash to Backbone urls
Backbone.Model.oldUrl = Backbone.Model.prototype.url;
Backbone.Model.prototype.url = function() {
    var base = Backbone.Model.oldUrl.call(this);
    return base + ((base.length > 0 && base.charAt(base.length - 1) === '/') ? '' : '/');
};

// Add Tastypie metadata to collections
Backbone.Collection.prototype.parse = function(response) {
    this.recent_meta = response.meta || {};
    return response.objects || response;
};
