(function() {


	function newLayerModel() {
		var self = this;
		self.name = ko.observable();
		self.url = ko.observable();
		self.layer_type = ko.observable();
		self.theme = ko.observable();
		self.arcgis_layers = ko.observable();
		return this;
	};
	app.viewModel.newLayer = ko.observable();

	app.viewModel.showAddLayerModal = function() {
		app.viewModel.newLayer(new newLayerModel());
		$('#add-layer-modal').modal('show');
	};

	app.viewModel.createLayer = function() {
		var theme_uri = "/api/v1/theme/" + app.viewModel.newLayer().theme().id + '/';
		var data = {
			name: app.viewModel.newLayer().name(),
			url: app.viewModel.newLayer().url(),
			layer_type: app.viewModel.newLayer().layer_type(),
			arcgis_layers: app.viewModel.newLayer().arcgis_layers(),
			themes: [theme_uri]
		};
		if (data.layer_type === 'ArcRest') {
			data.url = data.url + '/export';
			if (! data.arcgis_layer) {
				data.arcgis_layer = 0;
			}
		}
		$.ajax({
			beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", app.csrftoken);
            },
			type: "POST",
			url: "/api/v1/layer/",
			contentType: "application/json; charset=utf-8",
			dataType: 'json',
			processData: false,
			dataType: "json",
			data: JSON.stringify(data)
		})
			.success(function(data) {
				var layer = new layerModel(data);
				$.each(app.viewModel.themes(), function (i, theme) {
					if (theme.name === data.themes[0].display_name) {
						theme.layers.push(layer);
						if (! theme.isOpenTheme()) {
							theme.setOpenTheme();	
						}
						layer.activateLayer();
					}
				});
			});
	};

})();